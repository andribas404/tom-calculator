"""Util."""
import csv
import logging
import os
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def get_config_path():
    """Get configuration file's path from the environment variable."""
    config = os.getenv('TOM_CONFIG')
    return Path(config)


def load_csv(path: Path) -> Any:
    """Load data from csv file."""
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        items = list(reader)
        return items


def round_up(amount: Decimal) -> Decimal:
    """Round number to upper with cent precision."""
    return Decimal(amount.quantize(Decimal('.01'), rounding=ROUND_CEILING))


def round_down(amount: Decimal) -> Decimal:
    """Round number to smaller with cent precision."""
    return Decimal(amount.quantize(Decimal('.01'), rounding=ROUND_FLOOR))
