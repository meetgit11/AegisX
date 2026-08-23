"""DNS record collection with per-record-type graceful failures."""

from __future__ import annotations

from typing import Dict, List

import dns.resolver


def resolve_dns(host: str, timeout: float = 3.0) -> tuple[Dict[str, List[str]], List[str]]:
    """Resolve common DNS record types and return records plus non-fatal errors."""

    records: Dict[str, List[str]] = {}
    errors: List[str] = []
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    for record_type in ("A", "AAAA", "MX", "NS", "TXT", "CNAME"):
        try:
            answers = resolver.resolve(host, record_type)
            values = []
            for answer in answers:
                if record_type == "MX":
                    values.append(f"{answer.preference} {answer.exchange.to_text()}")
                elif record_type == "TXT":
                    values.append("".join(part.decode(errors="replace") if isinstance(part, bytes) else str(part) for part in answer.strings))
                else:
                    values.append(answer.to_text().rstrip("."))
            records[record_type] = values
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout, ValueError) as exc:
            errors.append(f"{record_type}: {exc.__class__.__name__}")
    return records, errors
