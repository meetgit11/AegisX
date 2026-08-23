"""AegisX Streamlit application entry point."""

from __future__ import annotations

import streamlit as st

from config.constants import APP_NAME, APP_TAGLINE
from config.settings import settings
from core.ai_explainer import AIExplainer
from core.models import ScanResult
from core.scanner import ScanOrchestrator
from core.validator import TargetValidationError, validate_target
from dashboard.charts import risk_gauge
from dashboard.pages import render_results
from dashboard.ui_components import render_metric_cards
from database.database import Database
from reports.csv_export import scan_to_csv
from reports.pdf_report import build_pdf

st.set_page_config(page_title=APP_NAME, page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
    .stApp { background: #07131a; color: #e2e8f0; }
    [data-testid="stSidebar"] { background: #0b1f2a; }
    .block-container { max-width: 1440px; padding-top: 2rem; }
    h1, h2, h3 { letter-spacing: -0.02em; }
    .notice { border: 1px solid #155e75; border-radius: 8px; padding: 0.8rem 1rem; background: #082f49; }
</style>
""", unsafe_allow_html=True)


def main() -> None:
    """Render the AegisX application."""

    database = Database()
    orchestrator = ScanOrchestrator(database)
    st.title("🛡️ AegisX")
    st.caption(APP_TAGLINE)
    st.markdown('<div class="notice"><b>Authorized use only:</b> Only scan systems, domains, and infrastructure you own or are explicitly authorized to assess.</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("Assessment controls")
        target_input = st.text_input("Target domain or IP", placeholder="example.com or 192.0.2.10")
        profile = st.selectbox("Scan profile", ["quick", "standard", "extended"], index=1, help="Quick checks a few web ports; standard checks common services; extended adds a bounded set of additional ports.")
        timeout = st.slider("TCP timeout (seconds)", 0.2, 3.0, min(float(settings.default_timeout), 3.0), 0.1)
        start = st.button("Start assessment", type="primary", use_container_width=True)
        st.divider()
        st.caption(f"AegisX v{settings.app_version}")

    if start:
        try:
            validate_target(target_input)
        except TargetValidationError as exc:
            st.error(str(exc))
        else:
            with st.spinner("Running authorized assessment modules…"):
                try:
                    st.session_state["last_result"] = orchestrator.execute_scan(target_input, profile=profile, timeout=timeout)
                except Exception:
                    st.error("The assessment could not be started. Check the target and application logs for technical details.")

    result: ScanResult | None = st.session_state.get("last_result")
    if result is None:
        st.info("Enter an authorized target in the sidebar to begin. Results will appear here after the assessment completes.")
    else:
        st.subheader(f"Assessment: {result.target.host}")
        render_metric_cards(result)
        score = result.score.score if result.score else 0.0
        level = result.score.risk_level if result.score else "Unknown"
        left, right = st.columns([1, 2])
        with left:
            st.plotly_chart(risk_gauge(score, level), use_container_width=True, config={"displayModeBar": False})
        with right:
            st.write("#### Major contributing factors")
            factors = result.score.contributing_factors if result.score else []
            st.write("\n".join(f"- {factor}" for factor in factors) if factors else "No weighted risk factors were recorded.")
        with st.expander("Explain this risk score"):
            st.write(AIExplainer().explain_risk(result))
        render_results(result)
        st.divider()
        st.subheader("Reports")
        pdf_bytes = build_pdf(result)
        csv_text = scan_to_csv(result)
        col_pdf, col_csv = st.columns(2)
        with col_pdf:
            st.download_button("Download executive PDF", pdf_bytes, file_name=f"aegisx-{result.scan_id}.pdf", mime="application/pdf", use_container_width=True)
        with col_csv:
            st.download_button("Download findings CSV", csv_text, file_name=f"aegisx-{result.scan_id}.csv", mime="text/csv", use_container_width=True)

    with st.expander("Scan history"):
        history = database.history()
        if history:
            st.dataframe(history, use_container_width=True, hide_index=True)
        else:
            st.caption("No completed assessments have been stored yet.")


if __name__ == "__main__":
    main()
