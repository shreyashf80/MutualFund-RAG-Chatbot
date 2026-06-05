"""
Query Classifier for Mutual Fund FAQ Assistant.
Classifies user queries as 'factual', 'advisory', or 'pii_detected'
using rule-based pattern matching with LLM fallback for ambiguous cases.
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


# ── PII Detection Patterns ───────────────────────────────────────────────────
# These are checked FIRST — PII must be blocked before any classification.

_PII_PATTERNS = {
    "pan": re.compile(
        # PAN: exactly 5 uppercase letters + 4 digits + 1 uppercase letter
        # Use word boundaries to avoid matching fund names like "HDFC BSE Sensex"
        r"\b[A-Z]{5}\d{4}[A-Z]\b"
    ),
    "aadhaar": re.compile(
        # Aadhaar: 12 digits, optionally separated by spaces or hyphens
        r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"
    ),
    "phone": re.compile(
        # Indian phone: 10 digits starting with 6-9, optionally prefixed with +91 or 0
        r"(?:\+91[\s-]?|0)?[6-9]\d{9}\b"
    ),
    "email": re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    ),
    "otp": re.compile(
        # OTP: 4-6 digit number mentioned near keywords like "otp", "code", "verify"
        r"\b(?:otp|code|verify|verification)\b.*?\b\d{4,6}\b"
        r"|\b\d{4,6}\b.*?\b(?:otp|code|verify|verification)\b",
        re.IGNORECASE,
    ),
    "folio": re.compile(
        # Folio/account number: keyword + 6-12 digit number
        r"\b(?:folio|account)\s*(?:number|no\.?|#)?\s*(?:is|:)?\s*\d{6,12}\b",
        re.IGNORECASE,
    ),
}

# Fund names and terms that could trigger false positive PII matches
_PII_FALSE_POSITIVE_TERMS = [
    "nifty 50", "nifty50", "top 20", "next 50", "nifty 100",
    "sensex", "bse 500", "50:50", "50:25:25",
]


# ── Advisory Pattern Detection ───────────────────────────────────────────────

_ADVISORY_PATTERNS = [
    # Direct advice-seeking
    r"\bshould\s+i\b",
    r"\bdo\s+you\s+recommend\b",
    r"\brecommend\b",
    r"\bgood\s+investment\b",
    r"\bbad\s+investment\b",
    r"\bworth\s+investing\b",
    r"\bwill\s+it\s+give\b",
    r"\bwill\s+.*?\bgo\s+up\b",
    r"\bwill\s+.*?\bgo\s+down\b",
    r"\bwill\s+(?:the\s+)?(?:fund|nav|returns?)\b.*?\b(?:increase|decrease|rise|fall|grow)\b",
    # Comparisons
    r"\bwhich\s+is\s+better\b",
    r"\bwhich\s+(?:one|fund|scheme)\s+(?:should|to|is)\b",
    r"\bwhich\s+has\s+(?:a\s+)?(?:lower|higher|better|worse)\b",
    r"\bbetter\s+(?:than|option|choice)\b",
    r"\bcompare\b",
    r"\bvs\.?\b",
    # Opinion-seeking
    r"\bis\s+(?:it|this)\s+(?:a\s+)?good\b",
    r"\bis\s+(?:it|this)\s+(?:a\s+)?safe\b",
    r"\bis\s+(?:it|this)\s+(?:a\s+)?risky\b",
    r"\bthe\s+best\b",
    r"\bworst\b",
    r"\bopinion\b",
    r"\badvice\b",
    r"\bsuggest\b",
    # Investment action
    r"\binvest\s+in\b",
    r"\bbuy\b",
    r"\bsell\b",
    r"\bredeem\b.*?\bshould\b",
    r"\bshould\b.*?\bredeem\b",
    r"\bswitch\s+(?:from|to)\b",
    # Future predictions
    r"\bpredict\b",
    r"\bforecast\b",
    r"\boutlook\b",
    r"\bfuture\b.*?\b(?:returns?|performance|growth)\b",
]

_ADVISORY_COMPILED = [re.compile(p, re.IGNORECASE) for p in _ADVISORY_PATTERNS]


# ── Factual Pattern Detection ────────────────────────────────────────────────
# These override advisory classification for queries that are clearly factual
# even if they contain some advisory-sounding words.

_FACTUAL_PATTERNS = [
    r"\bwhat\s+is\s+the\s+(?:expense\s+ratio|exit\s+load|nav|aum|sip|benchmark|risk|rating)\b",
    r"\bexpense\s+ratio\b",
    r"\bexit\s+load\b",
    r"\bsip\s+(?:amount|minimum)\b",
    r"\bminimum\s+(?:sip|investment)\b",
    r"\bfund\s+manager\b",
    r"\bwho\s+(?:is|manages)\b",
    r"\block[- ]?in\s+period\b",
    r"\bbenchmark\b",
    r"\briskometer\b",
    r"\brisk\s+(?:level|category|rating)\b",
    r"\bnav\b",
    r"\baum\b",
    r"\bfund\s+size\b",
    r"\btax\s+(?:implication|benefit)\b",
    r"\bstamp\s+duty\b",
    r"\bcategory\b",
    r"\bsub[- ]?category\b",
    r"\binvestment\s+objective\b",
    r"\bwhat\s+(?:is|are)\b",
    r"\btell\s+me\s+about\b",
    r"\bhow\s+much\b",
]

_FACTUAL_COMPILED = [re.compile(p, re.IGNORECASE) for p in _FACTUAL_PATTERNS]


def detect_pii(query: str) -> Optional[str]:
    """
    Check if the query contains personally identifiable information.

    Args:
        query: The user's raw query string.

    Returns:
        The type of PII detected (e.g., 'pan', 'aadhaar', 'email'),
        or None if no PII is found.
    """
    query_lower = query.lower()

    # Skip PII check if the query contains known false-positive terms
    for term in _PII_FALSE_POSITIVE_TERMS:
        if term in query_lower:
            # Remove the false-positive term before PII scanning
            query = query_lower.replace(term, "")

    for pii_type, pattern in _PII_PATTERNS.items():
        if pattern.search(query):
            logger.warning(f"PII detected in query: type={pii_type}")
            return pii_type

    return None


def classify(query: str) -> str:
    """
    Classify a user query as 'factual', 'advisory', or 'pii_detected'.

    Classification priority:
      1. PII detection (highest priority — always block)
      2. Advisory pattern matching
      3. Factual pattern matching (can override advisory if clearly factual)
      4. Default to 'factual' for ambiguous queries (let retrieval handle it)

    Args:
        query: The user's natural-language question.

    Returns:
        One of: 'factual', 'advisory', 'pii_detected'.
    """
    if not query or not query.strip():
        return "factual"

    query = query.strip()

    # Step 1: PII check (highest priority)
    pii_type = detect_pii(query)
    if pii_type:
        logger.info(f"Query classified as 'pii_detected' (type: {pii_type})")
        return "pii_detected"

    # Step 2: Check for advisory patterns
    has_advisory = any(p.search(query) for p in _ADVISORY_COMPILED)

    # Step 3: Check for factual patterns
    has_factual = any(p.search(query) for p in _FACTUAL_COMPILED)

    # Step 4: Resolve conflicts
    if has_advisory and has_factual:
        # Mixed intent — if the query contains strong advisory signals
        # like "should I", classify as advisory (per edge case QC-08)
        strong_advisory = re.search(
            r"\bshould\s+i\b|\brecommend\b|\bwhich\s+is\s+better\b|\binvest\s+in\b"
            r"|\boutlook\b|\bfuture\b.*?\b(?:returns?|performance|growth)\b"
            r"|\bpredict\b|\bforecast\b"
            r"|\bwhich\s+has\s+(?:a\s+)?(?:lower|higher|better|worse)\b"
            r"|\bcompare\b|\bvs\.?\b",
            query,
            re.IGNORECASE,
        )
        if strong_advisory:
            logger.info(
                "Query has mixed intent with strong advisory signal. "
                "Classified as 'advisory'."
            )
            return "advisory"
        # Weak advisory signal + clear factual signal → factual
        logger.info(
            "Query has mixed intent but factual patterns dominate. "
            "Classified as 'factual'."
        )
        return "factual"

    if has_advisory:
        logger.info("Query classified as 'advisory'.")
        return "advisory"

    # Default: factual (let the retrieval pipeline and LLM handle it)
    logger.info("Query classified as 'factual'.")
    return "factual"
