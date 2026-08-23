"""Optional AI explanation layer with a non-network deterministic fallback."""

from __future__ import annotations

import os
from typing import Any, Dict

from core.models import ScanResult


class AIExplainer:
    """Explain structured scan results without inventing findings.

    A provider can be injected later; absent a configured provider, the class
    returns a concise explanation built only from the scan's structured data.
    """

    def __init__(self, provider: Any | None = None) -> None:
        self.provider = provider
        self.api_key_configured = bool(os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY"))

    def explain_risk(self, result: ScanResult) -> str:
        """Return a human-friendly explanation grounded in the result."""

        score = result.score.score if result.score else 0.0
        level = result.score.risk_level if result.score else "Unknown"
        factors = result.score.contributing_factors if result.score else []
        if self.provider:
            return str(self.provider(result.to_dict()))
        if not factors:
            return f"AegisX calculated a {score:.2f}/10 {level.lower()} risk score. No weighted risk factors were recorded."
        return (f"AegisX calculated a {score:.2f}/10 {level.lower()} risk score. "
                f"The main contributing factors were: {', '.join(factors[:5])}. "
                "Address the highest-severity recommendations first and repeat the assessment after remediation.")

    def explain_finding(self, finding: Dict[str, Any]) -> str:
        """Explain one structured finding without adding unsupported claims."""

        return (f"{finding.get('title', 'This finding')} is rated {str(finding.get('severity', 'unknown')).lower()}. "
                f"{finding.get('description', '')} Recommended action: {finding.get('remediation', 'Review the finding and apply an appropriate control.')}" )
