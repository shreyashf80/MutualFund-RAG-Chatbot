from src.classification.query_classifier import classify

def test_classify_pii():
    assert classify("My PAN is ABCDE1234F") == "pii_detected"
    assert classify("Call me at 9876543210") == "pii_detected"
    assert classify("My folio number is 123456789") == "pii_detected"

def test_classify_advisory():
    assert classify("Should I invest in HDFC fund?") == "advisory"
    assert classify("Which is better, fund A or fund B?") == "advisory"
    assert classify("Is this a good time to buy?") == "advisory"

def test_classify_factual():
    assert classify("What is the expense ratio?") == "factual"
    assert classify("Who is the fund manager for HDFC Top 100?") == "factual"
    assert classify("Tell me the exit load.") == "factual"

def test_classify_ambiguous_defaults_to_factual():
    assert classify("What are mutual funds?") == "factual"
