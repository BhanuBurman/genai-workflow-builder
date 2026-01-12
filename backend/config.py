import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    def __init__(self):
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
        self.API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
        self.API_PORT: int = int(os.getenv("API_PORT", "8000"))
        self.PROJECT_NAME: str = "Workflow Builder AI"
        self.PROJECT_BASE_DIR: Path = Path(os.getenv("PROJECT_BASE_DIR", "."))
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "")

        # User files directory
        self.USER_FILES_DIR: Path = self.PROJECT_BASE_DIR / "user_files"

        # Vector database directory
        self.CHROMA_DB_PATH: Path = self.PROJECT_BASE_DIR / "chroma_db"

        self.LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gpt-4o")
        self.TIKTOKEN_MODEL_NAME: str = os.getenv("TIKTOKEN_MODEL_NAME", "gpt-4o")
        self.EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-small")
        self.EMBEDDING_TIKTOKEN_MODEL_NAME: str = os.getenv("EMBEDDING_TIKTOKEN_MODEL_NAME", "text-embedding-3-small")
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_BASE_URL: str = os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
        self.TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

        self.HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")

        # Parse CORS origins from comma-separated string
        cors_origins_str = os.getenv(
            "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
        )
        self.CORS_ORIGINS: List[str] = [
            origin.strip() for origin in cors_origins_str.split(",") if origin.strip()
        ]


settings = Settings()
