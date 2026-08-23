# AegisX

AegisX is an **AI-powered cybersecurity assessment platform** for authorized, defensive checks of domains, websites, and network hosts. It combines bounded TCP connectivity scanning, service identification, HTTP security-header auditing, TLS certificate inspection, DNS/WHOIS reconnaissance, deterministic risk scoring, SQLite scan history, and executive PDF/CSV reporting in a Streamlit dashboard.

> **Authorized use only:** Only scan systems, domains, and infrastructure you own or are explicitly authorized to assess. AegisX does not implement exploitation, credential attacks, brute force, payload delivery, or destructive actions.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env            # configure only local, non-committed settings
streamlit run app.py
```

Enter a target such as `example.com`, `https://example.com/`, an IPv4 address, or an IPv6 address. Choose a bounded **quick**, **standard**, or **extended** profile. The application validates input before running independent scanner modules concurrently. A module failure is recorded as a warning and does not discard the rest of the assessment.

## Architecture

The repository follows a layered flow:

`Streamlit UI → target validator → scan orchestrator → scanning modules → risk engine → SQLite DAO → reports`

The `core/models.py` dataclasses provide a stable serialization boundary. Network modules are intentionally implemented with native Python sockets, `requests`, `ssl`, and DNS/WHOIS libraries; no shell commands are constructed from user input. The optional `core/ai_explainer.py` layer has a deterministic fallback and does not block scanning when provider credentials are absent.

## Tests

```bash
pytest -q
```

The test suite covers validation, profile bounds, scoring transparency, recommendation ordering, database round trips, and PDF/CSV export integrity. Network-dependent behavior should be tested against local fixtures or mocks.

## Project layout

| Path | Responsibility |
| --- | --- |
| `app.py` | Streamlit application entry point |
| `core/` | Validation, models, orchestration, scoring, recommendations, logging, optional AI explanation |
| `modules/` | TCP, HTTP, TLS, DNS, WHOIS, and service-detection engines |
| `database/` | SQLite schema and parameterized data-access layer |
| `dashboard/` | Streamlit result views and Plotly visualization |
| `reports/` | ReportLab PDF and CSV exports |
| `tests/` | Focused unit and persistence/report tests |
| `docs/` | Product, software requirements, system design, and development log |
