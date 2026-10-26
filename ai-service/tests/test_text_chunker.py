"""
Tests for text chunking module.
"""
from app.services.text_chunker import TextChunker


def test_chunking_metadata_preservation():
    chunker = TextChunker(chunk_size=100, overlap=20)
    pages = [
        {"page_number": 1, "text": "Page one paragraph text that is relatively long and descriptive. " * 3},
        {"page_number": 2, "text": "Page two text containing different evaluation observations and metrics."}
    ]

    chunks = chunker.chunk_paper_pages(paper_id="paper-uuid-123", pages=pages)

    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk["paper_id"] == "paper-uuid-123"
        assert chunk["page_number"] in (1, 2)
        assert chunk["chunk_id"].startswith("paper-uuid-123-p")
        assert len(chunk["text"]) > 0


def test_empty_page_handling():
    chunker = TextChunker()
    pages = [
        {"page_number": 1, "text": "   \n\t  "},
        {"page_number": 2, "text": ""}
    ]
    chunks = chunker.chunk_paper_pages("paper-empty", pages)
    assert len(chunks) == 0
