"""
PaperTrail AI Service FastAPI Application.
Exposes internal endpoints for PDF extraction, comparison, retrieval, verification, and report generation.
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging

from app.config import settings
from app.schemas import (
    HealthResponse,
    ExtractResponse,
    CompareRequest,
    CompareResponse,
    RetrieveRequest,
    RetrieveResponse,
    VerifyRequest,
    VerifyResponse,
    ReportRequest,
    ReportResponse,
)
from app.services.pdf_extractor import PdfExtractor
from app.services.text_chunker import TextChunker
from app.services.retrieval import RetrievalService
from app.services.comparison import ComparisonService
from app.services.evidence_verifier import EvidenceVerifier
from app.services.report_generator import ReportGenerator
from app.exceptions import PdfProcessingError
from app.utils.text_utils import find_paper_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PaperTrail AI Service",
    description="Internal AI service for PDF extraction, multi-paper comparison, and evidence verification",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Initialize service instances
pdf_extractor = PdfExtractor()
text_chunker = TextChunker()
retrieval_service = RetrievalService()
comparison_service = ComparisonService(retrieval_service=retrieval_service)
evidence_verifier = EvidenceVerifier(retrieval_service=retrieval_service)
report_generator = ReportGenerator()


@app.get("/internal/health", response_model=HealthResponse)
async def health_check():
    """
    Check internal service health and AI configuration status without exposing credentials.
    """
    return HealthResponse(
        status="ok",
        service="PaperTrail AI Service",
        llm_enabled=settings.llm_enabled,
        embedding_enabled=settings.embedding_enabled,
        llm_provider=settings.llm_provider,
        embedding_provider=settings.embedding_provider,
    )


@app.post("/internal/extract", response_model=ExtractResponse)
async def extract_pdf(
    file: UploadFile = File(...),
    paper_id: str = Form(...)
):
    """
    Extract text page by page from an uploaded PDF file.
    Validates PDF format, preserves page numbering (1-indexed), and detects unextractable/scanned PDFs.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have .pdf extension."
        )

    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded PDF file is empty."
            )

        extraction = pdf_extractor.extract_from_bytes(content, paper_id)
        return ExtractResponse(**extraction)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process PDF for paper {paper_id}: {e}")
        raise PdfProcessingError(detail=f"Could not extract text from PDF: {str(e)}")


@app.post("/internal/compare", response_model=CompareResponse)
async def compare_papers(request: CompareRequest):
    """
    Perform multi-paper comparison extracting problem, methodology, dataset, metrics,
    results, limitations, and candidate research gaps.
    """
    if len(request.papers) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one paper is required for analysis."
        )

    try:
        papers_dict = [p.model_dump() for p in request.papers]
        result = comparison_service.compare(
            job_id=request.job_id,
            papers=papers_dict,
            question=request.question
        )
        return CompareResponse(**result)
    except Exception as e:
        logger.error(f"Error running comparison job {request.job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparison failed: {str(e)}"
        )


@app.post("/internal/retrieve", response_model=RetrieveResponse)
async def retrieve_chunks(request: RetrieveRequest):
    """
    Retrieve top-k relevant text chunks across papers for a search query.
    Employs semantic vector retrieval if available; otherwise uses documented lexical TF-IDF retrieval.
    """
    # Chunk all papers present in storage
    # In a full-blown deployment, chunks would be cached or stored in PostgreSQL/pgvector
    chunks = []
    # If paper_ids given, read them from configured storage directory
    if request.paper_ids:
        for pid in request.paper_ids:
            try:
                candidate_file = find_paper_file(settings.storage_path, f"{pid}.pdf")
                if candidate_file and candidate_file.exists():
                    ext = pdf_extractor.extract_from_path(candidate_file, pid)
                    chunks.extend(text_chunker.chunk_paper_pages(pid, ext.get("pages", [])))
            except Exception:
                continue

    results = retrieval_service.retrieve(
        query=request.query,
        chunks=chunks,
        paper_ids=request.paper_ids,
        top_k=request.top_k
    )

    formatted_results = [
        {
            "chunk_id": r["chunk_id"],
            "paper_id": r["paper_id"],
            "page_number": r["page_number"],
            "text": r["text"],
            "relevance_score": r["relevance_score"]
        }
        for r in results
    ]

    return RetrieveResponse(query=request.query, results=formatted_results)


@app.post("/internal/verify", response_model=VerifyResponse)
async def verify_evidence(request: VerifyRequest):
    """
    Check whether specified claims and metric comparisons are supported by paper evidence.
    Returns SUPPORTED, CONTRADICTED, INSUFFICIENT_EVIDENCE, or NOT_COMPARABLE.
    """
    try:
        papers_dict = [p.model_dump() for p in request.papers]
        result = evidence_verifier.verify(request.claim, papers_dict)
        return VerifyResponse(**result)
    except Exception as e:
        logger.error(f"Evidence verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification failed: {str(e)}"
        )


@app.post("/internal/report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Produce structured literature-review report in Markdown.
    """
    try:
        markdown = report_generator.generate_markdown(
            job_id=request.job_id,
            comparison_result=request.comparison_result,
            paper_ids=request.paper_ids
        )
        return ReportResponse(job_id=request.job_id, markdown=markdown)
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )
