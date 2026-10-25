"""Transparent, rule-based phishing indicator analyzer. Not a definitive classifier."""
import hashlib
import re
from urllib.parse import urlparse

URGENT_TERMS = [
    "urgent", "immediately", "act now", "within 24 hours", "account suspended",
    "verify now", "limited time", "final warning", "expires today"
]
CREDENTIAL_TERMS = [
    "password", "otp", "one-time password", "pin", "login", "log in",
    "bank details", "credit card", "social security"
]
PAYMENT_TERMS = ["payment failed", "pay now", "refund", "prize", "won", "claim reward", "fee"]
LINK_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly"}
URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>'\"]+", re.IGNORECASE)

def analyze_message(message: str, message_type: str = "Message") -> dict:
    text = message.strip()
    lowered = text.lower()
    indicators = []
    score = 0

    if any(term in lowered for term in URGENT_TERMS):
        indicators.append({
            "name": "Urgency or pressure language",
            "detail": "The message uses urgent or pressure-based wording.",
            "points": 25
        })
        score += 25
    if any(term in lowered for term in CREDENTIAL_TERMS):
        indicators.append({"name": "Credential or sensitive-data request", "detail": "The message mentions credentials or sensitive information.", "points": 25})
        score += 25
    if any(term in lowered for term in PAYMENT_TERMS):
        indicators.append({"name": "Payment, prize, or reward language", "detail": "The message mentions a payment, prize, or reward.", "points": 15})
        score += 15

    urls = URL_RE.findall(text)
    for raw_url in urls:
        cleaned = raw_url.rstrip(".,);!?]")
        candidate = cleaned if cleaned.lower().startswith(("http://", "https://")) else "http://" + cleaned
        host = (urlparse(candidate).hostname or "").lower()
        if host in LINK_SHORTENERS:
            indicators.append({"name": "URL shortener detected", "detail": f"The link uses a shortening service ({host}). Inspect the destination safely.", "points": 20})
            score += 20
        if host and (host.replace(".", "").isdigit() or re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host)):
            indicators.append({"name": "IP-address URL", "detail": "The link appears to use an IP address instead of a domain name.", "points": 20})
            score += 20
        if "@" in cleaned:
            indicators.append({"name": "URL contains an @ symbol", "detail": "An @ symbol in a URL can obscure the destination.", "points": 15})
            score += 15
        if host and host.startswith("xn--"):
            indicators.append({"name": "Internationalized domain pattern", "detail": "The domain uses an encoded internationalized-name prefix; verify it carefully.", "points": 15})
            score += 15

    # Cap score so repeated indicators cannot exceed 100.
    score = min(score, 100)
    if score >= 50:
        level = "High"
    elif score >= 25:
        level = "Medium"
    else:
        level = "Low"

    if not indicators:
        indicators.append({"name": "No configured indicators found", "detail": "The rules did not find the patterns configured in this demo. This does not prove the message is safe.", "points": 0})
    summary = {
        "High": "Several warning signs were detected. Treat the message cautiously and verify it through an independent trusted channel.",
        "Medium": "One or more warning signs were detected. Check the sender and destination independently before taking action.",
        "Low": "Few configured warning signs were detected. This result does not guarantee that the message is legitimate."
    }[level]

    return {
        "risk_score": score,
        "risk_level": level,
        "indicators": indicators,
        "summary": summary,
        "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "message_type": message_type,
    }
