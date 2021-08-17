import csv
import os
from pathlib import Path
from typing import Any

import pydevd_pycharm


def get_config_path():
    """Get configuration file's path from the environment variable."""
    return Path(os.getenv('TOM_CONFIG'))


def load_csv(path: Path) -> Any:
    """Load data from csv file."""
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        items = list(reader)
        return items


def set_debug():
    """Set debug from env."""
    if os.getenv("DEBUG_PYDEVD"):
        host, port = os.getenv("DEBUG_PYDEVD", "").split(":")
        port_int: int = int(port)

        pydevd_pycharm.settrace(
            host=host,
            stdoutToServer=True,
            stderrToServer=True,
            port=port_int,
            suspend=False,
        )
