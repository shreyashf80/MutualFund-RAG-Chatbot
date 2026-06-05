import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def fetch_html(url: str, max_retries: int = 3, timeout: int = 30) -> Optional[str]:
    """Fetch HTML content from a URL with retries and timeout."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to fetch {url} after {max_retries} attempts.")
                return None
    return None

def extract_sections(soup: BeautifulSoup) -> Dict[str, str]:
    """Extract key sections from the parsed HTML using CSS class selectors."""
    import re
    sections = {}
    
    # 1. Scheme Name
    h1 = soup.find("h1")
    if h1:
        sections["scheme_name"] = h1.get_text(strip=True)
        
    # 2. Category, Sub-Category, Risk Pills
    pills_container = soup.find(class_=lambda c: c and "pills_container" in c)
    if pills_container:
        pills = [p.get_text(strip=True) for p in pills_container.find_all(class_=lambda c: c and "pill12Pill" in c)]
        if len(pills) > 0:
            sections["category"] = pills[0]
        if len(pills) > 1:
            sections["sub_category"] = pills[1]
        if len(pills) > 2:
            sections["riskometer"] = pills[2]
            
    # 3. Details Container (NAV, Min SIP, AUM, Expense Ratio, Rating, Lock-in)
    details_container = soup.find(class_=lambda c: c and "fundDetailsContainer" in c)
    if details_container:
        for block in details_container.find_all(recursive=False):
            divs = block.find_all(recursive=False)
            if len(divs) >= 2:
                key = divs[0].get_text(strip=True)
                val = divs[1].get_text(strip=True)
                if "NAV" in key:
                    sections["nav"] = val
                elif "Min. for SIP" in key or "Min SIP" in key:
                    sections["sip_details"] = val
                elif "Fund size" in key or "AUM" in key:
                    sections["aum"] = val
                elif "Expense ratio" in key:
                    sections["expense_ratio"] = val
                elif "Rating" in key:
                    sections["rating"] = val
                elif "Lock-in" in key or "lock-in" in key:
                    sections["lock_in_period"] = val
                    
    # 4. Benchmark Index
    bench_row = soup.find(class_=lambda c: c and "investmentObjective_benchmarkRow" in c)
    if bench_row:
        children = bench_row.find_all(recursive=False)
        if children:
            sections["benchmark"] = children[-1].get_text(strip=True)
            
    # 5. Exit Load, Stamp Duty, Tax details
    tax_container = soup.find(class_=lambda c: c and "exitLoadStampDutyTax_container" in c)
    if tax_container:
        sections_elements = tax_container.find_all(class_=lambda c: c and "exitLoadStampDutyTax_section" in c)
        for sec in sections_elements:
            divs = sec.find_all(recursive=False)
            if len(divs) >= 2:
                key = divs[0].get_text(strip=True)
                val = divs[1].get_text(separator=" ", strip=True)
                val = re.sub(r'\s+', ' ', val).strip()
                if "Exit load" in key:
                    sections["exit_load"] = val
                elif "Tax implication" in key:
                    sections["tax_implication"] = val
                elif "Stamp duty" in key:
                    sections["stamp_duty"] = val
                    
    # 6. Fund Managers
    managers = []
    accordions = soup.find_all(class_=lambda c: c and any(x.startswith("fundManagement_accordion__") for x in c.split()))
    for acc in accordions:
        name_tag = acc.find(class_=lambda c: c and "fundManagement_personName" in c)
        if name_tag:
            mgr_name = name_tag.get_text(strip=True)
            tenure = ""
            card_text_div = name_tag.parent
            if card_text_div:
                tenure_div = card_text_div.find(class_=lambda c: c and "bodyLarge" in c)
                if tenure_div:
                    tenure = tenure_div.get_text(strip=True)
            managers.append(f"{mgr_name} ({tenure})")
            
    if managers:
        sections["fund_manager"] = ", ".join(managers)
        
    return sections

def scrape_url(url: str) -> Dict[str, Any]:
    """
    Scrape a Groww mutual fund URL.
    Returns structured data with source URL, scrape timestamp, and raw HTML.
    """
    html = fetch_html(url)
    timestamp = datetime.utcnow().isoformat()
    
    result = {
        "source_url": url,
        "scrape_date": timestamp,
        "raw_html": html or "",
        "extracted_sections": {}
    }
    
    if html:
        soup = BeautifulSoup(html, "html.parser")
        result["extracted_sections"] = extract_sections(soup)
        
    return result
