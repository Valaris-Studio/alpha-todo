"""Simple arithmetic calculator CLI using argparse."""

import argparse
import math
import os
import sys

HISTORY_FILE = os.path.expanduser("~/.calc_history")


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    # ST5 Validated
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a minus b."""
    # ST5 Validated
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    # ST5 Validated
    return a * b


DIVISION_BY_ZERO_MESSAGE = "Division by zero is not allowed"


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b. Raises ValueError on division by zero."""
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


def modulo(a: float, b: float) -> float:
    """Return a modulo b. Exits with code 1 on division by zero."""
    # ST5 Validated
    if b == 0:
        print("Error: modulo by zero", file=sys.stderr)
        sys.exit(1)
    return a % b


def absolute(number: float) -> float:
    """Return the absolute value of number."""
    # ST5 Validated
    return abs(number)


PERCENTAGE_NON_NUMERIC_MESSAGE = "Both value and percent must be numeric"

MAX_FACTORIAL_INPUT = 170
FACTORIAL_NEGATIVE_MESSAGE = "n must be a non-negative integer"
FACTORIAL_NON_INTEGER_MESSAGE = "n must be a non-negative integer"
FACTORIAL_OVERFLOW_MESSAGE = f"n must not exceed {MAX_FACTORIAL_INPUT}"


def factorial(n: int) -> int:
    """Return n! (n factorial) using iteration.

    Raises ValueError if n is negative, not an integer, or exceeds MAX_FACTORIAL_INPUT.
    Returns 1 for factorial(0).
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError(FACTORIAL_NON_INTEGER_MESSAGE)
    if n < 0:
        raise ValueError(FACTORIAL_NEGATIVE_MESSAGE)
    if n > MAX_FACTORIAL_INPUT:
        raise ValueError(FACTORIAL_OVERFLOW_MESSAGE)
    result = 1
    for factor in range(2, n + 1):
        result *= factor
    return result


def percentage(value: float, percent: float) -> float:
    """Return the given percent of value (i.e. value * percent / 100).

    Raises ValueError if either argument is not numeric.
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(PERCENTAGE_NON_NUMERIC_MESSAGE)
    if not isinstance(percent, (int, float)) or isinstance(percent, bool):
        raise ValueError(PERCENTAGE_NON_NUMERIC_MESSAGE)
    return value * percent / 100


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

    pct_sub = subparsers.add_parser("percentage", help="Compute percent of a value")
    pct_sub.add_argument("value", type=float, help="Base value")
    pct_sub.add_argument("percent", type=float, help="Percentage to compute")

    factorial_sub = subparsers.add_parser("factorial", help="Compute factorial of a non-negative integer")
    factorial_sub.add_argument("n", type=int, help="Non-negative integer")

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

    if args.command == "factorial":
        try:
            result = factorial(args.n)
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
        print(result)
        append_history(f"factorial({args.n})", result)
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
        result = modulo(args.a, args.b)
        print(result)
        append_history(f"{args.a}%{args.b}", result)
        return

    if args.command == "abs":
        result = absolute(args.number)
        print(result)
        append_history(f"abs({args.number})", result)
        return

    if args.command == "percentage":
        result = percentage(args.value, args.percent)
        print(result)
        append_history(f"{args.percent}%of{args.value}", result)
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
