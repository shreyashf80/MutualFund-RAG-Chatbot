from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the FastAPI app
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@patch("src.api.routes.classify")
def test_query_endpoint_refusal(mock_classify):
    # Mock classification to return advisory
    mock_classify.return_value = "advisory"
    
    response = client.post("/api/query", json={"query": "Should I invest?"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "refusal"
    assert "investment advice" in data["answer"].lower()

@patch("src.api.routes.classify")
@patch("src.api.routes.retrieve")
@patch("src.api.routes.llm_client")
def test_query_endpoint_factual(mock_llm, mock_retrieve, mock_classify):
    # Mock the full RAG pipeline
    mock_classify.return_value = "factual"
    
    mock_retrieve.return_value = [
        {"text": "Expense ratio is 1%.", "metadata": {"source_url": "http://test.com"}}
    ]
    
    mock_llm.generate.return_value = "The expense ratio is 1%."
    
    response = client.post("/api/query", json={"query": "What is the expense ratio?"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "factual"
    assert data["answer"] == "The expense ratio is 1%."
    assert data["citation"] == "http://test.com"

@patch("src.api.routes.run_ingestion")
def test_manual_ingest_trigger(mock_run_ingestion):
    # Mock the ingestion script
    mock_run_ingestion.return_value = {
        "urls_scraped": 19,
        "chunks_created": 150,
        "time_taken_seconds": 12.5
    }
    
    response = client.post("/api/ingest")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["stats"]["urls_scraped"] == 19
