"""HTTP security header assessment module."""

from __future__ import annotations

from typing import Dict
from urllib.parse import urlparse

import requests

from core.models import Finding, HeaderAudit

HEADER_RULES = {
    "Content-Security-Policy": ("high", "Controls which resources a browser may load.", "Add a restrictive, tested CSP appropriate for the application."),
    "Strict-Transport-Security": ("high", "Prevents downgrade attacks after HTTPS is established.", "Serve HTTPS consistently and add HSTS with an appropriate max-age."),
    "X-Frame-Options": ("medium", "Reduces clickjacking exposure for legacy user agents.", "Set DENY or SAMEORIGIN, and complement it with CSP frame-ancestors."),
    "X-Content-Type-Options": ("medium", "Prevents MIME-type sniffing in browsers.", "Set X-Content-Type-Options to nosniff."),
    "Referrer-Policy": ("low", "Controls how much referrer data is shared.", "Set a privacy-preserving policy such as strict-origin-when-cross-origin."),
    "Permissions-Policy": ("low", "Restricts access to browser capabilities.", "Declare only the browser features the application needs."),
}


def _finding_for_header(name: str, value: str | None, is_https: bool) -> Finding:
    severity, description, remediation = HEADER_RULES[name]
    if value:
        if name == "Strict-Transport-Security" and not is_https:
            return Finding("web", "medium", "HSTS observed on HTTP response", "HSTS is only effective when delivered over HTTPS.", "An HTTP-only response cannot establish browser HSTS policy.", "Verify the header is sent on the HTTPS endpoint and redirect HTTP to HTTPS.", value, "WEB-HSTS-HTTP")
        return Finding("web", "info", f"{name} configured", description, "The control is present; value quality should be reviewed for application context.", "Review the directive against the application’s deployment and browser support needs.", value, f"WEB-{name.upper().replace('-', '_')}-PRESENT")
    if name == "Strict-Transport-Security" and not is_https:
        severity = "medium"
    return Finding("web", severity, f"Missing {name}", f"The response does not include {name}.", description, remediation, "header absent", f"WEB-{name.upper().replace('-', '_')}-MISSING")


def audit_headers(host: str, timeout: float = 5.0, session: requests.Session | None = None) -> HeaderAudit:
    """Fetch an HTTPS-first endpoint and evaluate standard security headers."""

    client = session or requests.Session()
    candidates = [f"https://{host}", f"http://{host}"]
    last_error = ""
    for url in candidates:
        try:
            response = client.get(url, timeout=timeout, allow_redirects=True,
                                  headers={"User-Agent": "AegisX-Authorized-Assessment/1.0"})
            headers: Dict[str, str] = {key: value for key, value in response.headers.items()}
            final_url = response.url
            is_https = urlparse(final_url).scheme.lower() == "https"
            findings = [_finding_for_header(name, headers.get(name), is_https) for name in HEADER_RULES]
            server = headers.get("Server", "")
            powered = headers.get("X-Powered-By", "")
            if server:
                findings.append(Finding("web", "low", "Server header exposed", "The response advertises server software information.", "Detailed version data can help attackers fingerprint exposed components.", "Minimize or remove version details from the Server response header.", server, "WEB-SERVER-DISCLOSURE"))
            if powered:
                findings.append(Finding("web", "low", "X-Powered-By header exposed", "The response advertises an implementation technology.", "Technology disclosures make passive fingerprinting easier.", "Remove X-Powered-By or configure the framework to suppress it.", powered, "WEB-POWERED-BY-DISCLOSURE"))
            if urlparse(final_url).scheme.lower() == "http":
                findings.append(Finding("web", "high", "HTTPS endpoint unavailable or redirect absent", "The target did not finish on an HTTPS URL.", "Traffic may be exposed to interception or downgrade attacks.", "Enable HTTPS and redirect HTTP requests to HTTPS.", final_url, "WEB-NO-HTTPS"))
            return HeaderAudit(url, response.status_code, final_url, headers, findings)
        except requests.RequestException as exc:
            last_error = str(exc)
    return HeaderAudit(candidates[0], None, "", error=last_error or "HTTP request failed")
