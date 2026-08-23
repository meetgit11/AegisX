"""Assessment result page rendering."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from core.models import ScanResult
from dashboard.ui_components import render_finding_table


def render_results(result: ScanResult) -> None:
    """Render the completed assessment with clear, task-oriented tabs."""

    overview, network, web, tls_tab, recon, recommendations = st.tabs(["Overview", "Network", "Web security", "TLS", "DNS & WHOIS", "Recommendations"])
    with overview:
        render_finding_table(result)
        if result.module_errors:
            st.warning("Some modules completed with warnings: " + ", ".join(result.module_errors))
    with network:
        rows = [port.to_dict() for port in result.ports]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True) if rows else st.info("No port results returned.")
    with web:
        if result.headers:
            st.caption(f"Checked {result.headers.final_url or result.headers.url} (HTTP {result.headers.status_code or 'error'})")
            st.dataframe(pd.DataFrame([finding.to_dict() for finding in result.headers.findings]), use_container_width=True, hide_index=True)
        else:
            st.info("HTTP header analysis unavailable.")
    with tls_tab:
        if result.tls:
            tls = result.tls
            st.json({key: value for key, value in tls.to_dict().items() if key != "findings"})
            if tls.findings:
                st.dataframe(pd.DataFrame([finding.to_dict() for finding in tls.findings]), use_container_width=True, hide_index=True)
        else:
            st.info("TLS inspection unavailable.")
    with recon:
        if result.recon:
            st.subheader("DNS records")
            st.json(result.recon.records)
            st.subheader("WHOIS metadata")
            st.json(result.recon.whois or {"status": "No public WHOIS data returned"})
            if result.recon.errors:
                st.caption("Non-fatal lookup notes: " + "; ".join(result.recon.errors))
        else:
            st.info("Reconnaissance is available for domain targets.")
    with recommendations:
        actionable = [finding for finding in result.findings if finding.severity.lower() != "info"]
        if not actionable:
            st.success("No actionable recommendations were generated.")
        for finding in actionable:
            with st.expander(f"{finding.severity.upper()} — {finding.title}"):
                st.write(finding.remediation)
                if finding.impact:
                    st.caption(f"Impact: {finding.impact}")
