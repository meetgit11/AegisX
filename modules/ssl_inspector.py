"""TLS certificate inspection for authorized HTTPS endpoints."""

from __future__ import annotations

import socket
import ssl
from datetime import datetime, timezone
from typing import Any, Dict

from core.models import Finding, TLSInspection


def _name(subject: Any) -> str:
    """Flatten a certificate subject/issuer tuple into readable text."""

    parts = []
    for group in subject or ():
        for key, value in group:
            parts.append(f"{key}={value}")
    return ", ".join(parts)


def _cert_date(value: str) -> datetime:
    return datetime.strptime(value, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)


def inspect_tls(host: str, port: int = 443, timeout: float = 5.0) -> TLSInspection:
    """Inspect a TLS handshake and certificate without sending application payloads."""

    context = ssl.create_default_context()
    verified = True
    verification_error = ""
    try:
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with context.wrap_socket(raw, server_hostname=host) as tls_socket:
                cert: Dict[str, Any] = tls_socket.getpeercert()
                valid_from = _cert_date(cert["notBefore"])
                valid_to = _cert_date(cert["notAfter"])
                days_remaining = (valid_to - datetime.now(timezone.utc)).days
                findings = []
                if days_remaining < 0:
                    findings.append(Finding("tls", "critical", "TLS certificate expired", "The presented certificate is past its validity period.", "Users may receive browser warnings and cannot rely on certificate freshness.", "Renew the certificate and deploy the complete trusted chain.", cert.get("notAfter", ""), "TLS-CERT-EXPIRED"))
                elif days_remaining <= 30:
                    findings.append(Finding("tls", "high", "TLS certificate expires soon", "The certificate expires within 30 days.", "An avoidable expiry can cause outages and user trust failures.", "Renew and deploy the certificate before the expiry window closes.", cert.get("notAfter", ""), "TLS-CERT-NEAR-EXPIRY"))
                if tls_socket.version() in {"TLSv1", "TLSv1.1", "SSLv3"}:
                    findings.append(Finding("tls", "high", "Legacy TLS protocol negotiated", "The connection negotiated an obsolete protocol version.", "Legacy protocols provide weaker cryptographic protections.", "Disable legacy protocols and require TLS 1.2 or newer.", tls_socket.version() or "", "TLS-LEGACY-PROTOCOL"))
                return TLSInspection(host, port, True, _name(cert.get("subject")), _name(cert.get("issuer")), str(cert.get("serialNumber", "")), valid_from.isoformat(), valid_to.isoformat(), days_remaining, tls_socket.version() or "", str(tls_socket.cipher() or ""), True, "", findings)
    except ssl.SSLCertVerificationError as exc:
        verified = False
        verification_error = str(exc)
    except (ssl.SSLError, OSError, ValueError) as exc:
        verification_error = str(exc)

    findings = [Finding("tls", "high" if not verified else "medium", "TLS inspection failed", "The certificate could not be verified or the TLS handshake failed.", "The assessment could not establish a trusted encrypted connection.", "Verify the endpoint, certificate chain, hostname coverage, and supported TLS versions.", verification_error, "TLS-HANDSHAKE-FAILURE")]
    return TLSInspection(host, port, False, certificate_valid=verified, verification_error=verification_error, findings=findings, error=verification_error)
