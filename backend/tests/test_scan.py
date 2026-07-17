import socket

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_health(client):
    # GET /health should report the service is up
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_scan_valid_url(client):
    # POST /api/scan with a normal public URL should succeed and return a scored response
    response = client.post("/api/scan", json={"url": "https://example.com"})
    assert response.status_code == 200
    body = response.get_json()
    assert body["url"] == "https://example.com"
    assert isinstance(body["risk_score"], int)
    assert body["risk_level"] in {"low", "medium", "high"}
    assert isinstance(body["reasons"], list)


def test_scan_missing_url(client):
    # POST /api/scan with no "url" field should be rejected as a bad request
    response = client.post("/api/scan", json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "missing_field"


def test_scan_invalid_url_format(client):
    # POST /api/scan with a string that isn't a valid http/https URL should be rejected
    response = client.post("/api/scan", json={"url": "not-a-url"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid_url"


def test_scan_blocks_localhost(client):
    # POST /api/scan targeting "localhost" should be blocked to prevent SSRF
    response = client.post("/api/scan", json={"url": "http://localhost:5000"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "blocked_host"


def test_scan_blocks_loopback_ip(client):
    # POST /api/scan targeting the loopback IP 127.0.0.1 should be blocked to prevent SSRF
    response = client.post("/api/scan", json={"url": "http://127.0.0.1"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "blocked_host"


def test_scan_blocks_private_ip_via_dns(client, monkeypatch):
    # POST /api/scan targeting a hostname that *resolves* to a private IP should also be
    # blocked, not just literal private IPs typed directly into the URL. DNS is mocked so
    # this test doesn't depend on real network/DNS behavior.
    def fake_getaddrinfo(host, port):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.5", 0))]

    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)
    response = client.post("/api/scan", json={"url": "http://internal.example.com"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "blocked_host"


"""
Future tests to be added:
- url_validator/url_analyzer unit tests in isolation (not just through the /api/scan endpoint)
- additional SSRF cases: IPv6 loopback/link-local, cloud metadata IP (169.254.169.254), .local hostnames
- malformed JSON body (not just missing field)
- non-string "url" values (e.g. a number or list)
- risk scoring edge cases: URL with multiple stacked red flags, score capped at 100
"""
