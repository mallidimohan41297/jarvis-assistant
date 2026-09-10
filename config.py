import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class Config:
    """Centralized application configuration loaded from environment variables."""

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    STORAGE_FILE = str(BASE_DIR / "notes.json")
    LOG_FILE = str(BASE_DIR / "jarvis_system.log")
