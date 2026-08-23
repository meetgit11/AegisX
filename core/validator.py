"""Target validation and normalization for authorized defensive assessments."""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse

from core.models import ValidatedTarget

_DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}$|^localhost$",
    re.IGNORECASE,
)
_SUSPICIOUS_CHARS = re.compile(r"[\s;|&`$<>\\\n\r\t]")


class TargetValidationError(ValueError):
    """Raised when a target is malformed or contains unsafe input."""


def validate_target(value: str) -> ValidatedTarget:
    """Validate and normalize a domain, IP address, or HTTP(S) URL.

    The function intentionally rejects shell metacharacters and unsupported URL
    schemes. It never resolves or probes the target, making it safe to call from
    the UI before a scan begins.
    """

    if not isinstance(value, str):
        raise TargetValidationError("Target must be text.")
    raw = value.strip()
    if not raw or len(raw) > 253 or _SUSPICIOUS_CHARS.search(raw):
        raise TargetValidationError("Enter a valid domain name or IP address.")

    candidate = raw
    scheme = None
    port = None
    if "://" in raw:
        parsed = urlparse(raw)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            raise TargetValidationError("Only HTTP and HTTPS URLs are supported.")
        if parsed.username or parsed.password or parsed.path not in {"", "/"}:
            raise TargetValidationError("Provide only a hostname or a simple HTTP(S) URL.")
        candidate = parsed.hostname
        scheme = parsed.scheme.lower()
        port = parsed.port
    else:
        # A bracketed IPv6 address is accepted, while arbitrary host:port input
        # is not, keeping the public input surface intentionally small.
        candidate = raw[1:-1] if raw.startswith("[") and raw.endswith("]") else raw

    try:
        ip = ipaddress.ip_address(candidate)
        return ValidatedTarget(raw, candidate, "ipv4" if ip.version == 4 else "ipv6", scheme, port)
    except ValueError:
        pass

    if not _DOMAIN_RE.fullmatch(candidate.rstrip(".")):
        raise TargetValidationError("Enter a valid domain name or IP address.")
    return ValidatedTarget(raw, candidate.rstrip("."), "domain", scheme, port)


def sanitize_target(value: str) -> str:
    """Return the canonical hostname or raise :class:`TargetValidationError`."""

    return validate_target(value).host


def is_valid_target(value: str) -> bool:
    """Return whether *value* passes :func:`validate_target`."""

    try:
        validate_target(value)
    except TargetValidationError:
        return False
    return True
