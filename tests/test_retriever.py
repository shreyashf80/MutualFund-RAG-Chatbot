from unittest.mock import patch, MagicMock
from src.retrieval.retriever import retrieve

@patch("src.retrieval.retriever.get_vectorstore")
def test_retrieve_success(mock_get_vectorstore):
    mock_vs = MagicMock()
    
    mock_doc1 = MagicMock()
    mock_doc1.page_content = "HDFC Top 100 has an expense ratio of 1.2%."
    mock_doc1.metadata = {"scheme_name": "HDFC Top 100"}
    
    # similarity_search_with_score returns (doc, distance) pairs.
    # The relevance_fn converts distance to a 0-1 score.
    mock_vs.similarity_search_with_score.return_value = [(mock_doc1, 0.15)]
    # Mock the relevance score function (identity for simplicity → score = 0.85)
    mock_vs._select_relevance_score_fn.return_value = lambda d: 1.0 - d
    mock_get_vectorstore.return_value = mock_vs
    
    chunks = retrieve("What is the expense ratio?")
    
    assert len(chunks) == 1
    assert "1.2%" in chunks[0]["page_content"]
    assert chunks[0]["metadata"]["scheme_name"] == "HDFC Top 100"

@patch("src.retrieval.retriever.get_vectorstore")
def test_retrieve_empty(mock_get_vectorstore):
    mock_vs = MagicMock()
    mock_vs.similarity_search_with_score.return_value = []
    mock_vs._select_relevance_score_fn.return_value = lambda d: 1.0 - d
    mock_get_vectorstore.return_value = mock_vs
    
    chunks = retrieve("Random unrelated query")
    assert len(chunks) == 0

@patch("src.retrieval.retriever.get_vectorstore")
def test_retrieve_with_scheme_name(mock_get_vectorstore):
    """When scheme_name is provided, the filter should be passed and query rewritten."""
    mock_vs = MagicMock()
    
    mock_doc1 = MagicMock()
    mock_doc1.page_content = "NAV of HDFC Gold ETF FoF is ₹20.50."
    mock_doc1.metadata = {"scheme_name": "HDFC Gold ETF Fund Of Fund Direct Plan Growth"}
    
    mock_vs.similarity_search_with_score.return_value = [(mock_doc1, 0.10)]
    mock_vs._select_relevance_score_fn.return_value = lambda d: 1.0 - d
    mock_get_vectorstore.return_value = mock_vs
    
    chunks = retrieve("what is nav", scheme_name="HDFC Gold ETF Fund Of Fund Direct Plan Growth")
    
    assert len(chunks) == 1
    assert "HDFC Gold ETF" in chunks[0]["page_content"]
    
    # Verify the filter was passed to similarity_search_with_score
    call_kwargs = mock_vs.similarity_search_with_score.call_args
    assert call_kwargs.kwargs.get("filter") == {"scheme_name": {"$eq": "HDFC Gold ETF Fund Of Fund Direct Plan Growth"}}
    # Verify query was rewritten to include the scheme name
    assert "HDFC Gold ETF Fund Of Fund Direct Plan Growth" in call_kwargs.kwargs.get("query", call_kwargs.args[0] if call_kwargs.args else "")

