"""
Tests for PDF text extraction service.
"""
import pytest
import fitz
from app.services.pdf_extractor import PdfExtractor


def create_test_pdf(pages_text: list[str]) -> bytes:
    """Helper to generate an in-memory PDF with specified pages."""
    doc = fitz.open()
    for text in pages_text:
        page = doc.new_page()
        page.insert_text((50, 50), text)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_valid_pdf_extraction_and_page_preservation():
    pages = [
        "Title: Attention Is All You Need\nAuthors: Vaswani et al.\nAbstract: We propose Transformer.",
        "Methodology: Multi-head attention mechanisms replace recurrent layers.",
        "Results: We achieved 28.4 BLEU score on WMT 2014 English-to-German."
    ]
    pdf_bytes = create_test_pdf(pages)
    result = PdfExtractor.extract_from_bytes(pdf_bytes, paper_id="test-paper-1")

    assert result["paper_id"] == "test-paper-1"
    assert result["page_count"] == 3
    assert len(result["pages"]) == 3
    # Check 1-indexed page numbering
    assert result["pages"][0]["page_number"] == 1
    assert "Attention Is All You Need" in result["pages"][0]["text"]
    assert result["pages"][1]["page_number"] == 2
    assert "Multi-head attention" in result["pages"][1]["text"]
    assert result["pages"][2]["page_number"] == 3
    assert "28.4 BLEU" in result["pages"][2]["text"]
    assert result["warning"] is None


def test_empty_or_scanned_pdf_warning():
    # PDF with blank page (no text)
    doc = fitz.open()
    doc.new_page()  # empty
    pdf_bytes = doc.tobytes()
    doc.close()

    result = PdfExtractor.extract_from_bytes(pdf_bytes, paper_id="blank-paper")
    assert result["page_count"] == 1
    assert result["warning"] is not None
    assert "no extractable text" in result["warning"].lower() or "ocr" in result["warning"].lower()


def test_corrupt_pdf_handling():
    corrupt_bytes = b"not a real pdf content"
    with pytest.raises(ValueError, match="Failed to parse PDF document"):
        PdfExtractor.extract_from_bytes(corrupt_bytes, paper_id="corrupt-paper")
