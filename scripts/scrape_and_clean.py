#!/usr/bin/env python3
"""
Script to scrape HDFC mutual fund URLs from Groww, clean the HTML content,
and save both the raw HTML and cleaned text data to the local filesystem.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR, ensure_data_dirs
from src.config.urls import SCHEME_URLS
from src.ingestion.scraper import scrape_url
from src.ingestion.cleaner import clean_text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def slugify(url: str) -> str:
    """Create a filename-safe slug from the scheme URL."""
    return url.split("/")[-1].strip()

def main():
    logger.info("Starting scrape and clean process...")
    
    # Ensure data directories exist
    ensure_data_dirs()
    logger.info(f"Data directories verified: Raw: {RAW_DATA_DIR}, Processed: {PROCESSED_DATA_DIR}")
    
    success_count = 0
    failure_count = 0
    
    for name, url in SCHEME_URLS.items():
        slug = slugify(url)
        logger.info(f"Processing '{name}'...")
        
        try:
            # 1. Scrape the URL
            scraped_data = scrape_url(url)
            raw_html = scraped_data.get("raw_html", "")
            
            if not raw_html:
                logger.error(f"Failed to scrape content for {name} (empty HTML).")
                failure_count += 1
                continue
                
            # 2. Save Raw HTML
            raw_file_path = RAW_DATA_DIR / f"{slug}.html"
            with open(raw_file_path, "w", encoding="utf-8") as f:
                f.write(raw_html)
            logger.info(f"  Saved raw HTML to {raw_file_path.name}")
            
            # 3. Clean Text
            cleaned_text = clean_text(raw_html)
            
            # 4. Save Cleaned Text
            processed_txt_path = PROCESSED_DATA_DIR / f"{slug}.txt"
            with open(processed_txt_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            logger.info(f"  Saved cleaned text to {processed_txt_path.name}")
            
            # 5. Save structured JSON metadata (extremely useful for downstream chunker)
            processed_json_path = PROCESSED_DATA_DIR / f"{slug}.json"
            processed_data = {
                "scheme_name": name,
                "source_url": url,
                "scrape_date": scraped_data.get("scrape_date"),
                "extracted_sections": scraped_data.get("extracted_sections", {}),
                "cleaned_text": cleaned_text
            }
            with open(processed_json_path, "w", encoding="utf-8") as f:
                json.dump(processed_data, f, indent=2, ensure_ascii=False)
            logger.info(f"  Saved metadata JSON to {processed_json_path.name}")
            
            success_count += 1
            
            # Sleep 1.5 seconds between requests to be polite and avoid rate limits
            time.sleep(1.5)
            
        except Exception as e:
            logger.error(f"Error processing {name} ({url}): {e}", exc_info=True)
            failure_count += 1
            
    logger.info("Scrape and clean process completed.")
    logger.info(f"Successfully processed: {success_count}/{len(SCHEME_URLS)}")
    if failure_count > 0:
        logger.warning(f"Failed to process: {failure_count}/{len(SCHEME_URLS)}")

if __name__ == "__main__":
    main()
