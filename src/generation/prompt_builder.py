"""
Prompt Builder for Mutual Fund FAQ Assistant.
Constructs the system and user prompts for the Groq LLM,
injecting retrieved context into a structured template.
"""

import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a facts-only mutual fund FAQ assistant for HDFC mutual fund schemes listed on Groww. You MUST follow these rules strictly:

1. Answer ONLY using information found in the provided context chunks.
2. Keep responses to a MAXIMUM of 3 sentences.
3. Include EXACTLY ONE citation link (the source URL from the chunk metadata).
4. Append a footer: "Last updated from sources: <scrape_date>"
5. NEVER provide investment advice, opinions, or recommendations.
6. NEVER compare fund performance or calculate returns.
7. If the answer is not found in the context, say: "I don't have this information in my current sources."
8. Include fund management data (fund manager name, tenure) when asked."""

USER_PROMPT_TEMPLATE = """Context:
{context}

---

User Question: {query}

Provide a concise, factual answer based ONLY on the context above. Include exactly one source URL and the "Last updated from sources" footer."""


def build_prompt(query: str, context: str) -> tuple[str, str]:
    """
    Build the system and user prompts for the LLM.

    Args:
        query: The user's natural-language question.
        context: The assembled context string from the context builder.

    Returns:
        A tuple of (system_prompt, user_prompt).
    """
    user_prompt = USER_PROMPT_TEMPLATE.format(
        context=context,
        query=query,
    )

    logger.info(
        f"Built prompt. System: {len(SYSTEM_PROMPT)} chars, "
        f"User: {len(user_prompt)} chars"
    )

    return SYSTEM_PROMPT, user_prompt
