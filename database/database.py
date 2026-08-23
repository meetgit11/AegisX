"""SQLite persistence layer for AegisX scan history."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from config.settings import settings
from core.models import Finding, ScanResult


class Database:
    """Small parameterized SQLite DAO with automatic schema initialization."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or settings.database_name)
        if not self.path.is_absolute():
            self.path = Path(__file__).resolve().parent.parent / self.path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        with self.connect() as connection:
            connection.executescript(schema)

    def save_scan(self, result: ScanResult) -> None:
        target_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"aegisx:{result.target.host}"))
        payload = json.dumps(result.to_dict(), ensure_ascii=False)
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO targets(target_id, host_identifier, target_type, created_at) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(host_identifier) DO UPDATE SET target_type=excluded.target_type",
                (target_id, result.target.host, result.target.target_type, result.started_at),
            )
            connection.execute(
                "INSERT OR REPLACE INTO scans(scan_id, target_id, scan_timestamp, risk_score, risk_level, status, profile, result_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (result.scan_id, target_id, result.completed_at or result.started_at,
                 result.score.score if result.score else None,
                 result.score.risk_level if result.score else None,
                 result.status, result.profile, payload),
            )
            connection.execute("DELETE FROM findings WHERE scan_id = ?", (result.scan_id,))
            connection.executemany(
                "INSERT INTO findings(scan_id, category, severity, title, description, impact, remediation, evidence, rule_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [(result.scan_id, item.category, item.severity, item.title, item.description,
                  item.impact, item.remediation, item.evidence, item.rule_id) for item in result.findings],
            )

    def history(self, limit: int = 25) -> List[Dict[str, Any]]:
        """Return recent scans without exposing the full JSON payload."""

        with self.connect() as connection:
            rows = connection.execute(
                "SELECT scan_id, target_id, scan_timestamp, risk_score, risk_level, status, profile "
                "FROM scans ORDER BY scan_timestamp DESC LIMIT ?", (max(1, min(limit, 100)),)
            ).fetchall()
        return [dict(row) for row in rows]

    def get_scan(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Return a persisted scan payload and its findings."""

        with self.connect() as connection:
            row = connection.execute("SELECT result_json FROM scans WHERE scan_id = ?", (scan_id,)).fetchone()
            if not row:
                return None
            result = json.loads(row["result_json"])
            finding_rows = connection.execute(
                "SELECT category, severity, title, description, impact, remediation, evidence, rule_id "
                "FROM findings WHERE scan_id = ? ORDER BY finding_id", (scan_id,)
            ).fetchall()
        result["findings"] = [dict(item) for item in finding_rows]
        return result

    def record_report(self, scan_id: str, report_type: str, file_path: str) -> None:
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO reports(scan_id, report_type, file_path, created_at) VALUES (?, ?, ?, datetime('now'))",
                (scan_id, report_type, file_path),
            )
