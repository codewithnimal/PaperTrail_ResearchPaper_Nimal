"""
Configurable embedding interface.
Provides vector embeddings if configured, or flags as unavailable for lexical fallback.
"""
from typing import List, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.provider = settings.embedding_provider.lower()
        self.model_name = settings.embedding_model
        self.api_key = settings.embedding_api_key
        self._client = None
        self._initialize()

    def _initialize(self):
        if self.provider == "openai" and self.api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
                logger.info(f"Initialized OpenAI embedding provider ({self.model_name})")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self._client = None
        elif self.provider in ("sentence-transformers", "local"):
            try:
                from sentence_transformers import SentenceTransformer
                self._client = SentenceTransformer(self.model_name)
                logger.info(f"Initialized local SentenceTransformer ({self.model_name})")
            except Exception as e:
                logger.warning(f"Failed to load sentence-transformers model: {e}")
                self._client = None
        else:
            self._client = None

    def is_available(self) -> bool:
        return self._client is not None

    def get_provider_name(self) -> str:
        return self.provider

    def embed_texts(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Generate embeddings for a list of strings.
        Returns None if embedding provider is not available or fails.
        """
        if not self.is_available() or not texts:
            return None

        try:
            if self.provider == "openai":
                response = self._client.embeddings.create(
                    input=texts,
                    model=self.model_name
                )
                return [d.embedding for d in response.data]
            elif self.provider in ("sentence-transformers", "local"):
                embeddings = self._client.encode(texts, convert_to_numpy=True)
                return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error during embedding generation: {e}")
            return None

        return None

    def embed_query(self, query: str) -> Optional[List[float]]:
        results = self.embed_texts([query])
        return results[0] if results else None
