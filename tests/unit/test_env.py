"""Test that environment is set."""
import os
from pathlib import Path


class TestEnvironment:
    """Test environment."""
    def test_env_exists(self):
        """Test env variable exists."""
        config = os.getenv('TOM_CONFIG')
        assert config is not None
        assert Path(config).is_file() is True

    def test_env_is_test(self):
        """Test env variable is correct."""
        config = os.getenv('TOM_CONFIG')
        assert config.endswith('config-test.yml')
