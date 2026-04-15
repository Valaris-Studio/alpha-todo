"""Simple arithmetic calculator CLI using argparse."""

import argparse
import math
import os
import sys

HISTORY_FILE = os.path.expanduser("~/.calc_history")


def _validate_numeric(value: object, name: str) -> None:
    """Raise TypeError if value is not int or float (bool excluded)."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{name} must be int or float, got {type(value).__name__}")


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    _validate_numeric(a, "a")
    _validate_numeric(b, "b")
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a minus b."""
    _validate_numeric(a, "a")
    _validate_numeric(b, "b")
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    _validate_numeric(a, "a")
    _validate_numeric(b, "b")
    return a * b


DIVISION_BY_ZERO_MESSAGE = "Division by zero is not allowed"


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b. Raises ValueError on division by zero."""
    _validate_numeric(a, "a")
    _validate_numeric(b, "b")
    if b == 0:
        raise ValueError(DIVISION_BY_ZERO_MESSAGE)
    return a / b


def power(base: float, exponent: float) -> float:
    """Return base raised to the power of exponent."""
    # ST5 Validated
    return base ** exponent


def sqrt(number: float) -> float:
    """Return the square root of number. Exits with code 1 for negative input."""
    # ST5 Validated
    if number < 0:
        print("Error: square root of negative number", file=sys.stderr)
        sys.exit(1)
    return math.sqrt(number)


def modulus(a: float, b: float) -> float:
    """Return the remainder of a divided by b. Raises ValueError when b is zero."""
    _validate_numeric(a, "a")
    _validate_numeric(b, "b")
    if b == 0:
        raise ValueError("Modulus by zero is not allowed")
    return a % b


def absolute(number: float) -> float:
    """Return the absolute value of number."""
    # ST5 Validated
    return abs(number)


def append_history(expression: str, result: float) -> None:
    """Append a calculation entry to ~/.calc_history in 'expr=result' format."""
    # ST5 Validated
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{expression}={result}\n")


def show_history(last: int) -> None:
    """Print the last N entries from ~/.calc_history."""
    # ST5 Validated
    if not os.path.exists(HISTORY_FILE):
        print("No history found.")
        return
    if last <= 0:
        return
    with open(HISTORY_FILE, "r") as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]
    for entry in lines[-last:]:
        print(entry)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser with arithmetic subcommands."""
    # ST5 Validated
    parser = argparse.ArgumentParser(description="Simple arithmetic calculator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for cmd in ("add", "subtract", "multiply", "divide"):
        sub = subparsers.add_parser(cmd, help=f"Perform {cmd} on two numbers")
        sub.add_argument("a", type=float, help="First operand")
        sub.add_argument("b", type=float, help="Second operand")

    power_sub = subparsers.add_parser("power", help="Raise base to an exponent")
    power_sub.add_argument("base", type=float, help="Base number")
    power_sub.add_argument("exponent", type=float, help="Exponent")

    sqrt_sub = subparsers.add_parser("sqrt", help="Compute square root of a number")
    sqrt_sub.add_argument("number", type=float, help="Number to take square root of")

    mod_sub = subparsers.add_parser("mod", help="Compute a modulo b")
    mod_sub.add_argument("a", type=float, help="Dividend")
    mod_sub.add_argument("b", type=float, help="Divisor")

    abs_sub = subparsers.add_parser("abs", help="Compute absolute value of a number")
    abs_sub.add_argument("number", type=float, help="Number to take absolute value of")

    history_sub = subparsers.add_parser("history", help="Show recent calculation history")
    history_sub.add_argument(
        "--last", type=int, default=10, metavar="N",
        help="Number of most recent entries to show (default: 10)"
    )

    return parser


def main() -> None:
    """Entry point: parse args, dispatch to the appropriate arithmetic function."""
    # ST5 Validated
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "history":
        show_history(args.last)
        return

    if args.command == "power":
        result = power(args.base, args.exponent)
        print(result)
        append_history(f"{args.base}**{args.exponent}", result)
        return

    if args.command == "sqrt":
        result = sqrt(args.number)
        print(result)
        append_history(f"sqrt({args.number})", result)
        return

    if args.command == "mod":
        result = modulus(args.a, args.b)
        print(result)
        append_history(f"{args.a}%{args.b}", result)
        return

    if args.command == "abs":
        result = absolute(args.number)
        print(result)
        append_history(f"abs({args.number})", result)
        return

    operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }
    op_symbols = {"add": "+", "subtract": "-", "multiply": "*", "divide": "/"}
    try:
        result = operations[args.command](args.a, args.b)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    print(result)
    append_history(f"{args.a}{op_symbols[args.command]}{args.b}", result)


if __name__ == "__main__":
    main()
