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

    parser.add_argument(
        "--quiet",
        default=False,
        action="store_true",
        help="Suppress all output",
    )
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Produce all possible output, useful for debugging "
        + "tools and benchmarks",
    )
    parser.add_argument(
        "--verbose",
        default=False,
        action="store_true",
        help="Produce extra output useful for monitoring jobs",
    )

    root_subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
    )

    # ----------------------------------
    # run
    # ----------------------------------

    run_parser = root_subparsers.add_parser("run")

    run_parser.add_argument(
        "--benchmark",
        "-b",
        required=True,
        metavar="NAME",
        help="The benchmarks to run",
    )
    run_parser.add_argument(
        "--tools",
        "-t",
        required=True,
        type=_comma_tuple,
        metavar="LIST",
        help="A list of tools (metadata files), comma-separated, to "
        + "run against the selected benchmarks",
    )
    run_parser.add_argument(
        "--backend",
        default="nextflow",
        choices=("nextflow",),
        metavar="NAME",
        help="The backend to use for execution, note that not all backends "
        + "necessarily support all execution environments",
    )

    run_subparsers = run_parser.add_subparsers(
        title="environment",
        dest="environment",
    )

    # ----------------------------------
    # run ... aws
    # ----------------------------------

    aws_batch_parser = run_subparsers.add_parser("aws_batch")

    aws_batch_parser.add_argument(
        "--bucket",
        required=True,
        metavar="NAME",
        help="AWS S3 bucket to use as the working directory",
    )
    aws_batch_parser.add_argument(
        "--cli-path",
        default="/home/ec2-user/miniconda/bin/aws",
        metavar="PATH",
        help="Path to the aws command within the Batch instance AMI",
    )
    aws_batch_parser.add_argument(
        "--queue",
        required=True,
        metavar="NAME",
        help="AWS Batch queue to use for benchmark jobs",
    )
    aws_batch_parser.add_argument(
        "--region",
        default="us-east-1",
        metavar="NAME",
        help="AWS region to create resources in",
    )

    # ----------------------------------
    # run ... docker
    # ----------------------------------

    docker_parser = run_subparsers.add_parser("docker")

    # ----------------------------------
    # benchmarks
    # ----------------------------------

    benchmarks_parser = root_subparsers.add_parser(
        "benchmarks",
        description="manipulate benchmark definitions",
    )

    benchmarks_parser.add_argument(
        "--list",
        default=False,
        action="store_true",
        help="list built-in benchmarks",
    )

    benchmarks_parser.add_argument(
        "--validate",
        default="",
        metavar="PATH",
        help="validate the given benchmark metadata file",
    )

    # ----------------------------------
    # tools
    # ----------------------------------

    tools_parser = root_subparsers.add_parser(
        "tools",
        description="manipulate tool definitions",
    )

    tools_parser.add_argument(
        "--list",
        default=False,
        action="store_true",
        help="list built-in tools",
    )

    tools_parser.add_argument(
        "--validate",
        default="",
        metavar="PATH",
        help="validate the given tool metadata file",
    )

    return parser.parse_args(args)
