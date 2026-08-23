from pathlib import Path

from core.models import Finding, PortFinding, ScanResult, ScoreReport, ValidatedTarget
from database.database import Database
from reports.csv_export import scan_to_csv
from reports.pdf_report import build_pdf


def sample_result():
    result = ScanResult(
        scan_id="scan-test-1",
        target=ValidatedTarget("example.com", "example.com", "domain"),
        started_at="2026-08-23T00:00:00+00:00",
        completed_at="2026-08-23T00:00:01+00:00",
        status="completed",
        ports=[PortFinding(443, "open", "HTTPS")],
        findings=[Finding("web", "high", "Missing CSP", "desc", "impact", "fix", "", "WEB-CSP-MISSING")],
        score=ScoreReport(2.15, "Low", [{"rule_id": "WEB-CSP-MISSING", "points": 2.0, "reason": "Missing CSP"}], ["Missing CSP"]),
    )
    return result


def test_database_round_trip(tmp_path: Path):
    database = Database(tmp_path / "test.db")
    result = sample_result()
    database.save_scan(result)
    history = database.history()
    assert history[0]["scan_id"] == result.scan_id
    restored = database.get_scan(result.scan_id)
    assert restored["target"]["host"] == "example.com"
    assert restored["findings"][0]["rule_id"] == "WEB-CSP-MISSING"


def test_report_exports_are_non_empty():
    result = sample_result()
    csv = scan_to_csv(result)
    pdf = build_pdf(result)
    assert "scan_id,target,category" in csv
    assert "Missing CSP" in csv
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000
