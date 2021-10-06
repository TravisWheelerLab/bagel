from .app import run_app
from .parameters import parse_args


def main():
    from sys import argv

    ns = parse_args(argv[1:])
    run_app(ns)


if __name__ == "__main__":
    main()
