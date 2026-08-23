"""Defensive TCP connectivity scanner with conservative scope limits."""

from __future__ import annotations

import errno
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List

from config.constants import COMMON_PORTS
from core.logger import logger
from core.models import PortFinding
from modules.service_detector import clean_banner, service_for_port

PROFILES = {
    "quick": (22, 53, 80, 443, 8080),
    "standard": tuple(COMMON_PORTS.keys()),
    "extended": tuple(sorted(set(COMMON_PORTS) | {111, 135, 139, 445, 587, 993, 995, 1433,
                                                      1521, 2049, 2375, 3000, 3389, 5000,
                                                      5432, 6379, 8000, 8443, 9200})),
}


def ports_for_profile(profile: str = "standard", custom_ports: Iterable[int] | None = None) -> List[int]:
    """Return a validated, bounded list of ports for a scan profile."""

    if custom_ports is not None:
        ports = sorted({int(port) for port in custom_ports if 1 <= int(port) <= 65535})
        if len(ports) > 256:
            raise ValueError("Custom scans are limited to 256 TCP ports.")
        return ports
    normalized = profile.lower()
    if normalized not in PROFILES:
        raise ValueError("Unknown scan profile. Choose quick, standard, or extended.")
    return list(PROFILES[normalized])


def _scan_one(host: str, port: int, timeout: float, grab_banners: bool) -> PortFinding:
    started = time.perf_counter()
    sock = socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        address = (host, port, 0, 0) if ":" in host else (host, port)
        code = sock.connect_ex(address)
        elapsed = round((time.perf_counter() - started) * 1000, 2)
        if code != 0:
            state = "timeout" if code in {errno.ETIMEDOUT, errno.EAGAIN, errno.EWOULDBLOCK} else "closed"
            return PortFinding(port, state, service_for_port(port), response_time_ms=elapsed)
        banner = ""
        if grab_banners and port not in {80, 443}:
            try:
                sock.settimeout(min(timeout, 0.75))
                banner = clean_banner(sock.recv(256))
            except (socket.timeout, OSError):
                banner = ""
        return PortFinding(port, "open", service_for_port(port), banner, elapsed)
    except socket.timeout:
        return PortFinding(port, "timeout", service_for_port(port), response_time_ms=round((time.perf_counter() - started) * 1000, 2))
    except OSError as exc:
        logger.debug("Port %s scan failed: %s", port, exc)
        return PortFinding(port, "error", service_for_port(port), error=str(exc))
    finally:
        sock.close()


def scan_ports(host: str, profile: str = "standard", timeout: float = 1.0,
               max_workers: int = 32, custom_ports: Iterable[int] | None = None,
               grab_banners: bool = True) -> List[PortFinding]:
    """Scan selected TCP ports using a bounded worker pool."""

    if timeout <= 0 or timeout > 10:
        raise ValueError("Timeout must be greater than zero and no more than 10 seconds.")
    ports = ports_for_profile(profile, custom_ports)
    workers = max(1, min(int(max_workers), 64, len(ports) or 1))
    results: List[PortFinding] = []
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="aegisx-port") as pool:
        futures = [pool.submit(_scan_one, host, port, timeout, grab_banners) for port in ports]
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda item: item.port)
