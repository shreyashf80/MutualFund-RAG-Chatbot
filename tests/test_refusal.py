from src.classification.refusal_handler import generate_refusal

def test_generate_refusal_advisory():
    result = generate_refusal("Should I buy this fund?", "advisory")
    assert result["status"] == "success"
    assert result["type"] == "refusal"
    assert "investment advice" in result["answer"].lower()
    assert result["educational_link"] is not None

def test_generate_refusal_pii():
    result = generate_refusal("My PAN is ABCDE1234F", "pii_detected")
    assert result["status"] == "success"
    assert result["type"] == "refusal"
    assert "personal information" in result["answer"].lower()
