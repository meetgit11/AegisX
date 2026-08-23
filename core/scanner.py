"""Central AegisX assessment orchestration layer."""

from __future__ import annotations

import socket
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, Any

from core.logger import logger
from core.models import ScanResult
from core.recommendations import generate_recommendations
from core.risk_engine import calculate_score
from core.validator import validate_target
from database.database import Database
from modules.dns_lookup import resolve_dns
from modules.header_analyzer import audit_headers
from modules.port_scanner import scan_ports
from modules.ssl_inspector import inspect_tls
from modules.whois_lookup import lookup_whois


class ScanOrchestrator:
    """Coordinate independent assessment modules without a single point of failure."""

    def __init__(self, database: Database | None = None) -> None:
        self.database = database

    def execute_scan(self, raw_target: str, profile: str = "standard", timeout: float = 1.0,
                     persist: bool = True) -> ScanResult:
        """Validate a target, run modules concurrently, score, and optionally persist."""

        target = validate_target(raw_target)
        result = ScanResult(str(uuid.uuid4()), target, ScanResult.now_iso(), profile=profile)
        try:
            resolved_host = socket.gethostbyname(target.host)
        except OSError:
            resolved_host = target.host

        jobs: Dict[str, Callable[[], Any]] = {
            "ports": lambda: scan_ports(resolved_host, profile=profile, timeout=timeout),
            "headers": lambda: audit_headers(target.host, timeout=max(2.0, timeout * 3)),
            "tls": lambda: inspect_tls(target.host, timeout=max(2.0, timeout * 3)),
        }
        if target.target_type == "domain":
            jobs["recon"] = lambda: self._recon(target.host)

        with ThreadPoolExecutor(max_workers=len(jobs), thread_name_prefix="aegisx-module") as pool:
            future_map = {pool.submit(job): name for name, job in jobs.items()}
            for future in as_completed(future_map):
                name = future_map[future]
                try:
                    value = future.result()
                    if name == "ports":
                        result.ports = value
                    elif name == "headers":
                        result.headers = value
                        result.findings.extend(value.findings)
                    elif name == "tls":
                        result.tls = value
                        result.findings.extend(value.findings)
                    elif name == "recon":
                        result.recon = value
                except Exception as exc:  # module failures are recorded, not fatal
                    logger.exception("Scan module %s failed for %s", name, target.host)
                    result.module_errors[name] = exc.__class__.__name__

        result.score = calculate_score(result.findings, result.ports, result.tls)
        result.completed_at = ScanResult.now_iso()
        result.status = "completed" if not result.module_errors else "completed_with_warnings"
        if persist and self.database:
            self.database.save_scan(result)
        return result

    @staticmethod
    def _recon(host: str):
        records, errors = resolve_dns(host)
        whois_data, whois_error = lookup_whois(host)
        if whois_error:
            errors.append(whois_error)
        from core.models import ReconResult
        return ReconResult(host, records, whois_data, errors)


def execute_scan(raw_target: str, profile: str = "standard", timeout: float = 1.0,
                 database: Database | None = None, persist: bool = True) -> ScanResult:
    """Convenience wrapper for the default orchestrator."""

    return ScanOrchestrator(database).execute_scan(raw_target, profile, timeout, persist)
