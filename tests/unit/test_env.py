"""Test that environment is set."""
import os
from pathlib import Path


class TestEnvironment:
    """Test environment."""
    def test_tom_config_exists(self):
        """Test TOM_CONFIG exists."""
        config = os.getenv('TOM_CONFIG')
        assert config is not None
        assert Path(config).is_file() is True

    def test_tom_config_is_test(self):
        """Test TOM_CONFIG is correct."""
        config = os.getenv('TOM_CONFIG')
        assert config.endswith('config-test.yml')

    def test_tom_data_exists(self):
        """Test TOM_DATA exists."""
        config = os.getenv('TOM_DATA')
        assert config is not None
        assert Path(config).is_dir() is True

    def test_tom_data_is_test(self):
        """Test TOM_DATA is correct."""
        config = os.getenv('TOM_DATA')
        assert config.endswith('tests/data')
