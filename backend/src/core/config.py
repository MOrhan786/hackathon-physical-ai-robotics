from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.GEMINI_API_KEY: str = self._get_required_env("GEMINI_API_KEY")
        self.QDRANT_URL: str = self._get_required_env("QDRANT_URL")
        self.QDRANT_API_KEY: str = self._get_required_env("QDRANT_API_KEY")
        self.NEON_DB_URL: str = self._get_required_env("NEON_DB_URL")
        self.API_KEY: str = self._get_required_env("API_KEY")
        # Gemini OpenAI-compatible endpoint
        self.GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"

    def _get_required_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' is not set.")
        return value

settings = Settings()
