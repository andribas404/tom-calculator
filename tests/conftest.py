import os

import pytest


def pytest_configure(config):
    os.environ['TOM_CONFIG'] = os.path.join(config.rootdir, 'config-test.yml')
    return config


def pytest_collection_modifyitems(items):
    for item in items:
        itemdir = item.nodeid.split('/')[1]
        marker = getattr(pytest.mark, itemdir, None)
        if marker:
            item.add_marker(marker)
