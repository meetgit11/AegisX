"""Recommendation generation derived only from structured findings."""

from __future__ import annotations

from typing import Iterable, List, Dict, Any

from core.models import Finding


def generate_recommendations(findings: Iterable[Finding]) -> List[Dict[str, Any]]:
    """Convert findings into stable, prioritized remediation records."""

    recommendations = []
    for finding in findings:
        if finding.severity.lower() == "info":
            continue
        recommendations.append({
            "title": finding.title,
            "category": finding.category,
            "severity": finding.severity,
            "why_it_matters": finding.description,
            "security_impact": finding.impact,
            "recommended_action": finding.remediation,
            "reference": finding.rule_id or "AegisX rule",
        })
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(recommendations, key=lambda item: (order.get(item["severity"].lower(), 9), item["title"]))
