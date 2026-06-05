from src.ingestion.chunker import chunk_text

def test_chunk_text_basic():
    text = """
    This is some general overview text.
    
    Investment Objective:
    This fund aims to generate long term capital appreciation.
    
    Exit Load & Tax Implications:
    1% exit load for 1 year.
    
    Fund Managers:
    1. John Doe
    Manages the fund.
    2. Jane Smith
    Also manages the fund.
    """
    
    metadata = {"scheme_name": "Test Fund", "source_url": "https://test.com"}
    chunks = chunk_text(text, metadata)
    
    assert len(chunks) == 5, f"Expected 5 chunks, got {len(chunks)}"
    
    sections_found = [c["metadata"]["section"] for c in chunks]
    assert "Key Metrics & Overview" in sections_found
    assert "Investment Objective" in sections_found
    assert "Exit Load & Tax Implications" in sections_found
    assert sections_found.count("Fund Managers") == 2

def test_chunk_text_empty():
    chunks = chunk_text("", {})
    assert len(chunks) == 0
