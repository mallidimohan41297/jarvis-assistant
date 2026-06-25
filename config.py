import os
from pathlib import Path
from dotenv import load_dotenv

# Establish relative file directory lines cleanly using Path tracking
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Config:
    """Centralized environment properties management block."""
    GEMINI_API_KEY: str = "YOUR_GEMINI_API_KEY_HERE"
    MODEL_NAME: str = "gemini-2.5-flash"
    STORAGE_FILE: str = str(BASE_DIR / "notes.json")
    LOG_FILE: str = str(BASE_DIR / "jarvis_system.log")