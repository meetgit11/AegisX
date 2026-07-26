"""
====================================================
AegisX Utility Functions
====================================================

Common reusable helper functions.

Author : Meet Patil
Project : AegisX
"""

from datetime import datetime

import validators


def is_valid_domain(domain: str) -> bool:
    """Validate a domain or URL."""
    return validators.domain(domain) or validators.url(domain)


def current_timestamp() -> str:
    """Return current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")