"""
====================================================
AegisX Logging System
====================================================

Provides centralized logging throughout the
application.

Author : Meet Patil
Project : AegisX
"""

import logging
from pathlib import Path

from config.settings import settings

# Create log directory
log_dir = Path(settings.output_directory) / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "aegisx.log"

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AegisX")