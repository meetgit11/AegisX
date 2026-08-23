"""Typed domain models shared across the AegisX application layers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ValidatedTarget:
    """Normalized target accepted by the defensive assessment workflow."""

    original: str
    host: str
    target_type: str
    scheme: Optional[str] = None
    port: Optional[int] = None


@dataclass
class Finding:
    """A normalized security observation produced by a scan module."""

    category: str
    severity: str
    title: str
    description: str
    impact: str = ""
    remediation: str = ""
    evidence: str = ""
    rule_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PortFinding:
    """Result of a single TCP connect attempt."""

    port: int
    state: str
    service: str
    banner: str = ""
    response_time_ms: Optional[float] = None
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HeaderAudit:
    """HTTP security header assessment output."""

    url: str
    status_code: Optional[int]
    final_url: str
    headers: Dict[str, str] = field(default_factory=dict)
    findings: List[Finding] = field(default_factory=list)
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "status_code": self.status_code,
            "final_url": self.final_url,
            "headers": dict(self.headers),
            "findings": [finding.to_dict() for finding in self.findings],
            "error": self.error,
        }


@dataclass
class TLSInspection:
    """Certificate and negotiated TLS connection metadata."""

    host: str
    port: int
    success: bool
    subject: str = ""
    issuer: str = ""
    serial_number: str = ""
    valid_from: str = ""
    valid_to: str = ""
    days_remaining: Optional[int] = None
    tls_version: str = ""
    cipher: str = ""
    certificate_valid: Optional[bool] = None
    verification_error: str = ""
    findings: List[Finding] = field(default_factory=list)
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["findings"] = [finding.to_dict() for finding in self.findings]
        return data


@dataclass
class ReconResult:
    """DNS and WHOIS results, including per-provider errors."""

    host: str
    records: Dict[str, List[str]] = field(default_factory=dict)
    whois: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScoreReport:
    """Transparent deterministic risk calculation output."""

    score: float
    risk_level: str
    breakdown: List[Dict[str, Any]] = field(default_factory=list)
    contributing_factors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScanResult:
    """Complete serializable result for one assessment."""

    scan_id: str
    target: ValidatedTarget
    started_at: str
    completed_at: str = ""
    status: str = "running"
    profile: str = "standard"
    ports: List[PortFinding] = field(default_factory=list)
    headers: Optional[HeaderAudit] = None
    tls: Optional[TLSInspection] = None
    recon: Optional[ReconResult] = None
    findings: List[Finding] = field(default_factory=list)
    score: Optional[ScoreReport] = None
    module_errors: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scan_id": self.scan_id,
            "target": asdict(self.target),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "profile": self.profile,
            "ports": [item.to_dict() for item in self.ports],
            "headers": self.headers.to_dict() if self.headers else None,
            "tls": self.tls.to_dict() if self.tls else None,
            "recon": self.recon.to_dict() if self.recon else None,
            "findings": [item.to_dict() for item in self.findings],
            "score": self.score.to_dict() if self.score else None,
            "module_errors": dict(self.module_errors),
        }
