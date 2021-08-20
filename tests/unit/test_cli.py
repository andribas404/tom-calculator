"""Test cli.py."""
from unittest import mock

import pytest

from tom_calculator import cli


class TestCLI:
    """Test cli."""
    @mock.patch('tom_calculator.cli.subprocess.run')
    def test_migrate(self, mock_run, client_cli):
        """Test migrate."""
        result = client_cli(['migrate'])
        assert result.exit_code == 0
        mock_run.assert_called_once_with(['alembic', 'upgrade', 'head'])

    @mock.patch('tom_calculator.cli.load')
    @mock.patch('tom_calculator.cli.get_datadir')
    def test_migrate(self, mock_get_datadir, mock_load, client_cli):
        """Test migrate."""
        mock_get_datadir.return_value = 'config'
        result = client_cli(['migrate-data'])
        assert result.exit_code == 0
        mock_get_datadir.assert_called_once()
        mock_load.assert_called_once_with('config')
