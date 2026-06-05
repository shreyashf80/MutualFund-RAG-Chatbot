"""
Response Formatter for Mutual Fund FAQ Assistant.
Validates and structures the raw LLM output into a consistent
response format with answer, citation, and update footer.
"""

import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Pattern to find URLs in text
_URL_PATTERN = re.compile(r"https?://[^\s\)\]\"']+")

# Pattern to find the "Last updated" footer
_FOOTER_PATTERN = re.compile(
    r"Last updated from sources?:\s*(.+)", re.IGNORECASE
)


def format_response(
    raw_answer: str,
    retrieved_chunks: List[Dict],
) -> Dict:
    """
    Parse and validate the LLM output, ensuring it conforms to the
    expected response structure.

    Ensures:
      - Answer text is present (max 3 sentences enforced)
      - Exactly one citation link
      - "Last updated from sources: <date>" footer

    If the LLM omits the citation or footer, they are injected from
    the retrieved chunk metadata.

    Args:
        raw_answer: The raw text output from the Groq LLM.
        retrieved_chunks: The chunks returned by the retriever (for
                          fallback citation and date extraction).

    Returns:
        A structured response dict:
        {
            "status": "success",
            "type": "factual",
            "answer": "...",
            "citation": "https://...",
            "last_updated": "2026-06-03"
        }
    """
    if not raw_answer or not raw_answer.strip():
        return _no_info_response(retrieved_chunks)

    answer = raw_answer.strip()

    # ── Extract citation URL from the answer ─────────────────────────
    urls_in_answer = _URL_PATTERN.findall(answer)
    citation = _pick_best_citation(urls_in_answer, retrieved_chunks)

    # ── Extract or inject the "Last updated" footer ──────────────────
    footer_match = _FOOTER_PATTERN.search(answer)
    if footer_match:
        last_updated = footer_match.group(1).strip()
        # Remove the footer line from the answer body (we return it separately)
        answer = _FOOTER_PATTERN.sub("", answer).strip()
    else:
        last_updated = _get_scrape_date(retrieved_chunks)

    # ── Enforce max 3 sentences ──────────────────────────────────────
    answer = _limit_sentences(answer, max_sentences=3)

    # ── Clean up stray URL artifacts in the answer text ──────────────
    # (the citation is returned as a separate field)
    # We keep URLs in the answer text as the LLM may embed them naturally

    return {
        "status": "success",
        "type": "factual",
        "answer": answer,
        "citation": citation,
        "last_updated": last_updated,
    }


def _no_info_response(chunks: List[Dict]) -> Dict:
    """Return a standard 'no information' response."""
    return {
        "status": "success",
        "type": "factual",
        "answer": "I don't have this information in my current sources.",
        "citation": None,
        "last_updated": _get_scrape_date(chunks),
    }


def _pick_best_citation(
    urls_in_answer: List[str],
    chunks: List[Dict],
) -> Optional[str]:
    """
    Pick exactly one citation URL.

    Priority:
      1. First Groww URL found in the LLM answer
      2. source_url from the top retrieved chunk
    """
    # Prefer a Groww URL from the answer
    for url in urls_in_answer:
        if "groww.in" in url:
            return url.rstrip(".")

    # Fall back to the top chunk's source_url
    if chunks:
        url = chunks[0].get("metadata", {}).get("source_url", "")
        if url:
            return url

    # Any URL from the answer
    if urls_in_answer:
        return urls_in_answer[0].rstrip(".")

    return None


def _get_scrape_date(chunks: List[Dict]) -> str:
    """Extract the most recent scrape date from chunk metadata."""
    if not chunks:
        return "Date unavailable"

    dates = []
    for chunk in chunks:
        date = chunk.get("metadata", {}).get("scrape_date", "")
        if date:
            dates.append(date)

    if dates:
        # Return the most recent date (lexicographic sort works for ISO dates)
        return sorted(dates, reverse=True)[0]

    return "Date unavailable"


def _limit_sentences(text: str, max_sentences: int = 3) -> str:
    """
    Limit text to max_sentences sentences.

    Uses a simple sentence-boundary regex that handles common cases
    (periods, question marks, exclamation marks followed by space or end).
    """
    # Split on sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", text)

    if len(sentences) <= max_sentences:
        return text

    limited = " ".join(sentences[:max_sentences])

    # Ensure it ends with proper punctuation
    if not limited.rstrip().endswith((".", "!", "?")):
        limited = limited.rstrip() + "."

    logger.info(
        f"Truncated response from {len(sentences)} to {max_sentences} sentences."
    )

    return limited
