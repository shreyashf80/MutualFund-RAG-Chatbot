"""Data ingestion pipeline — scraper, cleaner, chunker, embedder, scheduler."""

import os
import json
import logging
import time
from src.config.urls import get_all_schemes
from src.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR, ensure_data_dirs
from src.ingestion.scraper import scrape_url
from src.ingestion.cleaner import clean_text
from src.ingestion.chunker import chunk_text
from src.ingestion.embedder import rebuild_index

logger = logging.getLogger(__name__)

def run_ingestion():
    """
    Orchestrates the full data ingestion pipeline:
    1. Scrape all URLs
    2. Clean raw content
    3. Chunk text semantically
    4. Generate embeddings and store in ChromaDB
    """
    logger.info("Starting data ingestion pipeline...")
    start_time = time.time()
    ensure_data_dirs()
    
    schemes = get_all_schemes()
    all_chunks = []
    successful_scrapes = 0
    
    for scheme in schemes:
        url = scheme["url"]
        scheme_name = scheme["scheme_name"]
        logger.info(f"Processing: {scheme_name}")
        
        # 1. Scrape
        result = scrape_url(url)
        if not result or not result.get("raw_html"):
            logger.error(f"Failed to scrape {url}")
            continue
            
        base_id = scheme_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        raw_path = RAW_DATA_DIR / f"{base_id}.html"
        
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(result["raw_html"])
            
        successful_scrapes += 1
            
        # 2. Clean
        cleaned_text, facts = clean_text(result["raw_html"])
        if not cleaned_text:
            logger.error(f"Failed to clean {url}")
            continue
            
        txt_path = PROCESSED_DATA_DIR / f"{base_id}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
            
        # Metadata and structured data
        metadata = {
            "scheme_name": scheme_name,
            "source_url": result["source_url"],
            "scrape_date": result["scrape_date"]
        }
        
        json_data = {
            "metadata": metadata,
            "extracted_sections": facts
        }
        json_path = PROCESSED_DATA_DIR / f"{base_id}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
            
        # 3. Chunk
        chunks = chunk_text(cleaned_text, metadata)
        all_chunks.extend(chunks)
        
        chunks_json_path = PROCESSED_DATA_DIR / f"{base_id}_chunks.json"
        with open(chunks_json_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
    # 4 & 5. Embed and Index
    if all_chunks:
        logger.info(f"Rebuilding index with {len(all_chunks)} total chunks...")
        rebuild_index(all_chunks)
        logger.info("Ingestion pipeline completed successfully.")
    else:
        logger.warning("No chunks generated. Index will not be rebuilt.")
        
    time_taken = time.time() - start_time
    return {
        "urls_scraped": successful_scrapes,
        "chunks_created": len(all_chunks),
        "time_taken_seconds": round(time_taken, 2)
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_ingestion()
