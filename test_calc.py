"""Tests for power and sqrt commands in calc.py."""

import pytest
from calc import power, sqrt


def test_power_positive_exponent():
    # ST5 Validated
    assert power(2, 3) == 8.0


def test_power_zero_exponent():
    # ST5 Validated
    assert power(5, 0) == 1.0


def test_sqrt_positive_number():
    # ST5 Validated
    assert sqrt(9) == 3.0


def test_sqrt_zero():
    # ST5 Validated
    assert sqrt(0) == 0.0


def test_sqrt_negative_exits(capsys):
    # ST5 Validated
    with pytest.raises(SystemExit) as exc_info:
        sqrt(-1)
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err
