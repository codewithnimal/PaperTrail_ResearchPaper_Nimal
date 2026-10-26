"""
PDF text extraction using PyMuPDF (fitz).
Preserves page-level structure and detects scanned/empty documents.
"""
import io
import fitz  # PyMuPDF
from typing import Dict, Any, List, Optional
from pathlib import Path
from app.utils.text_utils import extract_title_from_text


class PdfExtractor:
    @staticmethod
    def extract_from_bytes(file_bytes: bytes, paper_id: str) -> Dict[str, Any]:
        """Extract page-level text from PDF bytes."""
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {str(e)}")

        return PdfExtractor._process_doc(doc, paper_id)

    @staticmethod
    def extract_from_path(file_path: Path, paper_id: str) -> Dict[str, Any]:
        """Extract page-level text from a local PDF path."""
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        try:
            doc = fitz.open(str(file_path))
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {str(e)}")

        return PdfExtractor._process_doc(doc, paper_id)

    @staticmethod
    def _process_doc(doc: fitz.Document, paper_id: str) -> Dict[str, Any]:
        page_count = len(doc)
        pages: List[Dict[str, Any]] = []
        total_extracted_chars = 0
        first_page_raw_text = ""

        try:
            for i, page in enumerate(doc):
                page_num = i + 1  # 1-indexed
                text = page.get_text("text")
                total_extracted_chars += len(text.strip())
                if page_num == 1:
                    first_page_raw_text = text

                pages.append({
                    "page_number": page_num,
                    "text": text
                })
        finally:
            doc.close()

        warning = None
        if page_count == 0:
            warning = "PDF has 0 pages or is empty."
        elif total_extracted_chars < 50:
            warning = "PDF contains no extractable text. Scanned or image-only document; OCR may be required."

        title = extract_title_from_text(first_page_raw_text)

        return {
            "paper_id": paper_id,
            "page_count": page_count,
            "title": title,
            "pages": pages,
            "warning": warning
        }
