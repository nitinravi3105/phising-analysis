from analyzer import analyze_message

def test_urgent_credential_message_is_high():
    result = analyze_message("URGENT: verify your password immediately")
    assert result["risk_level"] == "High"
    assert result["risk_score"] >= 45

def test_plain_message_is_low():
    result = analyze_message("The team meeting is at 3 PM tomorrow.")
    assert result["risk_level"] == "Low"
    assert result["risk_score"] == 0

def test_shortened_url_adds_indicator():
    result = analyze_message("Please check https://bit.ly/example")
    assert any("shortener" in x["name"].lower() for x in result["indicators"])

def test_hash_is_sha256_hex():
    result = analyze_message("hello")
    assert len(result["content_hash"]) == 64
    assert all(c in "0123456789abcdef" for c in result["content_hash"])
