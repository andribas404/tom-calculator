import csv
import logging
import os
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def get_config_path():
    """Get configuration file's path from the environment variable."""
    return Path(os.getenv('TOM_CONFIG'))


def load_csv(path: Path) -> Any:
    """Load data from csv file."""
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        items = list(reader)
        return items


def round_up(amount):
    return Decimal(amount.quantize(Decimal('.01'), rounding=ROUND_CEILING))


def round_down(amount):
    return Decimal(amount.quantize(Decimal('.01'), rounding=ROUND_FLOOR))
