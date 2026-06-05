import pytest
from unittest.mock import patch, MagicMock
import requests
from src.ingestion.scraper import scrape_url

def test_scrape_url_success():
    with patch("src.ingestion.scraper.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Groww Fund</h1></body></html>"
        mock_get.return_value = mock_response
        
        result = scrape_url("https://groww.in/mutual-funds/test-fund")
        
        assert result is not None
        assert result["source_url"] == "https://groww.in/mutual-funds/test-fund"
        assert "<h1>Groww Fund</h1>" in result["raw_html"]
        assert "scrape_date" in result

def test_scrape_url_failure():
    with patch("src.ingestion.scraper.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Not Found")
        mock_get.return_value = mock_response
        
        result = scrape_url("https://groww.in/mutual-funds/not-found")
        assert result is not None
        assert result["raw_html"] == ""
