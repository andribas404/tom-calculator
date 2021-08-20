"""Test util.py."""
from decimal import Decimal
from pathlib import Path
from unittest import mock

import pytest

from tom_calculator import util


class TestGetConfigPath:
    """Test get_config_path."""
    @mock.patch('tom_calculator.util.os.getenv')
    def test_get_config_path(self, mock_getenv):
        """Test get_config_path."""
        mock_getenv.return_value = 'config'
        result = util.get_config_path()
        assert result == Path('config')


class TestGetDatadir:
    """Test get_datadir."""
    @mock.patch('tom_calculator.util.os.getenv')
    def test_get_config_path(self, mock_getenv):
        """Test get_datadir."""
        mock_getenv.return_value = 'config'
        result = util.get_datadir()
        assert result == Path('config')


class TestLoadCsv:
    """Test load_csv."""
    def test_load_csv_discounts(self, data_discounts, snapshot):
        """Test load_csv."""
        result = util.load_csv(data_discounts)
        assert result == snapshot

    def test_load_csv_taxes(self, data_taxes, snapshot):
        """Test load_csv."""
        result = util.load_csv(data_taxes)
        assert result == snapshot


class TestRoundUp:
    """Test round_up."""
    @pytest.mark.parametrize(('amount', 'expected'), [
        (Decimal('0'), Decimal('0.')),
        (Decimal('23'), Decimal('23')),
        (Decimal('23.05'), Decimal('23.05')),
        (Decimal('0.001'), Decimal('0.01')),
        (Decimal('0.234'), Decimal('0.24')),
        (Decimal('0.22999999'), Decimal('0.23')),
        (Decimal('-0.00001'), Decimal('0.')),
        (Decimal('232.05555'), Decimal('232.06')),
    ])
    def test_round_up(self, amount, expected):
        """Test ."""
        result = util.round_up(amount)
        assert result == expected


class TestRoundDown:
    """Test round_down."""
    @pytest.mark.parametrize(('amount', 'expected'), [
        (Decimal('0'), Decimal('0.')),
        (Decimal('23'), Decimal('23')),
        (Decimal('23.05'), Decimal('23.05')),
        (Decimal('0.001'), Decimal('0.')),
        (Decimal('0.234'), Decimal('0.23')),
        (Decimal('0.22999999'), Decimal('0.22')),
        (Decimal('-0.00001'), Decimal('-0.01')),
        (Decimal('232.05555'), Decimal('232.05')),
    ])
    def test_round_down(self, amount, expected):
        """Test round_down."""
        result = util.round_down(amount)
        assert result == expected
