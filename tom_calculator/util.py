import os
from pathlib import Path


def get_config_path():
    return Path(os.getenv('TOM_CONFIG'))
