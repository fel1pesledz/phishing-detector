import ipaddress
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = ["login", "verify", "secure", "account", "update", "confirm", "signin"]
STANDARD_PORTS = {"http": 80, "https": 443}


def analyze(url):
    """Deterministic, explainable heuristic risk scoring for a URL.

    Returns {"risk_score": int, "risk_level": str, "reasons": [str, ...]}.
    """
    parsed = urlparse(url)
    host = parsed.hostname or ""
    score = 0
    reasons = []

    if _is_ip_literal(host):
        score += 20
        reasons.append("host is an IP address rather than a domain name")

    if "@" in url:
        score += 25
        reasons.append("URL contains '@', which can be used to obscure the real destination")

    subdomain_count = max(host.count("."), 0)
    if subdomain_count >= 3:
        score += 15
        reasons.append(f"host has an unusually high number of subdomains ({subdomain_count})")

    haystack = f"{host}{parsed.path}".lower()
    matched_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in haystack]
    if matched_keywords:
        score += 10 * len(matched_keywords)
        reasons.append(f"suspicious keyword(s) found: {', '.join(matched_keywords)}")

    if parsed.port and parsed.port != STANDARD_PORTS.get(parsed.scheme):
        score += 15
        reasons.append(f"non-standard port used: {parsed.port}")

    if len(url) > 75:
        score += 10
        reasons.append("URL is unusually long")

    score = min(score, 100)
    risk_level = _risk_level(score)

    return {"risk_score": score, "risk_level": risk_level, "reasons": reasons}


def _is_ip_literal(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _risk_level(score):
    if score < 30:
        return "low"
    if score < 60:
        return "medium"
    return "high"
