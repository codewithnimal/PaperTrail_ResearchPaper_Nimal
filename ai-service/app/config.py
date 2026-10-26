"""
PaperTrail AI Service configuration using pydantic-settings.
Loads from environment variables and .env file.
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Storage
    paper_storage_dir: str = "./data/papers"

    # LLM
    llm_provider: str = "none"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"

    # Embeddings
    embedding_provider: str = "none"
    embedding_api_key: str = ""
    embedding_model: str = "all-MiniLM-L6-v2"

    # Service
    ai_service_host: str = "0.0.0.0"
    ai_service_port: int = 8001
    max_file_size_mb: int = 20

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }

    @property
    def llm_enabled(self) -> bool:
        return self.llm_provider.lower() not in ("none", "") and bool(self.llm_api_key)

    @property
    def embedding_enabled(self) -> bool:
        return self.embedding_provider.lower() not in ("none", "")

    @property
    def storage_path(self) -> Path:
        path = Path(self.paper_storage_dir).resolve()
        if not path.exists() or not any(path.glob("*.pdf")):
            candidates = [
                (Path(__file__).parent.parent.parent / "backend-java" / "data" / "papers").resolve(),
                (Path(__file__).parent.parent / "data" / "papers").resolve(),
                (Path(__file__).parent.parent.parent / "data" / "papers").resolve(),
            ]
            for cand in candidates:
                if cand.exists() and any(cand.glob("*.pdf")):
                    return cand
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
