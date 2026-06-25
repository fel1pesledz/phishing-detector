import ipaddress
import socket
from urllib.parse import urlparse

ALLOWED_SCHEMES = {"http", "https"}


def validate(url):
    """Validate URL format and block SSRF-prone targets.

    Returns (is_valid, error_code, message).
    """
    if not isinstance(url, str) or not url.strip():
        return False, "invalid_url", "URL must be a non-empty string"

    parsed = urlparse(url)

    if parsed.scheme not in ALLOWED_SCHEMES:
        return False, "invalid_url", "URL must use http or https"

    hostname = parsed.hostname
    if not hostname:
        return False, "invalid_url", "URL must include a hostname"

    if hostname == "localhost" or hostname.endswith(".local"):
        return False, "blocked_host", "URL host is not allowed: localhost/internal hostname"

    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False, "invalid_url", "URL host could not be resolved"

    for info in addr_infos:
        ip_str = info[4][0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            continue
        if (
            ip.is_loopback
            or ip.is_private
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_unspecified
            or ip.is_multicast
        ):
            return False, "blocked_host", "URL host resolves to a private/internal address and cannot be scanned"

    return True, None, None
