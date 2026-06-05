"""
Refusal Handler for Mutual Fund FAQ Assistant.
Generates polite, structured refusal responses for advisory queries
and privacy-focused refusals for PII-containing queries.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Educational link for investment guidance
_EDUCATIONAL_LINK = "https://www.amfiindia.com/investor-corner/knowledge-center"

# Refusal message templates
_ADVISORY_REFUSAL = (
    "I can only provide factual information about mutual fund schemes. "
    "I'm unable to offer investment advice or recommendations."
)

_PII_REFUSAL = (
    "I don't collect or process personal data such as PAN numbers, "
    "Aadhaar, phone numbers, or email addresses. "
    "Please do not share any personal information here."
)

_OFF_TOPIC_REFUSAL = (
    "I can only answer factual questions about HDFC mutual fund schemes "
    "listed on Groww."
)


def generate_refusal(query: str, classification: str = "advisory") -> Dict:
    """
    Generate a polite refusal response based on the classification type.

    Args:
        query: The original user query (for logging purposes).
        classification: The classification result — either 'advisory'
                       or 'pii_detected'.

    Returns:
        A structured response dict matching the API response format:
        {
            "status": "success",
            "type": "refusal",
            "answer": "...",
            "educational_link": "https://...",
            "last_updated": null
        }
    """
    if classification == "pii_detected":
        answer = _PII_REFUSAL
        logger.info(f"Generated PII refusal for query: '{query[:50]}...'")
    else:
        answer = _ADVISORY_REFUSAL
        logger.info(f"Generated advisory refusal for query: '{query[:50]}...'")

    return {
        "status": "success",
        "type": "refusal",
        "answer": answer,
        "educational_link": _EDUCATIONAL_LINK,
        "last_updated": None,
    }
