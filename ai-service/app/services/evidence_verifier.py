"""
Evidence and Metric Verification Service.
Performs deterministic numeric and textual consistency checks to classify claims as:
- SUPPORTED
- CONTRADICTED
- INSUFFICIENT_EVIDENCE
- NOT_COMPARABLE
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from app.config import settings
from app.services.retrieval import RetrievalService
from app.services.text_chunker import TextChunker
from app.services.pdf_extractor import PdfExtractor
from app.utils.text_utils import extract_numbers_and_units, resolve_safe_path, find_paper_file, clean_text

logger = logging.getLogger(__name__)


class EvidenceVerifier:
    def __init__(self, retrieval_service: Optional[RetrievalService] = None):
        self.retrieval_service = retrieval_service or RetrievalService()
        self.chunker = TextChunker()

    def verify(self, claim: str, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verify a claim against the given papers' extracted chunks.
        """
        if not claim or not papers:
            return {
                "claim": claim,
                "verification_status": "INSUFFICIENT_EVIDENCE",
                "explanation": "No claim or no papers provided for verification.",
                "evidence": []
            }

        # 1. Gather all chunks across specified papers
        all_chunks = []
        paper_titles = {}
        for p in papers:
            pid = p.get("paper_id")
            title = p.get("title") or "Untitled Paper"
            paper_titles[pid] = title
            pages = []
            storage_path = p.get("storage_path")

            if storage_path:
                try:
                    full_path = find_paper_file(settings.storage_path, storage_path)
                    if full_path and full_path.is_file():
                        extraction = PdfExtractor.extract_from_path(full_path, pid)
                        pages = extraction.get("pages", [])
                except Exception as e:
                    logger.warning("Failed to extract pages for paper %s in verifier: %s", pid, e)

            if not pages and p.get("extracted_text"):
                pages = [{"page_number": 1, "text": p.get("extracted_text")}]

            chunks = self.chunker.chunk_paper_pages(pid, pages)
            all_chunks.extend(chunks)

        if not all_chunks:
            return {
                "claim": claim,
                "verification_status": "INSUFFICIENT_EVIDENCE",
                "explanation": "No text content could be extracted from the specified papers.",
                "evidence": []
            }

        # 2. Retrieve top matching chunks for the claim
        relevant_chunks = self.retrieval_service.retrieve(claim, all_chunks, top_k=3)

        if not relevant_chunks or relevant_chunks[0].get("relevance_score", 0.0) < 0.05:
            return {
                "claim": claim,
                "verification_status": "INSUFFICIENT_EVIDENCE",
                "explanation": "No relevant text matching the claim was found in the papers.",
                "evidence": []
            }

        # Format evidence items
        evidence_items = []
        for rc in relevant_chunks:
            pid = rc.get("paper_id")
            evidence_items.append({
                "paper_id": pid,
                "paper_title": paper_titles.get(pid, "Paper"),
                "page_number": rc.get("page_number"),
                "quotation": rc.get("text")[:300],
                "relevance_score": rc.get("relevance_score", 0.0)
            })

        # 3. Numeric & Metric Verification
        claim_numbers = extract_numbers_and_units(claim)
        best_chunk_text = relevant_chunks[0].get("text", "")
        evidence_numbers = extract_numbers_and_units(best_chunk_text)

        # Check for numeric consistency
        if claim_numbers:
            for c_val, c_unit in claim_numbers:
                if evidence_numbers:
                    matching_unit_e = [e for e in evidence_numbers if c_unit and e[1] and c_unit == e[1]]
                    if matching_unit_e:
                        e_val, e_unit = matching_unit_e[0]
                        if abs(c_val - e_val) > 0.01:
                            return {
                                "claim": claim,
                                "verification_status": "CONTRADICTED",
                                "explanation": (
                                    f"Claim reports {c_val}{c_unit}, but evidence reports {e_val}{e_unit} "
                                    f"(Paper {relevant_chunks[0]['paper_id']}, Page {relevant_chunks[0]['page_number']})."
                                ),
                                "evidence": evidence_items
                            }
                        else:
                            return {
                                "claim": claim,
                                "verification_status": "SUPPORTED",
                                "explanation": (
                                    f"Numeric value {c_val}{c_unit} is directly corroborated by the text "
                                    f"on Page {relevant_chunks[0]['page_number']}."
                                ),
                                "evidence": evidence_items
                            }
                    elif c_unit and any(e[1] for e in evidence_numbers if e[1]):
                        diff_units = [e[1] for e in evidence_numbers if e[1]]
                        return {
                            "claim": claim,
                            "verification_status": "NOT_COMPARABLE",
                            "explanation": (
                                f"Claim references metric with unit '{c_unit}', but evidence evaluates under "
                                f"different metrics or units ({diff_units})."
                            ),
                            "evidence": evidence_items
                        }
                    else:
                        exact_match = any(abs(c_val - e[0]) <= 0.01 for e in evidence_numbers)
                        if not exact_match:
                            e_vals = [str(e[0]) for e in evidence_numbers]
                            return {
                                "claim": claim,
                                "verification_status": "CONTRADICTED",
                                "explanation": (
                                    f"Claim reports numeric value {c_val}, but evidence reports {e_vals}."
                                ),
                                "evidence": evidence_items
                            }

        # 4. Textual Corroboration (Lexical / Semantic)
        top_score = relevant_chunks[0].get("relevance_score", 0.0)
        top_text_lower = best_chunk_text.lower()
        claim_words = [w for w in clean_text(claim).lower().split() if len(w) > 3]

        match_count = sum(1 for w in claim_words if w in top_text_lower)
        overlap_ratio = match_count / max(len(claim_words), 1)

        # Look for explicit negation in evidence
        negation_terms = ["does not", "fails to", "cannot", "contradicts", "disproved", "inferior"]
        claim_has_negation = any(neg in claim.lower() for neg in negation_terms)
        evidence_has_negation = any(neg in top_text_lower for neg in negation_terms)

        if claim_has_negation != evidence_has_negation and overlap_ratio > 0.6:
            return {
                "claim": claim,
                "verification_status": "CONTRADICTED",
                "explanation": (
                    f"Evidence contains conflicting polarity or negation regarding the claim "
                    f"(Paper {relevant_chunks[0]['paper_id']}, Page {relevant_chunks[0]['page_number']})."
                ),
                "evidence": evidence_items
            }

        if overlap_ratio >= 0.5 or top_score >= 0.4:
            return {
                "claim": claim,
                "verification_status": "SUPPORTED",
                "explanation": (
                    f"Claim is supported by text extracted from Paper {relevant_chunks[0]['paper_id']}, "
                    f"Page {relevant_chunks[0]['page_number']}."
                ),
                "evidence": evidence_items
            }

        return {
            "claim": claim,
            "verification_status": "INSUFFICIENT_EVIDENCE",
            "explanation": (
                "Relevant context was found, but evidence is insufficient to conclusively verify or refute the claim."
            ),
            "evidence": evidence_items
        }
