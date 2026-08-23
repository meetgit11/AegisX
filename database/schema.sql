PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS targets (
    target_id TEXT PRIMARY KEY,
    host_identifier TEXT NOT NULL UNIQUE,
    target_type TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scans (
    scan_id TEXT PRIMARY KEY,
    target_id TEXT NOT NULL,
    scan_timestamp TEXT NOT NULL,
    risk_score REAL,
    risk_level TEXT,
    status TEXT NOT NULL,
    profile TEXT NOT NULL,
    result_json TEXT NOT NULL,
    FOREIGN KEY (target_id) REFERENCES targets(target_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS findings (
    finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    impact TEXT,
    remediation TEXT,
    evidence TEXT,
    rule_id TEXT,
    FOREIGN KEY (scan_id) REFERENCES scans(scan_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id TEXT NOT NULL,
    report_type TEXT NOT NULL,
    file_path TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (scan_id) REFERENCES scans(scan_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_scans_timestamp ON scans(scan_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_findings_scan ON findings(scan_id);
