"""
Frontend initialization and utilities.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ENABLE_MEMORY_RAG = os.getenv("ENABLE_MEMORY_RAG", "true").lower() == "true"
ENABLE_SPEECH_RESPONSE = os.getenv("ENABLE_SPEECH_RESPONSE", "true").lower() == "true"
ENABLE_AUDIO_INPUT = os.getenv("ENABLE_AUDIO_INPUT", "true").lower() == "true"
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "~/.voice_assistant/chroma_data")
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "default_user")

__all__ = [
    "API_BASE_URL",
    "ENABLE_MEMORY_RAG",
    "ENABLE_SPEECH_RESPONSE",
    "ENABLE_AUDIO_INPUT",
    "CHROMA_DB_PATH",
    "DEFAULT_USER_ID"
]
