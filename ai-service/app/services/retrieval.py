"""
Retrieval engine supporting semantic vector search (when configured)
and robust lexical retrieval fallback (TF-IDF / keyword similarity).
"""
import math
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.embeddings import EmbeddingService


class RetrievalService:
    def __init__(self, embedding_service: Optional[EmbeddingService] = None):
        self.embedding_service = embedding_service or EmbeddingService()

    def retrieve(
        self,
        query: str,
        chunks: List[Dict[str, Any]],
        paper_ids: Optional[List[str]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the top_k relevant chunks for the given query.
        Filters by paper_ids if provided.
        """
        if not chunks or not query:
            return []

        # Filter chunks by paper_id if requested
        if paper_ids:
            allowed = set(paper_ids)
            filtered_chunks = [c for c in chunks if c.get("paper_id") in allowed]
        else:
            filtered_chunks = chunks

        if not filtered_chunks:
            return []

        # 1. Attempt Semantic Retrieval if embeddings available
        if self.embedding_service.is_available():
            results = self._semantic_retrieve(query, filtered_chunks, top_k)
            if results:
                return results

        # 2. Documented Lexical Fallback: TF-IDF Cosine Similarity
        return self._lexical_retrieve(query, filtered_chunks, top_k)

    def _semantic_retrieve(
        self, query: str, chunks: List[Dict[str, Any]], top_k: int
    ) -> Optional[List[Dict[str, Any]]]:
        try:
            chunk_texts = [c.get("text", "") for c in chunks]
            chunk_embeddings = self.embedding_service.embed_texts(chunk_texts)
            query_embedding = self.embedding_service.embed_query(query)

            if chunk_embeddings is None or query_embedding is None:
                return None

            chunk_vecs = np.array(chunk_embeddings)
            q_vec = np.array(query_embedding).reshape(1, -1)

            scores = cosine_similarity(q_vec, chunk_vecs)[0]

            ranked_indices = np.argsort(scores)[::-1][:top_k]

            results = []
            for idx in ranked_indices:
                chunk = chunks[idx].copy()
                chunk["relevance_score"] = float(round(scores[idx], 4))
                chunk["retrieval_mode"] = "semantic_vector"
                results.append(chunk)

            return results
        except Exception:
            return None

    def _lexical_retrieve(
        self, query: str, chunks: List[Dict[str, Any]], top_k: int
    ) -> List[Dict[str, Any]]:
        """
        Documented Lexical Retrieval Fallback using TF-IDF and Cosine Similarity.
        """
        chunk_texts = [c.get("text", "") for c in chunks]
        corpus = [query] + chunk_texts

        try:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(corpus)
            query_vec = tfidf_matrix[0:1]
            chunk_matrix = tfidf_matrix[1:]

            scores = cosine_similarity(query_vec, chunk_matrix)[0]
            ranked_indices = np.argsort(scores)[::-1][:top_k]

            results = []
            for idx in ranked_indices:
                chunk = chunks[idx].copy()
                score = float(round(scores[idx], 4))
                chunk["relevance_score"] = score
                chunk["retrieval_mode"] = "lexical_tfidf"
                results.append(chunk)

            return results
        except Exception:
            # Simple keyword overlap fallback if corpus is too small or uniform
            return self._keyword_overlap_retrieve(query, chunks, top_k)

    def _keyword_overlap_retrieve(
        self, query: str, chunks: List[Dict[str, Any]], top_k: int
    ) -> List[Dict[str, Any]]:
        query_words = set(query.lower().split())
        scored_chunks = []

        for c in chunks:
            text_words = set(c.get("text", "").lower().split())
            overlap = len(query_words.intersection(text_words))
            score = round(overlap / max(len(query_words), 1), 4)
            item = c.copy()
            item["relevance_score"] = float(score)
            item["retrieval_mode"] = "lexical_keyword_overlap"
            scored_chunks.append(item)

        scored_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_chunks[:top_k]
