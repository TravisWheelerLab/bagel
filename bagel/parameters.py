from argparse import ArgumentParser, Namespace
from typing import List, Tuple


def _comma_tuple(arg: str) -> Tuple[str, ...]:
    """
    A "type" that can be used with ``ArgumentParser`` to split a
    comma-delimited list of values into an actual list.
    """
    return tuple((a.strip() for a in arg.split(",") if a.strip() != ""))


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser("benchmarks.py")
    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="command",
    )

    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Run in debug mode to produce additional output",
    )

    run_parser = subparsers.add_parser("run")

    run_parser.add_argument(
        "--benchmark",
        "-b",
        default="transmark",
        choices=("transmark",),
        metavar="NAME",
        help="The benchmarks to run",
    )
    run_parser.add_argument(
        "--tools",
        "-t",
        default=(),
        type=_comma_tuple,
        metavar="LIST",
        help="A list of tools (directories of metadata files) to "
        + "run against the selected benchmarks",
    )

    run_subparsers = run_parser.add_subparsers(
        title="environment",
        dest="environment",
    )

    aws_parser = run_subparsers.add_parser("aws")
    aws_parser.add_argument(
        "--bucket",
        required=True,
        metavar="NAME",
        help="AWS S3 bucket to use as the working directory",
    )
    aws_parser.add_argument(
        "--cli-path",
        default="/home/ec2-user/miniconda/bin/aws",
        metavar="PATH",
        help="Path to the aws command within the Batch instance AMI",
    )
    aws_parser.add_argument(
        "--queue",
        required=True,
        metavar="NAME",
        help="AWS Batch queue to use for benchmark jobs",
    )
    aws_parser.add_argument(
        "--region",
        default="us-east-1",
        metavar="NAME",
        help="AWS region to create resources in",
    )

    list_benchmarks_parser = subparsers.add_parser("benchmarks")

    list_tools_parser = subparsers.add_parser("tools")

    list_tools_parser.add_argument(
        "--benchmark",
        "-b",
        default="transmark",
        choices=("transmark",),
        metavar="NAME",
        help="Show tools compatible with a particular benchmark",
    )

    return parser.parse_args(args)
