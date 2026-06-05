"""
FastAPI Routes for Mutual Fund FAQ Assistant.
Exposes endpoints for querying, health checks, and listing schemes.
"""

import time
import logging
from typing import Optional, List, Dict
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.ingestion import run_ingestion

from src.classification.query_classifier import classify
from src.classification.refusal_handler import generate_refusal
from src.retrieval.retriever import retrieve
from src.retrieval.context_builder import build_context
from src.generation.prompt_builder import build_prompt
from src.generation.llm_client import GroqClient
from src.generation.response_formatter import format_response
from src.ingestion.embedder import get_vectorstore
from src.config.settings import CHROMA_COLLECTION_NAME

logger = logging.getLogger(__name__)

router = APIRouter()

# Instantiate LLM client once to reuse
# Ensure GROQ_API_KEY is loaded in environment
llm_client = GroqClient()


# ── Models ───────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    status: str
    type: str  # "factual", "refusal"
    answer: str
    citation: Optional[str] = None
    educational_link: Optional[str] = None
    last_updated: Optional[str] = None


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Main orchestration pipeline for answering mutual fund queries.
    
    Pipeline:
    1. Check PII
    2. Classify (Factual / Advisory)
    3. If Advisory/PII -> Refuse
    4. If Factual -> Retrieve chunks -> Build context -> Generate prompt -> LLM -> Format Response
    """
    start_time = time.time()
    query = request.query
    logger.info(f"Received query: '{query}'")

    if not query.strip():
        return QueryResponse(
            status="success",
            type="factual",
            answer="Please enter a valid question.",
        )

    try:
        # Step 1 & 2: Classify (which includes PII check)
        classification = classify(query)
        logger.info(f"Classification: {classification}")

        # Step 3: Handle Non-Factual (Refusal)
        if classification in ["advisory", "pii_detected"]:
            refusal = generate_refusal(query, classification)
            logger.info(f"Query processed in {time.time() - start_time:.2f}s (Refusal)")
            return QueryResponse(**refusal)

        # Step 4: Handle Factual (RAG Pipeline)
        # a. Retrieve
        chunks = retrieve(query)
        
        # b. Check if we have chunks
        if not chunks:
            from src.generation.response_formatter import _no_info_response
            response_dict = _no_info_response(chunks)
            logger.info(f"Query processed in {time.time() - start_time:.2f}s (No Info)")
            return QueryResponse(**response_dict)

        # c. Build Context
        context = build_context(chunks)

        # d. Build Prompt
        system_prompt, user_prompt = build_prompt(query, context)

        # e. Generate via LLM
        raw_answer = llm_client.generate(system_prompt, user_prompt)

        # f. Format Response
        response_dict = format_response(raw_answer, chunks)
        
        logger.info(f"Query processed in {time.time() - start_time:.2f}s (Factual)")
        return QueryResponse(**response_dict)

    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred while processing your request.")


@router.get("/health")
async def health_check():
    """System health status."""
    try:
        vectorstore = get_vectorstore()
        collection = vectorstore._collection
        count = collection.count() if collection else 0
    except Exception as e:
        logger.error(f"Health check failed to connect to vectorstore: {e}")
        count = "Unavailable"

    return {
        "status": "healthy",
        "vector_store_collection": CHROMA_COLLECTION_NAME,
        "total_chunks_indexed": count
    }


@router.get("/schemes")
async def list_schemes():
    """
    Returns list of all schemes indexed in the vector store.
    We get this by finding all unique scheme names in the metadata.
    """
    try:
        vectorstore = get_vectorstore()
        collection = vectorstore._collection
        if not collection:
            return {"schemes": []}
            
        result = collection.get(include=["metadatas"])
        metadatas = result.get("metadatas", [])
        
        # Extract unique schemes and their URLs
        schemes_dict = {}
        for meta in metadatas:
            if meta:
                name = meta.get("scheme_name")
                url = meta.get("source_url")
                if name and url and name not in schemes_dict:
                    schemes_dict[name] = url
                    
        schemes_list = [{"name": name, "url": url} for name, url in schemes_dict.items()]
        # Sort alphabetically
        schemes_list = sorted(schemes_list, key=lambda x: x["name"])
        
        return {"schemes": schemes_list, "count": len(schemes_list)}
        
    except Exception as e:
        logger.error(f"Failed to list schemes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve schemes")


@router.post("/ingest")
def trigger_ingestion():
    """
    Manually triggers the ingestion pipeline to scrape, clean, chunk, and embed all URLs.
    Warning: This is a synchronous operation that may take several minutes to complete.
    """
    try:
        logger.info("Manual ingestion triggered via API.")
        stats = run_ingestion()
        
        return {
            "status": "success",
            "message": "Ingestion pipeline completed successfully.",
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Manual ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
