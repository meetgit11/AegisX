"""
====================================================
AegisX Configuration Loader
====================================================

Loads environment variables from .env and exposes
them as application settings.

Author : Meet Patil
Project : AegisX
"""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    """Application Configuration"""

    app_name: str = os.getenv("APP_NAME", "AegisX")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    author: str = os.getenv("AUTHOR", "Unknown")

    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    default_timeout: int = int(os.getenv("DEFAULT_TIMEOUT", 2))

    default_port_start: int = int(os.getenv("DEFAULT_PORT_START", 1))
    default_port_end: int = int(os.getenv("DEFAULT_PORT_END", 1024))

    max_threads: int = int(os.getenv("MAX_THREADS", 100))

    output_directory: str = os.getenv("OUTPUT_DIRECTORY", "outputs")

    database_name: str = os.getenv("DATABASE_NAME", "aegisx.db")

    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()