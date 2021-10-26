from argparse import Namespace

from .api import (
    benchmarks_list,
    benchmarks_validate,
    run_aws_batch,
    run_docker,
    tools_list,
    tools_validate,
)
from .aws import AWSBatchConfig
from .benchmarks import get_benchmark
from .exceptions import BackendError, CLIError, UnsupportedEnvironment
from .logger import configure_logger, get_logger
from .metadata.benchmark import Benchmark
from .metadata.tool import load_tool
from .tools import get_tool

FAIL_CODE = 100


def run_cli(args: Namespace) -> int:
    """
    Run the command line application given a namespace of arguments.

    The return value is set as the exit code.
    """
    configure_logger(args.quiet, args.debug, args.verbose)

    if args.command == "run":
        benchmark = get_benchmark(args.benchmark)

        if benchmark is None:
            with open(args.benchmark, "r") as bmark_file:
                try:
                    benchmark = Benchmark.load(bmark_file)
                except ValueError as err:
                    raise CLIError(
                        f"Failed to load benchmark from {args.benchmark}"
                    ) from err

        tools = []
        for tool_path in args.tools:
            tool = get_tool(tool_path)

            if tool is None:
                with open(tool_path, "r") as tool_file:
                    try:
                        tool = load_tool(tool_file)
                    except ValueError as err:
                        raise CLIError(f"Failed to load tool from {tool_path}") from err

            tools.append(tool)

        try:
            if args.environment == "aws_batch":
                config = AWSBatchConfig(
                    args.bucket,
                    args.cli_path,
                    args.queue,
                    args.region,
                )

                run_aws_batch(
                    aws=config,
                    benchmark=benchmark,
                    tools=tools,
                )
            if args.environment == "docker":
                run_docker(
                    benchmark=benchmark,
                    tools=tools,
                )
        except UnsupportedEnvironment as err:
            raise CLIError(
                f"Backend does not support {args.environment} environment"
            ) from err
        except BackendError as err:
            raise CLIError(
                f"Backend {err.name} failed with message:\n{err.message}"
            ) from err

    if args.command == "benchmarks":
        if args.list:
            available_bmarks = benchmarks_list()
            if available_bmarks:
                print("NAME\tFAMILY\tVERSION")
            for bmark in available_bmarks:
                print(bmark)

        if args.validate:
            if args.list:
                get_logger().warning("Ignoring --validate because --list was passed")
            else:
                errors = benchmarks_validate(args.validate)
                for error in errors:
                    print(error)
                if errors:
                    return FAIL_CODE

    if args.command == "tools":
        if args.list:
            available_tools = tools_list()
            if available_tools:
                print("NAME\tVERSION\tBENCHMARKS")
            for tool in available_tools:
                print(tool)

        if args.validate:
            if args.list:
                get_logger().warning("Ignoring --validate because --list was passed")
            else:
                errors = tools_validate(args.validate)
                for error in errors:
                    print(error)
                if errors:
                    return FAIL_CODE

    return 0
