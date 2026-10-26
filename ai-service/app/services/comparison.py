"""
Paper comparison service.
Generates structured paper comparisons using either an LLM provider (if configured)
or a reliable deterministic heuristic extraction fallback.
"""
import logging
import re
from typing import List, Dict, Any, Optional
from app.config import settings
from app.services.retrieval import RetrievalService
from app.services.text_chunker import TextChunker
from app.services.pdf_extractor import PdfExtractor
from app.utils.text_utils import resolve_safe_path, find_paper_file, clean_text

logger = logging.getLogger(__name__)


class ComparisonService:
    def __init__(self, retrieval_service: Optional[RetrievalService] = None):
        self.retrieval_service = retrieval_service or RetrievalService()
        self.chunker = TextChunker()

    def compare(self, job_id: str, papers: List[Dict[str, Any]], question: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute paper comparison across multiple papers.
        """
        # 1. Gather text and chunks for each paper
        loaded_papers = []
        all_chunks = []

        for p in papers:
            paper_id = p.get("paper_id")
            title = p.get("title") or "Untitled Paper"
            storage_path = p.get("storage_path")
            pages = []

            # If storage_path provided, extract pages if not already extracted
            if storage_path:
                try:
                    full_path = find_paper_file(settings.storage_path, storage_path)
                    if full_path and full_path.is_file():
                        extraction = PdfExtractor.extract_from_path(full_path, paper_id)
                        pages = extraction.get("pages", [])
                        if not title or title == "Untitled Paper":
                            title = extraction.get("title") or title
                    else:
                        logger.warning("Could not find file for paper %s at storage_path=%s (base_dir=%s)", paper_id, storage_path, settings.storage_path)
                except Exception as e:
                    logger.error("Failed to extract pages for paper %s: %s", paper_id, e)

            # If extracted text directly provided or pages extracted
            if not pages and p.get("extracted_text"):
                pages = [{"page_number": 1, "text": p.get("extracted_text")}]

            chunks = self.chunker.chunk_paper_pages(paper_id, pages)
            all_chunks.extend(chunks)

            loaded_papers.append({
                "paper_id": paper_id,
                "title": title,
                "filename": p.get("filename"),
                "pages": pages,
                "chunks": chunks
            })

        # Check if LLM is enabled
        if settings.llm_enabled:
            llm_result = self._compare_with_llm(job_id, loaded_papers, all_chunks, question)
            if llm_result:
                return llm_result

        # Deterministic Grounded Fallback
        return self._compare_deterministic(job_id, loaded_papers, all_chunks, question)

    def _compare_deterministic(
        self,
        job_id: str,
        loaded_papers: List[Dict[str, Any]],
        all_chunks: List[Dict[str, Any]],
        question: Optional[str]
    ) -> Dict[str, Any]:
        """
        Deterministic, rule-based extraction that NEVER invents data.
        Scans chunk text for specific key phrases and metrics.
        """
        research_problem = {}
        methodology = {}
        dataset = {}
        evaluation_metrics = {}
        reported_results = {}
        limitations = {}
        future_work = {}
        evidence_references = []
        uncertainty_notes = []
        research_gaps = []

        aspect_keywords = {
            "research_problem": ["problem", "challenge", "objective", "aim", "propose", "focus on", "motivation"],
            "methodology": ["method", "architecture", "framework", "model", "algorithm", "approach", "pipeline"],
            "dataset": ["dataset", "data", "corpus", "benchmark", "samples", "collected from"],
            "evaluation_metrics": ["metric", "accuracy", "f1", "precision", "recall", "bleu", "loss", "rmse", "auc"],
            "reported_results": ["result", "achieve", "outperform", "baseline", "score", "table", "performance"],
            "limitations": ["limitation", "drawback", "restricted", "bottleneck", "assumption", "fails when"],
            "future_work": ["future work", "future direction", "further research", "next step", "remains to be investigated"],
        }

        comparison_matrix = {
            "research_problem": {},
            "methodology": {},
            "dataset": {},
            "evaluation_metrics": {},
            "reported_results": {},
            "limitations": {},
            "future_work": {}
        }

        for paper in loaded_papers:
            pid = paper["paper_id"]
            title = paper["title"]
            chunks = paper["chunks"]

            if not chunks:
                for aspect in aspect_keywords:
                    comparison_matrix[aspect][pid] = "Not reported (no text extracted)"
                continue

            extracted_aspects = {}
            for aspect, keywords in aspect_keywords.items():
                matched_chunk = None
                matched_sentence = None

                # Search through chunks for highest keyword density
                for c in chunks:
                    text_lower = c["text"].lower()
                    for kw in keywords:
                        if kw in text_lower:
                            matched_chunk = c
                            # Extract the specific sentence
                            sentences = re.split(r'(?<=[.!?]) +', c["text"])
                            for s in sentences:
                                if kw in s.lower():
                                    matched_sentence = s.strip()
                                    break
                            if matched_sentence:
                                break
                    if matched_sentence:
                        break

                if matched_chunk and matched_sentence:
                    # Grounded finding
                    extracted_aspects[aspect] = matched_sentence
                    comparison_matrix[aspect][pid] = matched_sentence
                    evidence_references.append({
                        "paper_id": pid,
                        "page_number": matched_chunk.get("page_number"),
                        "text": matched_sentence[:200]
                    })
                else:
                    extracted_aspects[aspect] = "Not reported"
                    comparison_matrix[aspect][pid] = "Not reported"

            research_problem[pid] = extracted_aspects["research_problem"]
            methodology[pid] = extracted_aspects["methodology"]
            dataset[pid] = extracted_aspects["dataset"]
            evaluation_metrics[pid] = extracted_aspects["evaluation_metrics"]
            reported_results[pid] = extracted_aspects["reported_results"]
            limitations[pid] = extracted_aspects["limitations"]
            future_work[pid] = extracted_aspects["future_work"]

        # Note on uncertainty and deterministic execution
        uncertainty_notes.append(
            "Comparison performed using deterministic keyword and lexical extraction. "
            "No generative hallucination was performed."
        )

        # Identify candidate research gaps based on limitations and future work
        for paper in loaded_papers:
            pid = paper["paper_id"]
            lim = limitations.get(pid, "")
            fw = future_work.get(pid, "")
            if lim and lim != "Not reported":
                research_gaps.append(f"Candidate gap from Paper {pid} limitation: {lim}")
            if fw and fw != "Not reported":
                research_gaps.append(f"Candidate research opportunity from Paper {pid} future work: {fw}")

        if not research_gaps:
            research_gaps.append("No explicit research gaps or stated limitations identified in the extracted text.")

        summary = (
            f"Compared {len(loaded_papers)} research papers across problem formulation, methodology, "
            f"datasets, evaluation metrics, limitations, and future work. "
            f"All claims reflect explicit sentences extracted from source documents."
        )
        if question:
            summary += f" Query focus: '{question}'."

        return {
            "job_id": job_id,
            "summary": summary,
            "research_problem": research_problem,
            "methodology": methodology,
            "dataset": dataset,
            "evaluation_metrics": evaluation_metrics,
            "reported_results": reported_results,
            "limitations": limitations,
            "future_work": future_work,
            "evidence_references": evidence_references[:20],
            "uncertainty_notes": uncertainty_notes,
            "research_gaps": research_gaps,
            "comparison_matrix": comparison_matrix,
            "papers": [
                {"paper_id": p["paper_id"], "title": p["title"]} for p in loaded_papers
            ]
        }
    def _normalize_comparison_result(
        self,
        job_id: str,
        parsed: Dict[str, Any],
        loaded_papers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Normalize and sanitize LLM comparison output to ensure consistent data structures.
        """
        paper_ids = [str(p["paper_id"]) for p in loaded_papers]

        def _val_to_str(val: Any) -> str:
            if val is None:
                return "Not reported"
            if isinstance(val, (int, float, bool)):
                return str(val)
            if isinstance(val, dict):
                return ", ".join(f"{k}: {_val_to_str(v)}" for k, v in val.items())
            if isinstance(val, list):
                return "; ".join(_val_to_str(item) for item in val)
            return str(val).strip()

        def _normalize_aspect_dict(raw: Any) -> Dict[str, str]:
            res: Dict[str, str] = {}
            if isinstance(raw, dict):
                for k, v in raw.items():
                    res[str(k)] = _val_to_str(v)
            elif isinstance(raw, list):
                for i, item in enumerate(raw):
                    pid = paper_ids[i] if i < len(paper_ids) else f"paper_{i}"
                    res[pid] = _val_to_str(item)
            elif raw is not None:
                for pid in paper_ids:
                    res[pid] = _val_to_str(raw)
            # Ensure every paper has an entry
            for pid in paper_ids:
                if pid not in res:
                    res[pid] = "Not reported"
            return res

        # 1. Summary
        summary = parsed.get("summary")
        if not summary or not isinstance(summary, str):
            summary = (
                f"Compared {len(loaded_papers)} research papers across problem formulation, methodology, "
                f"datasets, evaluation metrics, limitations, and future work."
            )

        # 2. Aspect dicts
        research_problem = _normalize_aspect_dict(parsed.get("research_problem"))
        methodology = _normalize_aspect_dict(parsed.get("methodology"))
        dataset = _normalize_aspect_dict(parsed.get("dataset") or parsed.get("datasets"))
        evaluation_metrics = _normalize_aspect_dict(parsed.get("evaluation_metrics") or parsed.get("metrics"))
        reported_results = _normalize_aspect_dict(parsed.get("reported_results") or parsed.get("results"))
        limitations = _normalize_aspect_dict(parsed.get("limitations"))
        future_work = _normalize_aspect_dict(parsed.get("future_work"))

        # 3. Evidence references
        raw_ev = parsed.get("evidence_references") or parsed.get("evidence") or []
        evidence_references = []
        if isinstance(raw_ev, dict):
            for pid, items in raw_ev.items():
                if isinstance(items, list):
                    for it in items:
                        if isinstance(it, dict):
                            it_copy = dict(it)
                            it_copy.setdefault("paper_id", str(pid))
                            it_copy["text"] = _val_to_str(it_copy.get("text") or it_copy.get("quotation") or "")
                            evidence_references.append(it_copy)
                        elif isinstance(it, str):
                            evidence_references.append({"paper_id": str(pid), "text": it})
                elif isinstance(items, dict):
                    it_copy = dict(items)
                    it_copy.setdefault("paper_id", str(pid))
                    it_copy["text"] = _val_to_str(it_copy.get("text") or it_copy.get("quotation") or "")
                    evidence_references.append(it_copy)
                elif isinstance(items, str):
                    evidence_references.append({"paper_id": str(pid), "text": items})
        elif isinstance(raw_ev, list):
            for it in raw_ev:
                if isinstance(it, dict):
                    it_copy = dict(it)
                    it_copy["text"] = _val_to_str(it_copy.get("text") or it_copy.get("quotation") or "")
                    evidence_references.append(it_copy)
                elif isinstance(it, str):
                    evidence_references.append({"text": it})

        # 4. Uncertainty notes
        raw_notes = parsed.get("uncertainty_notes") or []
        uncertainty_notes = []
        if isinstance(raw_notes, dict):
            for k, v in raw_notes.items():
                uncertainty_notes.append(f"{k}: {_val_to_str(v)}")
        elif isinstance(raw_notes, list):
            for it in raw_notes:
                uncertainty_notes.append(_val_to_str(it))
        elif isinstance(raw_notes, str):
            uncertainty_notes.append(raw_notes)

        # 5. Research gaps
        raw_gaps = parsed.get("research_gaps") or []
        research_gaps = []
        if isinstance(raw_gaps, dict):
            for k, v in raw_gaps.items():
                research_gaps.append(f"{k}: {_val_to_str(v)}")
        elif isinstance(raw_gaps, list):
            for it in raw_gaps:
                if isinstance(it, dict):
                    topic = it.get("topic") or it.get("gap") or it.get("area") or "Gap"
                    desc = it.get("description") or it.get("details") or it.get("observation") or _val_to_str(it)
                    research_gaps.append(f"{topic}: {desc}")
                else:
                    research_gaps.append(_val_to_str(it))
        elif isinstance(raw_gaps, str):
            research_gaps.append(raw_gaps)

        # 6. Comparison matrix
        raw_matrix = parsed.get("comparison_matrix") or {}
        comparison_matrix: Dict[str, Dict[str, Any]] = {}
        if isinstance(raw_matrix, dict):
            for dim_key, dim_val in raw_matrix.items():
                if isinstance(dim_val, dict):
                    comparison_matrix[dim_key] = {}
                    for k, v in dim_val.items():
                        comparison_matrix[dim_key][str(k)] = _val_to_str(v)
                elif isinstance(dim_val, list):
                    row_dict: Dict[str, str] = {}
                    for i, it in enumerate(dim_val):
                        pid = paper_ids[i] if i < len(paper_ids) else f"paper_{i}"
                        row_dict[pid] = _val_to_str(it)
                    comparison_matrix[dim_key] = row_dict

        # Ensure base standard dimensions exist in comparison_matrix if missing
        for dim_key, dim_dict in [
            ("research_problem", research_problem),
            ("methodology", methodology),
            ("dataset", dataset),
            ("evaluation_metrics", evaluation_metrics),
            ("reported_results", reported_results),
            ("limitations", limitations),
            ("future_work", future_work),
        ]:
            if dim_key not in comparison_matrix:
                comparison_matrix[dim_key] = dim_dict

        # 7. Papers list
        papers_list = [
            {"paper_id": p["paper_id"], "title": p["title"]} for p in loaded_papers
        ]

        return {
            "job_id": job_id,
            "summary": summary,
            "research_problem": research_problem,
            "methodology": methodology,
            "dataset": dataset,
            "evaluation_metrics": evaluation_metrics,
            "reported_results": reported_results,
            "limitations": limitations,
            "future_work": future_work,
            "evidence_references": evidence_references,
            "uncertainty_notes": uncertainty_notes,
            "research_gaps": research_gaps,
            "comparison_matrix": comparison_matrix,
            "papers": papers_list,
        }

    def _compare_with_llm(
        self,
        job_id: str,
        loaded_papers: List[Dict[str, Any]],
        all_chunks: List[Dict[str, Any]],
        question: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Optional LLM comparison using configured provider (openai or groq).
        Enforces strict instructions against hallucination.
        Falls back to deterministic extraction on any error.
        """
        provider = settings.llm_provider.lower()
        if provider not in ("openai", "groq") or not settings.llm_api_key:
            return None

        # Build shared prompt context
        context_lines = []
        for p in loaded_papers:
            context_lines.append(f"\n--- Paper ID: {p['paper_id']}, Title: {p['title']} ---")
            for c in p['chunks'][:4]:
                context_lines.append(f"[Page {c['page_number']}]: {c['text']}")

        prompt = (
            "You are a scientific research assistant. Compare the provided research papers based STRICTLY on the text provided.\n"
            "RULES:\n"
            "- Never fabricate metrics, citations, results, or page numbers.\n"
            "- If a paper does not report an aspect, state 'Not reported'.\n"
            "- Any candidate research gaps must be labeled as 'Candidate gap requiring validation'.\n\n"
            f"Papers content:\n{''.join(context_lines)}\n\n"
            f"User question: {question or 'Provide comprehensive comparison'}\n"
            "Return a JSON object with this structure:\n"
            "{\n"
            '  "summary": "Overall summary of the comparison",\n'
            '  "research_problem": {"<paper_id>": "problem description string"},\n'
            '  "methodology": {"<paper_id>": "method description string"},\n'
            '  "dataset": {"<paper_id>": "dataset description string"},\n'
            '  "evaluation_metrics": {"<paper_id>": "metrics description string"},\n'
            '  "reported_results": {"<paper_id>": "results description string"},\n'
            '  "limitations": {"<paper_id>": "limitations description string"},\n'
            '  "future_work": {"<paper_id>": "future work description string"},\n'
            '  "evidence_references": [{"paper_id": "<paper_id>", "page_number": 1, "text": "exact quote string"}],\n'
            '  "uncertainty_notes": ["note 1", "note 2"],\n'
            '  "research_gaps": ["Candidate gap requiring validation: gap 1"],\n'
            '  "comparison_matrix": {\n'
            '    "research_problem": {"<paper_id>": "string"},\n'
            '    "methodology": {"<paper_id>": "string"},\n'
            '    "dataset": {"<paper_id>": "string"},\n'
            '    "evaluation_metrics": {"<paper_id>": "string"},\n'
            '    "reported_results": {"<paper_id>": "string"},\n'
            '    "limitations": {"<paper_id>": "string"},\n'
            '    "future_work": {"<paper_id>": "string"}\n'
            '  },\n'
            '  "papers": [{"paper_id": "<paper_id>", "title": "<title>"}]\n'
            "}"
        )

        try:
            import json
            from app.schemas import CompareResponse

            if provider == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=settings.llm_api_key)
                response = client.chat.completions.create(
                    model=settings.llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.0
                )
                content = response.choices[0].message.content

            elif provider == "groq":
                from groq import Groq
                client = Groq(api_key=settings.llm_api_key)
                response = client.chat.completions.create(
                    model=settings.llm_model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a scientific research assistant. Always respond with valid JSON only."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0
                )
                content = response.choices[0].message.content

            clean_json = content.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```", 1)[1].split("```", 1)[0].strip()

            parsed = json.loads(clean_json)
            normalized = self._normalize_comparison_result(job_id, parsed, loaded_papers)
            # Validate against schema
            CompareResponse(**normalized)
            return normalized

        except Exception as e:
            logger.warning(f"LLM comparison failed ({provider}), using deterministic fallback: {e}")
            return None
