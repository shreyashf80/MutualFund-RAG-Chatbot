"""
Semantic/Structural Chunker for Mutual Fund FAQ Assistant.
Breaks down cleaned structured text into distinct, logical sections
while preserving scheme-level metadata.
"""

import json
from typing import List, Dict

def chunk_text(text: str, base_metadata: dict) -> List[Dict]:
    """
    Splits the structured text into semantic chunks and attaches rich metadata.
    
    Args:
        text (str): The cleaned text content of a mutual fund scheme.
        base_metadata (dict): Metadata (scheme_name, source_url, scrape_date).
        
    Returns:
        List[Dict]: A list of chunks, where each chunk is a dictionary with
                    'page_content' and 'metadata'.
    """
    chunks = []
    lines = text.split('\n')
    
    current_section = "Key Metrics & Overview"
    
    sections = {
        "Key Metrics & Overview": [],
        "Investment Objective": [],
        "Exit Load & Tax Implications": [],
        "Fund Managers": []
    }
    
    section_keys = {
        "Investment Objective:": "Investment Objective",
        "Exit Load & Tax Implications:": "Exit Load & Tax Implications",
        "Fund Managers:": "Fund Managers"
    }
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        if stripped in section_keys:
            current_section = section_keys[stripped]
            continue
            
        if current_section in sections:
            sections[current_section].append(line)
        
    scheme_name = base_metadata.get("scheme_name", "Unknown Scheme")
    base_id = scheme_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
    
    # Chunk 1: Key Metrics & Overview
    if sections["Key Metrics & Overview"]:
        content = "\n".join(sections["Key Metrics & Overview"]).strip()
        if not content.startswith("Scheme Name:"):
            content = f"Scheme Name: {scheme_name}\n" + content
        chunk = {
            "page_content": content,
            "metadata": {
                **base_metadata,
                "chunk_id": f"{base_id}-metrics",
                "section": "Key Metrics & Overview"
            }
        }
        chunks.append(chunk)
        
    # Chunk 2: Investment Objective
    if sections["Investment Objective"]:
        content = "\n".join(sections["Investment Objective"]).strip()
        chunk = {
            "page_content": f"Scheme Name: {scheme_name}\n" + content,
            "metadata": {
                **base_metadata,
                "chunk_id": f"{base_id}-objective",
                "section": "Investment Objective"
            }
        }
        chunks.append(chunk)
        
    # Chunk 3: Exit Load & Tax Implications
    if sections["Exit Load & Tax Implications"]:
        content = "\n".join(sections["Exit Load & Tax Implications"]).strip()
        chunk = {
            "page_content": f"Scheme Name: {scheme_name}\n" + content,
            "metadata": {
                **base_metadata,
                "chunk_id": f"{base_id}-exit-load",
                "section": "Exit Load & Tax Implications"
            }
        }
        chunks.append(chunk)
        
    # Chunk 4+: Fund Managers (Split by manager)
    manager_lines = sections["Fund Managers"]
    current_manager = []
    manager_count = 1
    
    # Manager lines usually start with "1. Name...", "2. Name..."
    for line in manager_lines:
        stripped_line = line.strip()
        if stripped_line and stripped_line[0].isdigit() and stripped_line[1:3] in [". ", ".\t"]:
            if current_manager:
                content = "\n".join(current_manager).strip()
                chunk = {
                    "page_content": f"Scheme Name: {scheme_name}\n" + content,
                    "metadata": {
                        **base_metadata,
                        "chunk_id": f"{base_id}-manager-{manager_count}",
                        "section": "Fund Managers"
                    }
                }
                chunks.append(chunk)
                manager_count += 1
            current_manager = [line]
        else:
            if current_manager:
                current_manager.append(line)
                
    if current_manager:
        content = "\n".join(current_manager).strip()
        chunk = {
            "page_content": f"Scheme Name: {scheme_name}\n" + content,
            "metadata": {
                **base_metadata,
                "chunk_id": f"{base_id}-manager-{manager_count}",
                "section": "Fund Managers"
            }
        }
        chunks.append(chunk)
        
    # Add index and total to metadata
    total_chunks = len(chunks)
    for i, chunk in enumerate(chunks):
        chunk["metadata"]["chunk_index"] = i + 1
        chunk["metadata"]["total_chunks"] = total_chunks
        
    return chunks

def process_file_to_chunks(txt_path: str, json_path: str) -> List[Dict]:
    """Helper to process a pair of .txt and .json files into chunks."""
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    with open(json_path, 'r', encoding='utf-8') as f:
        base_metadata = json.load(f)
        
    return chunk_text(text, base_metadata)
