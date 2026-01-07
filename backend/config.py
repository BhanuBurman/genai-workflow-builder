import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    def __init__(self):
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        self.debug: bool = os.getenv("DEBUG", "True").lower() == "true"
        self.api_host: str = os.getenv("API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        
        # Parse CORS origins from comma-separated string
        cors_origins_str = os.getenv(
            "CORS_ORIGINS", 
            "http://localhost:3000,http://localhost:5173"
        )
        self.cors_origins: List[str] = [
            origin.strip() 
            for origin in cors_origins_str.split(",") 
            if origin.strip()
        ]


settings = Settings()

