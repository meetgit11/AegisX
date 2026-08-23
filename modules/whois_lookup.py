"""WHOIS metadata lookup with safe normalization and failure isolation."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict

try:
    import whois
except ImportError:  # pragma: no cover - optional dependency fallback
    whois = None


def _serializable(value: Any) -> Any:
    """Convert common WHOIS values to JSON-friendly values."""

    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, (list, tuple, set)):
        return [_serializable(item) for item in value]
    return value


def lookup_whois(host: str) -> tuple[Dict[str, Any], str]:
    """Return selected WHOIS fields and a non-fatal error string if needed."""

    if whois is None:
        return {}, "python-whois is not installed"
    try:
        record = whois.whois(host)
        fields = {}
        for key in ("registrar", "creation_date", "expiration_date", "org", "name", "emails", "name_servers", "status"):
            value = getattr(record, key, None)
            if value not in (None, "", []):
                fields[key] = _serializable(value)
        return fields, ""
    except Exception as exc:  # WHOIS libraries expose provider-specific exceptions
        return {}, f"WHOIS unavailable: {exc.__class__.__name__}"
