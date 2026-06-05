from unittest.mock import patch, MagicMock
from src.retrieval.retriever import retrieve

@patch("src.retrieval.retriever.get_vectorstore")
def test_retrieve_success(mock_get_vectorstore):
    mock_vs = MagicMock()
    
    mock_doc1 = MagicMock()
    mock_doc1.page_content = "HDFC Top 100 has an expense ratio of 1.2%."
    mock_doc1.metadata = {"scheme_name": "HDFC Top 100"}
    
    mock_vs.similarity_search_with_relevance_scores.return_value = [(mock_doc1, 0.85)]
    mock_get_vectorstore.return_value = mock_vs
    
    chunks = retrieve("What is the expense ratio?")
    
    assert len(chunks) == 1
    assert "1.2%" in chunks[0]["page_content"]
    assert chunks[0]["metadata"]["scheme_name"] == "HDFC Top 100"

@patch("src.retrieval.retriever.get_vectorstore")
def test_retrieve_empty(mock_get_vectorstore):
    mock_vs = MagicMock()
    mock_vs.similarity_search_with_relevance_scores.return_value = []
    mock_get_vectorstore.return_value = mock_vs
    
    chunks = retrieve("Random unrelated query")
    assert len(chunks) == 0
