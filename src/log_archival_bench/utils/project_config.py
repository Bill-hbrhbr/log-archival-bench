"""Project configurations."""

from pathlib import Path

import log_archival_bench

# Constants
PACKAGE_ROOT = Path(log_archival_bench.__file__).parent

BUILD_DIR = PACKAGE_ROOT / "build"
CONFIG_DIR = PACKAGE_ROOT / "config"
