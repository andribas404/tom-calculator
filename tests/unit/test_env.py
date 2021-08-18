import os
from pathlib import Path


class TestEnvironment:
    def test_env_exists(self):
        config = os.getenv('TOM_CONFIG')
        assert config is not None
        assert Path(config).is_file() is True

    def test_env_is_test(self):
        config = os.getenv('TOM_CONFIG')
        assert config.endswith('config-test.yml')
