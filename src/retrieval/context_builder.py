"""
Context Builder for Mutual Fund FAQ Assistant.
Assembles retrieved chunks into a structured context string
ready for injection into the LLM prompt.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def build_context(chunks: List[Dict]) -> str:
    """
    Assemble retrieved chunks into a structured context string for the LLM.

    Each chunk is formatted as a labeled block with its metadata
    (scheme name, section, source URL) so the LLM can attribute answers
    and produce citations.

    Args:
        chunks: List of chunk dicts from the retriever, each containing
                'page_content', 'metadata', and 'relevance_score'.

    Returns:
        A formatted context string. Returns an empty string if no chunks
        are provided.
    """
    if not chunks:
        return ""

    # De-duplicate by chunk_id (same chunk could theoretically appear twice)
    seen_ids = set()
    unique_chunks = []
    for chunk in chunks:
        chunk_id = chunk.get("metadata", {}).get("chunk_id", "")
        if chunk_id and chunk_id in seen_ids:
            logger.debug(f"De-duplicated chunk: {chunk_id}")
            continue
        seen_ids.add(chunk_id)
        unique_chunks.append(chunk)

    context_blocks = []
    for i, chunk in enumerate(unique_chunks, 1):
        metadata = chunk.get("metadata", {})
        scheme_name = metadata.get("scheme_name", "Unknown Scheme")
        section = metadata.get("section", "Unknown Section")
        source_url = metadata.get("source_url", "")
        scrape_date = metadata.get("scrape_date", "Unknown")
        content = chunk.get("page_content", "")

        block = (
            f"[Chunk {i}]\n"
            f"Scheme: {scheme_name}\n"
            f"Section: {section}\n"
            f"Source: {source_url}\n"
            f"Last Scraped: {scrape_date}\n"
            f"Content:\n{content}"
        )
        context_blocks.append(block)

    context = "\n\n---\n\n".join(context_blocks)

    logger.info(
        f"Built context from {len(unique_chunks)} chunks "
        f"({len(context)} chars)"
    )

    return context
