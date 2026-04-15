"""Simple arithmetic calculator CLI using argparse."""

import argparse
import math
import sys


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


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b. Exits with code 1 on division by zero."""
    # ST5 Validated
    if b == 0:
        print("Error: division by zero", file=sys.stderr)
        sys.exit(1)
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

    return parser


def main() -> None:
    """Entry point: parse args, dispatch to the appropriate arithmetic function."""
    # ST5 Validated
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "power":
        result = power(args.base, args.exponent)
        print(result)
        return

    if args.command == "sqrt":
        result = sqrt(args.number)
        print(result)
        return

    operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }
    result = operations[args.command](args.a, args.b)
    print(result)


if __name__ == "__main__":
    main()
