from core.models import Finding, HeaderAudit, PortFinding, TLSInspection, ValidatedTarget
from core.scanner import ScanOrchestrator
from database.database import Database


def test_orchestrator_isolates_module_failure(monkeypatch, tmp_path):
    monkeypatch.setattr("core.scanner.socket.gethostbyname", lambda host: "192.0.2.10")
    monkeypatch.setattr("core.scanner.scan_ports", lambda *args, **kwargs: [PortFinding(443, "open", "HTTPS")])
    monkeypatch.setattr("core.scanner.audit_headers", lambda *args, **kwargs: HeaderAudit("https://example.com", 200, "https://example.com", findings=[Finding("web", "high", "Missing CSP", "d", remediation="fix")]))
    monkeypatch.setattr("core.scanner.inspect_tls", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("simulated TLS outage")))
    monkeypatch.setattr("core.scanner.resolve_dns", lambda *args, **kwargs: ({"A": ["192.0.2.10"]}, []))
    monkeypatch.setattr("core.scanner.lookup_whois", lambda *args, **kwargs: ({}, "not available"))

    database = Database(tmp_path / "scan.db")
    result = ScanOrchestrator(database).execute_scan("example.com", persist=True)
    assert result.status == "completed_with_warnings"
    assert "tls" in result.module_errors
    assert result.score.score > 0
    assert database.get_scan(result.scan_id)["scan_id"] == result.scan_id
