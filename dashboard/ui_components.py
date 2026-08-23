"""Reusable Streamlit presentation components."""

from __future__ import annotations

import streamlit as st

from core.models import ScanResult


def render_metric_cards(result: ScanResult) -> None:
    """Render high-signal assessment metrics."""

    score = result.score.score if result.score else 0.0
    risk = result.score.risk_level if result.score else "Unknown"
    open_ports = sum(1 for port in result.ports if port.state == "open")
    actionable = sum(1 for finding in result.findings if finding.severity.lower() != "info")
    columns = st.columns(4)
    columns[0].metric("Risk score", f"{score:.2f} / 10", risk)
    columns[1].metric("Open TCP ports", open_ports)
    columns[2].metric("Actionable findings", actionable)
    columns[3].metric("Assessment status", result.status.replace("_", " ").title())


def render_finding_table(result: ScanResult) -> None:
    """Display findings as a safe dataframe."""

    rows = [{"Severity": item.severity.title(), "Category": item.category.title(), "Finding": item.title, "Evidence": item.evidence or "-", "Remediation": item.remediation} for item in result.findings]
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.success("No actionable findings were produced by the completed modules.")
