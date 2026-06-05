"""
Centralized configuration loader for the Mutual Fund FAQ Assistant.

Loads settings from environment variables (via .env file) with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env from project root ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)


# ── Groq LLM ─────────────────────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
LLM_FALLBACK_MODEL: str = os.getenv("LLM_FALLBACK_MODEL", "llama-3.1-8b-instant")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))
LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "200"))


# ── Embedding Model ──────────────────────────────────────────────────────────
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")


# ── Vector Store (ChromaDB) ──────────────────────────────────────────────────
CHROMA_PERSIST_DIR: str = os.getenv(
    "CHROMA_PERSIST_DIR",
    str(PROJECT_ROOT / "data" / "vectorstore"),
)
CHROMA_COLLECTION_NAME: str = os.getenv(
    "CHROMA_COLLECTION_NAME", "mutual_fund_faq"
)


# ── Retrieval ─────────────────────────────────────────────────────────────────
TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "5"))
SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))


# ── Chunking ──────────────────────────────────────────────────────────────────
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))


# ── Scheduler ─────────────────────────────────────────────────────────────────
SCHEDULER_HOUR: int = int(os.getenv("SCHEDULER_HOUR", "10"))
SCHEDULER_MINUTE: int = int(os.getenv("SCHEDULER_MINUTE", "0"))
SCHEDULER_TIMEZONE: str = os.getenv("SCHEDULER_TIMEZONE", "Asia/Kolkata")


# ── Server ────────────────────────────────────────────────────────────────────
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))


# ── Data Directories ─────────────────────────────────────────────────────────
DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
VECTORSTORE_DIR: Path = Path(CHROMA_PERSIST_DIR)


def ensure_data_dirs() -> None:
    """Create data directories if they don't exist."""
    for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, VECTORSTORE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def validate_config() -> list[str]:
    """
    Validate critical configuration values.

    Returns a list of error messages. Empty list means all checks passed.
    """
    errors: list[str] = []

    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        errors.append(
            "GROQ_API_KEY is not set. Please configure it in your .env file."
        )

    if CHUNK_SIZE <= 0:
        errors.append(f"CHUNK_SIZE must be positive, got {CHUNK_SIZE}.")

    if CHUNK_OVERLAP < 0 or CHUNK_OVERLAP >= CHUNK_SIZE:
        errors.append(
            f"CHUNK_OVERLAP ({CHUNK_OVERLAP}) must be >= 0 and < CHUNK_SIZE ({CHUNK_SIZE})."
        )

    if TOP_K_RESULTS <= 0:
        errors.append(f"TOP_K_RESULTS must be positive, got {TOP_K_RESULTS}.")

    if not 0.0 <= SIMILARITY_THRESHOLD <= 1.0:
        errors.append(
            f"SIMILARITY_THRESHOLD must be between 0.0 and 1.0, got {SIMILARITY_THRESHOLD}."
        )

    return errors
