"""
Retriever module for Mutual Fund FAQ Assistant.
Embeds user queries and performs similarity search against ChromaDB
to find the most relevant chunks.
"""

import logging
from typing import List, Dict, Optional

from src.ingestion.embedder import get_vectorstore
from src.config.settings import TOP_K_RESULTS, SIMILARITY_THRESHOLD

logger = logging.getLogger(__name__)

# Approximate token-to-word ratio for truncation
_MAX_QUERY_WORDS = 200


def _truncate_query(query: str) -> str:
    """
    Truncate excessively long queries to ~200 tokens (words).
    Logs a warning if truncation occurs.
    """
    words = query.split()
    if len(words) > _MAX_QUERY_WORDS:
        logger.warning(
            f"Query too long ({len(words)} words). "
            f"Truncating to first {_MAX_QUERY_WORDS} words."
        )
        return " ".join(words[:_MAX_QUERY_WORDS])
    return query


def retrieve(
    query: str,
    top_k: Optional[int] = None,
    threshold: Optional[float] = None,
) -> List[Dict]:
    """
    Embed the user query and perform similarity search against ChromaDB.

    Returns top-K chunks that pass the relevance threshold,
    sorted by descending relevance score.

    Args:
        query: The user's natural-language question.
        top_k: Number of results to retrieve. Defaults to TOP_K_RESULTS (5).
        threshold: Minimum relevance score (0–1). Defaults to SIMILARITY_THRESHOLD (0.3).

    Returns:
        A list of dicts, each containing:
          - page_content (str): The chunk text.
          - metadata (dict): scheme_name, source_url, scrape_date, section, etc.
          - relevance_score (float): Cosine similarity score.
        Returns an empty list if no results pass the threshold or
        the vector store is unavailable.
    """
    if not query or not query.strip():
        logger.warning("Empty query received. Returning no results.")
        return []

    k = top_k if top_k is not None else TOP_K_RESULTS
    min_score = threshold if threshold is not None else SIMILARITY_THRESHOLD

    # Truncate very long queries
    query = _truncate_query(query.strip())

    try:
        vectorstore = get_vectorstore()
    except Exception as e:
        logger.error(f"Failed to load vector store: {e}")
        return []

    try:
        # similarity_search_with_relevance_scores returns List[(Document, float)]
        # where float is the relevance score (higher = more similar)
        results = vectorstore.similarity_search_with_relevance_scores(
            query=query,
            k=k,
        )
    except Exception as e:
        logger.error(f"Similarity search failed: {e}")
        return []

    if not results:
        logger.info("No results returned from vector store.")
        return []

    # Filter by relevance threshold and build output
    filtered = []
    for doc, score in results:
        if score >= min_score:
            filtered.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata,
                "relevance_score": round(score, 4),
            })

    if not filtered:
        logger.info(
            f"All {len(results)} results below threshold ({min_score}). "
            f"Best score: {results[0][1]:.4f}"
        )
    else:
        logger.info(
            f"Retrieved {len(filtered)}/{len(results)} chunks above "
            f"threshold ({min_score}). "
            f"Top score: {filtered[0]['relevance_score']}"
        )

    return filtered
