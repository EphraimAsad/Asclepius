"""
Application configuration using Pydantic Settings.
"""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "Asclepius"
    app_version: str = "1.0.0"
    debug: bool = False

    # API
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql://postgres:password@db:5432/asclepius"

    # Rules - paths relative to project root (one level up from backend/)
    rulebook_path: Path = Path("../rules/compiled/compiled_rulebook.json")
    schema_path: Path = Path("../rules/schema/rulebook.schema.json")

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
