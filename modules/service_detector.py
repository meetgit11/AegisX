"""Service identification helpers for TCP port results."""

from __future__ import annotations

from typing import Dict

SERVICE_MAP: Dict[int, str] = {
    20: "FTP Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPCBind", 135: "MSRPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 587: "SMTP Submission",
    993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 1521: "Oracle", 2049: "NFS",
    2375: "Docker API", 3000: "HTTP Development", 3306: "MySQL", 3389: "RDP",
    5000: "HTTP Development", 5432: "PostgreSQL", 6379: "Redis", 8000: "HTTP Development",
    8080: "HTTP Alternate", 8443: "HTTPS Alternate", 9200: "Elasticsearch",
}


def service_for_port(port: int) -> str:
    """Return a conservative likely service label for a TCP port."""

    return SERVICE_MAP.get(port, "Unknown TCP Service")


def clean_banner(data: bytes, limit: int = 256) -> str:
    """Decode a service banner without allowing control characters into the UI."""

    text = data[:limit].decode("utf-8", errors="replace")
    return " ".join(text.replace("\x00", "").split())[:limit]
