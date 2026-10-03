from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Centralized configuration for Retail BDA Analytics Platform."""

    # Application metadata
    app_name: str = "Retail BDA Analytics Platform"
    app_version: str = "0.1.0"
    phase: str = "Phase 06"

    # Pipeline mode: "local" (default) | "hadoop" | "hive"
    # "local" uses Python/Pandas as fallback when Hadoop/Hive are unavailable
    pipeline_mode: str = "local"

    # Paths — always resolved relative to this config file so they
    # work on any Windows machine without hard-coded drive letters.
    project_root: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = Path(__file__).resolve().parent.parent / "data"
    output_dir: Path = Path(__file__).resolve().parent.parent / "output"
    dataset_path: Path = Path(__file__).resolve().parent.parent / "data" / "retail_logs.csv"

    # CORS allowed origins
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
