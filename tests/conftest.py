"""Pytest conftest."""
import os
from functools import partial
from pathlib import Path

import pytest
from typer.testing import CliRunner

from tom_calculator.cli import app as cli_app


def pytest_configure(config):
    """Configure before running tests."""
    os.environ['TOM_CONFIG'] = os.path.join(config.rootdir, 'config-test.yml')
    os.environ['TOM_DATA'] = os.path.join(config.rootdir, 'tests/data')
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


@pytest.fixture(scope='session')
def client_cli():
    """Client CLI fixture."""
    runner = CliRunner()
    yield partial(runner.invoke, cli_app)


@pytest.fixture(scope='session')
def data_discounts():
    """Fixture with discounts file path."""
    datadir = os.getenv('TOM_DATA', '')
    return Path(datadir) / 'discounts.csv'


@pytest.fixture(scope='session')
def data_taxes():
    """Fixture with discounts file path."""
    datadir = os.getenv('TOM_DATA', '')
    return Path(datadir) / 'taxes.csv'
