from .cli import FAIL_CODE, run_cli
from .exceptions import CLIError
from .logger import get_logger
from .parameters import parse_args


def main():
    from sys import argv

    ns = parse_args(argv[1:])

    try:
        return_code = run_cli(ns)
    except CLIError as err:
        get_logger().fatal(err.args[0])
        return_code = FAIL_CODE
    except FileNotFoundError as err:
        get_logger().fatal(f"File not found: {err.filename}")
        return_code = FAIL_CODE

    exit(return_code)


if __name__ == "__main__":
    main()
