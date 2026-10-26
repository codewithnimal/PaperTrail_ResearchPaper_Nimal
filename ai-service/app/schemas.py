"""
Pydantic schemas for request and response validation in the AI Service.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "PaperTrail AI Service"
    llm_enabled: bool
    embedding_enabled: bool
    llm_provider: str
    embedding_provider: str


class PageText(BaseModel):
    page_number: int
    text: str


class ExtractResponse(BaseModel):
    paper_id: str
    page_count: int
    title: Optional[str] = None
    pages: List[PageText] = []
    warning: Optional[str] = None


class PaperInput(BaseModel):
    paper_id: str
    title: Optional[str] = None
    filename: Optional[str] = None
    storage_path: Optional[str] = None
    extracted_text: Optional[str] = None


class CompareRequest(BaseModel):
    job_id: str
    papers: List[PaperInput]
    question: Optional[str] = None


class EvidenceReference(BaseModel):
    paper_id: Optional[str] = None
    page_number: Optional[int] = None
    text: str = ""


class CompareResponse(BaseModel):
    job_id: str
    summary: str
    research_problem: Dict[str, Any] = Field(default_factory=dict)
    methodology: Dict[str, Any] = Field(default_factory=dict)
    dataset: Dict[str, Any] = Field(default_factory=dict)
    evaluation_metrics: Dict[str, Any] = Field(default_factory=dict)
    reported_results: Dict[str, Any] = Field(default_factory=dict)
    limitations: Dict[str, Any] = Field(default_factory=dict)
    future_work: Dict[str, Any] = Field(default_factory=dict)
    evidence_references: List[Any] = Field(default_factory=list)
    uncertainty_notes: List[Any] = Field(default_factory=list)
    research_gaps: List[Any] = Field(default_factory=list)
    comparison_matrix: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    papers: List[Dict[str, Any]] = Field(default_factory=list)


class RetrieveRequest(BaseModel):
    query: str
    paper_ids: Optional[List[str]] = None
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievedChunk(BaseModel):
    chunk_id: str
    paper_id: str
    page_number: int
    text: str
    relevance_score: float


class RetrieveResponse(BaseModel):
    query: str
    results: List[RetrievedChunk]


class VerifyRequest(BaseModel):
    claim: str
    papers: List[PaperInput]


class EvidenceItem(BaseModel):
    paper_id: str
    paper_title: Optional[str] = None
    page_number: Optional[int] = None
    quotation: Optional[str] = None
    relevance_score: float = 0.0


class VerifyResponse(BaseModel):
    claim: str
    verification_status: str  # SUPPORTED, CONTRADICTED, INSUFFICIENT_EVIDENCE, NOT_COMPARABLE
    explanation: str
    evidence: List[EvidenceItem] = Field(default_factory=list)


class ReportRequest(BaseModel):
    job_id: str
    comparison_result: Dict[str, Any]
    paper_ids: Optional[str] = None


class ReportResponse(BaseModel):
    job_id: str
    markdown: str
