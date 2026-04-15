"""Simple arithmetic calculator CLI using argparse."""

import argparse
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


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser with arithmetic subcommands."""
    # ST5 Validated
    parser = argparse.ArgumentParser(description="Simple arithmetic calculator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for cmd in ("add", "subtract", "multiply", "divide"):
        sub = subparsers.add_parser(cmd, help=f"Perform {cmd} on two numbers")
        sub.add_argument("a", type=float, help="First operand")
        sub.add_argument("b", type=float, help="Second operand")

    return parser


def main() -> None:
    """Entry point: parse args, dispatch to the appropriate arithmetic function."""
    # ST5 Validated
    parser = build_parser()
    args = parser.parse_args()

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
