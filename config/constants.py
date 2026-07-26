"""
====================================================
AegisX - Global Constants
====================================================

This module stores constant values used throughout
the application.

Constants should NEVER be modified at runtime.

Author : Meet Patil
Project : AegisX
"""

# ====================================================
# Application Information
# ====================================================

APP_NAME = "AegisX"
APP_TAGLINE = "AI-Powered Cybersecurity Assessment Platform"

VERSION = "1.0.0"

# ====================================================
# Risk Levels
# ====================================================

LOW = "Low"
MEDIUM = "Medium"
HIGH = "High"
CRITICAL = "Critical"

RISK_LEVELS = [
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL
]

# ====================================================
# Default Scan Ports
# ====================================================

DEFAULT_PORT_RANGE = (1, 1024)

# ====================================================
# Common Ports
# ====================================================

COMMON_PORTS = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP Alternate",
}

# ====================================================
# Security Headers
# ====================================================

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]

# ====================================================
# Supported Protocols
# ====================================================

SUPPORTED_PROTOCOLS = [
    "HTTP",
    "HTTPS",
    "TCP",
    "UDP",
    "DNS",
    "SSL",
    "TLS"
]