import streamlit as st

from config.constants import APP_NAME, APP_TAGLINE
from config.settings import settings

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AegisX")

st.caption(APP_TAGLINE)

st.divider()

st.sidebar.title("Navigation")

st.sidebar.success("System Ready")

st.write("### AI-Powered Cybersecurity Assessment Platform")

target = st.text_input(
    "Target Domain / IP",
    placeholder="example.com"
)

scan_type = st.radio(
    "Scan Type",
    ["Website", "Network"]
)

if st.button("Start Scan"):
    st.info("Scanner module will be implemented in Phase 2.")

st.divider()

st.caption(
    f"{settings.app_name} v{settings.app_version}"
)