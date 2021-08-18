"""Pytest conftest."""
import os

import pytest


def pytest_configure(config):
    """Configure before running tests."""
    os.environ['TOM_CONFIG'] = os.path.join(config.rootdir, 'config-test.yml')
    return config


def pytest_collection_modifyitems(items):
    """Add markers to the items according to the folders.

    tests/unit/test_1 -> unit
    tests/integration/test_2 -> integration
    """
    for item in items:
        itemdir = item.nodeid.split('/')[1]
        marker = getattr(pytest.mark, itemdir, None)
        if marker:
            item.add_marker(marker)
