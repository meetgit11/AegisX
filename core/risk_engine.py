"""Deterministic heuristic risk scoring for AegisX assessments."""

from __future__ import annotations

from typing import Iterable, List

from core.models import Finding, PortFinding, ScoreReport, TLSInspection

SEVERITY_POINTS = {"info": 0.0, "low": 0.4, "medium": 1.0, "high": 2.0, "critical": 3.5}
SENSITIVE_PORT_POINTS = {21: 1.2, 23: 1.8, 445: 1.5, 2375: 2.5, 3389: 1.2, 6379: 1.8, 9200: 1.8}


def risk_level(score: float) -> str:
    """Map a normalized 0-10 score to a readable risk level."""

    if score >= 8:
        return "Critical"
    if score >= 6:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def calculate_score(findings: Iterable[Finding], ports: Iterable[PortFinding] = (), tls: TLSInspection | None = None) -> ScoreReport:
    """Calculate a capped score with a detailed rule-by-rule breakdown."""

    breakdown = []
    contributing = []
    total = 0.0
    for finding in findings:
        points = SEVERITY_POINTS.get(finding.severity.lower(), 0.0)
        if points <= 0:
            continue
        total += points
        breakdown.append({"rule_id": finding.rule_id or finding.title, "points": points, "reason": finding.title})
        contributing.append(finding.title)

    for port in ports:
        if port.state != "open":
            continue
        points = SENSITIVE_PORT_POINTS.get(port.port, 0.15)
        total += points
        reason = f"Open TCP port {port.port} ({port.service})"
        breakdown.append({"rule_id": f"PORT-{port.port}", "points": points, "reason": reason})
        if port.port in SENSITIVE_PORT_POINTS:
            contributing.append(reason)

    if tls and tls.success and tls.days_remaining is not None and tls.days_remaining > 30:
        # Successful TLS is evidence, not a vulnerability; no score is added.
        pass
    score = round(min(10.0, total), 2)
    return ScoreReport(score, risk_level(score), breakdown, contributing[:10])
