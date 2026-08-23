"""CSV export helpers for AegisX scan results."""

from __future__ import annotations

import csv
import io
from typing import Any

from core.models import ScanResult


def scan_to_csv(result: ScanResult) -> str:
    """Serialize ports and findings into a consistent analysis-friendly CSV."""

    output = io.StringIO()
    fields = ["scan_id", "target", "category", "severity", "title", "description", "impact", "remediation", "evidence", "rule_id", "port", "service", "state", "banner"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for finding in result.findings:
        writer.writerow({"scan_id": result.scan_id, "target": result.target.host, **finding.to_dict(), "port": "", "service": "", "state": "", "banner": ""})
    for port in result.ports:
        writer.writerow({"scan_id": result.scan_id, "target": result.target.host, "category": "network", "severity": "info", "title": f"TCP port {port.port}", "description": "TCP connectivity result", "impact": "", "remediation": "Close or restrict services that are not required.", "evidence": port.error, "rule_id": f"PORT-{port.port}", "port": port.port, "service": port.service, "state": port.state, "banner": port.banner})
    return output.getvalue()


def write_csv(result: ScanResult, path: str) -> str:
    """Write CSV output to *path* and return that path."""

    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(scan_to_csv(result))
    return path
