"""Tests for divide, power, sqrt, append_history, and show_history in calc.py."""

import pytest
import calc
from calc import divide, power, sqrt, append_history, show_history


def test_divide_normal_values():
    """Verify that divide returns the correct quotient for non-zero divisors."""
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises_value_error():
    """Verify that divide raises ValueError when the divisor is zero."""
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        divide(5, 0)


def test_divide_by_zero_error_message():
    """Verify the exact error message raised on division by zero."""
    with pytest.raises(ValueError) as exc_info:
        divide(1, 0)
    assert str(exc_info.value) == "Division by zero is not allowed"


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


class TestAppendHistory:
    def test_writes_correct_format(self, tmp_path, monkeypatch):
        # ST5 Validated
        history_file = tmp_path / "calc_history"
        monkeypatch.setattr(calc, "HISTORY_FILE", str(history_file))
        append_history("2+3", 5)
        assert history_file.read_text() == "2+3=5\n"

    def test_appends_multiple_entries(self, tmp_path, monkeypatch):
        # ST5 Validated
        history_file = tmp_path / "calc_history"
        monkeypatch.setattr(calc, "HISTORY_FILE", str(history_file))
        append_history("2+3", 5)
        append_history("10/2", 5.0)
        lines = history_file.read_text().splitlines()
        assert lines == ["2+3=5", "10/2=5.0"]


class TestShowHistory:
    def test_reads_and_prints_entries(self, tmp_path, monkeypatch, capsys):
        # ST5 Validated
        history_file = tmp_path / "calc_history"
        history_file.write_text("2+3=5\n4*4=16\n")
        monkeypatch.setattr(calc, "HISTORY_FILE", str(history_file))
        show_history(10)
        captured = capsys.readouterr()
        assert "2+3=5" in captured.out
        assert "4*4=16" in captured.out

    def test_missing_file_prints_no_history(self, tmp_path, monkeypatch, capsys):
        # ST5 Validated
        monkeypatch.setattr(calc, "HISTORY_FILE", str(tmp_path / "nonexistent"))
        show_history(10)
        captured = capsys.readouterr()
        assert captured.out.strip() == "No history found."

    def test_last_zero_returns_nothing(self, tmp_path, monkeypatch, capsys):
        # ST5 Validated
        history_file = tmp_path / "calc_history"
        history_file.write_text("2+3=5\n4*4=16\n")
        monkeypatch.setattr(calc, "HISTORY_FILE", str(history_file))
        show_history(0)
        captured = capsys.readouterr()
        assert captured.out == ""
