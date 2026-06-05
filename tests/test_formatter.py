from src.generation.response_formatter import format_response, _no_info_response

def test_format_response_with_chunks():
    raw_answer = "The expense ratio is 1.5%."
    chunks = [
        {
            "text": "The expense ratio is 1.5%.",
            "metadata": {
                "source_url": "https://test.com",
                "scrape_date": "2023-10-01"
            }
        }
    ]
    
    result = format_response(raw_answer, chunks)
    
    assert result["status"] == "success"
    assert result["type"] == "factual"
    assert result["answer"] == raw_answer
    assert result["citation"] == "https://test.com"
    assert result["last_updated"] == "2023-10-01"

def test_no_info_response():
    result = _no_info_response([])
    assert result["status"] == "success"
    assert result["type"] == "factual"
    assert "don't have this information" in result["answer"]
