from .app import AppError, run_app
from .logger import get_logger
from .parameters import parse_args


def main():
    from sys import argv

    ns = parse_args(argv[1:])

    try:
        return_code = run_app(ns)
    except AppError as err:
        get_logger().fatal(err.args[0])
        return_code = 100
    except FileNotFoundError as err:
        get_logger().fatal(f"File not found: {err.filename}")
        return_code = 100

    exit(return_code)


if __name__ == "__main__":
    main()
