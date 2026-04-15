"""Tests for divide, power, sqrt, percentage, factorial, append_history, and show_history in calc.py."""

import pytest
import calc
from calc import divide, factorial, percentage, power, sqrt, append_history, show_history


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


class TestPower:
    def test_positive_exponent(self):
        """Verify that 2^3 returns 8."""
        assert power(2, 3) == 8.0

    def test_zero_exponent(self):
        """Verify that any base raised to 0 returns 1."""
        assert power(5, 0) == 1.0

    def test_zero_to_zero_returns_one(self):
        """Verify the edge case 0^0 returns 1 per mathematical convention."""
        assert power(0, 0) == 1.0

    def test_negative_exponent_returns_float(self):
        """Verify that a negative exponent returns a float (reciprocal)."""
        result = power(2, -1)
        assert result == 0.5
        assert isinstance(result, float)

    def test_large_numbers(self):
        """Verify that large exponents compute correctly without error."""
        assert power(2, 10) == 1024.0
        assert power(10, 6) == 1_000_000.0

    def test_non_numeric_base_raises_value_error(self):
        """Verify that a non-numeric base raises ValueError."""
        with pytest.raises(ValueError, match="Both base and exponent must be numeric"):
            power("two", 3)

    def test_non_numeric_exponent_raises_value_error(self):
        """Verify that a non-numeric exponent raises ValueError."""
        with pytest.raises(ValueError, match="Both base and exponent must be numeric"):
            power(2, "three")

    def test_bool_base_raises_value_error(self):
        """Verify that a boolean base raises ValueError (bool is not treated as numeric)."""
        with pytest.raises(ValueError, match="Both base and exponent must be numeric"):
            power(True, 2)

    def test_bool_exponent_raises_value_error(self):
        """Verify that a boolean exponent raises ValueError."""
        with pytest.raises(ValueError, match="Both base and exponent must be numeric"):
            power(2, False)


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


class TestPercentage:
    def test_basic_percentage(self):
        """Verify that 50% of 200 returns 100."""
        assert percentage(200, 50) == 100.0

    def test_zero_percent(self):
        """Verify that 0% of any value returns 0."""
        assert percentage(500, 0) == 0.0

    def test_one_hundred_percent(self):
        """Verify that 100% of a value returns the value itself."""
        assert percentage(75, 100) == 75.0

    def test_negative_value(self):
        """Verify that percentage works correctly with a negative base value."""
        assert percentage(-200, 25) == -50.0

    def test_negative_percent(self):
        """Verify that a negative percent produces a negative result."""
        assert percentage(200, -10) == -20.0

    def test_non_numeric_value_raises_value_error(self):
        """Verify that a non-numeric value argument raises ValueError."""
        with pytest.raises(ValueError, match="Both value and percent must be numeric"):
            percentage("abc", 10)

    def test_non_numeric_percent_raises_value_error(self):
        """Verify that a non-numeric percent argument raises ValueError."""
        with pytest.raises(ValueError, match="Both value and percent must be numeric"):
            percentage(100, "fifty")

    def test_bool_value_raises_value_error(self):
        """Verify that a boolean value argument raises ValueError (bool is not numeric here)."""
        with pytest.raises(ValueError, match="Both value and percent must be numeric"):
            percentage(True, 10)

    def test_bool_percent_raises_value_error(self):
        """Verify that a boolean percent argument raises ValueError."""
        with pytest.raises(ValueError, match="Both value and percent must be numeric"):
            percentage(100, False)


class TestFactorial:
    def test_factorial_zero_returns_one(self):
        """Verify that factorial(0) returns 1 (base case)."""
        assert factorial(0) == 1

    def test_factorial_five(self):
        """Verify that factorial(5) returns 120."""
        assert factorial(5) == 120

    def test_factorial_ten(self):
        """Verify that factorial(10) returns 3628800."""
        assert factorial(10) == 3628800

    def test_negative_input_raises_value_error(self):
        """Verify that a negative integer raises ValueError."""
        with pytest.raises(ValueError):
            factorial(-1)

    def test_float_input_raises_value_error(self):
        """Verify that a float input raises ValueError (floats are not integers)."""
        with pytest.raises(ValueError):
            factorial(5.0)

    def test_exceeds_max_raises_value_error(self):
        """Verify that n > MAX_FACTORIAL_INPUT raises ValueError."""
        with pytest.raises(ValueError):
            factorial(calc.MAX_FACTORIAL_INPUT + 1)

    def test_max_allowed_input_does_not_raise(self):
        """Verify that factorial(MAX_FACTORIAL_INPUT) runs without error."""
        result = factorial(calc.MAX_FACTORIAL_INPUT)
        assert result > 0


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
