from argparse import Namespace

from .aws import AWSBatchConfig
from .benchmark import load_benchmark, validate_benchmark
from .commands import benchmarks_list, run_aws_batch, run_docker, tools_list
from .logger import configure_logger, get_logger
from .tool import load_tool, validate_tool


FAIL_CODE = 10


class AppError(Exception):
    pass


def run_app(ns: Namespace) -> int:
    configure_logger(ns.quiet, ns.debug, ns.verbose)

    if ns.command == "run":
        with open(ns.benchmark, "r") as bmark_file:
            try:
                benchmark = load_benchmark(bmark_file)
            except ValueError:
                raise AppError(f"failed to load benchmark from {ns.benchmark}")

        tools = []
        for tool_path in ns.tools:
            with open(tool_path, "r") as tool_file:
                try:
                    tool = load_tool(tool_file)
                except ValueError:
                    raise AppError(f"failed to load tool from {tool_path}")
            tools.append(tool)

        if ns.environment == "aws_batch":
            config = AWSBatchConfig(
                ns.bucket,
                ns.cli_path,
                ns.queue,
                ns.region,
            )

            run_aws_batch(
                aws=config,
                benchmark=benchmark,
                tools=tools,
                debug=ns.debug,
            )
        if ns.environment == "docker":
            run_docker(
                benchmark=benchmark,
                tools=tools,
                debug=ns.debug,
            )

    if ns.command == "benchmarks":
        if ns.list:
            benchmarks_list()
        if ns.validate:
            if ns.list:
                get_logger().warn("Ignoring --validate because --list was passed")
            else:
                with open(ns.validate, "r") as benchmark_file:
                    errors = validate_benchmark(benchmark_file)

                if errors:
                    for error in errors:
                        get_logger().error(error)
                        return FAIL_CODE

    if ns.command == "tools":
        if ns.list:
            tools_list()
        if ns.validate:
            if ns.list:
                get_logger().warn("Ignoring --validate because --list was passed")
            else:
                with open(ns.validate, "r") as tool_file:
                    errors = validate_tool(tool_file)

                if errors:
                    for error in errors:
                        get_logger().error(error)
                        return FAIL_CODE

    return 0
