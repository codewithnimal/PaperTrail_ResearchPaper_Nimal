"""
Text chunking module with metadata preservation (paper ID, page number, chunk ID).
"""
import uuid
from typing import List, Dict, Any
from app.utils.text_utils import clean_text


class TextChunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_paper_pages(self, paper_id: str, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes page-level text list [{"page_number": int, "text": str}]
        and returns a list of chunks with preserved metadata.
        """
        all_chunks: List[Dict[str, Any]] = []

        for page in pages:
            page_num = page.get("page_number", 1)
            raw_text = page.get("text", "")
            cleaned = clean_text(raw_text)

            if not cleaned:
                continue

            # Slide window across page text
            start = 0
            text_len = len(cleaned)
            chunk_index = 0

            while start < text_len:
                end = min(start + self.chunk_size, text_len)
                chunk_text = cleaned[start:end]

                # Try to break at a sentence boundary or word boundary if not at the end
                if end < text_len:
                    last_period = chunk_text.rfind('. ')
                    if last_period != -1 and last_period > self.chunk_size // 2:
                        end = start + last_period + 1
                        chunk_text = cleaned[start:end]
                    else:
                        last_space = chunk_text.rfind(' ')
                        if last_space != -1 and last_space > self.chunk_size // 2:
                            end = start + last_space
                            chunk_text = cleaned[start:end]

                chunk_id = f"{paper_id}-p{page_num}-c{chunk_index}"
                all_chunks.append({
                    "chunk_id": chunk_id,
                    "paper_id": paper_id,
                    "page_number": page_num,
                    "text": chunk_text.strip(),
                    "char_count": len(chunk_text.strip()),
                })

                chunk_index += 1
                start += max(self.chunk_size - self.overlap, 1)

        return all_chunks
