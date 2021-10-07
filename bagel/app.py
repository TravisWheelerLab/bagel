from argparse import Namespace

from .aws import AWSBatchConfig
from .benchmark import load_benchmark
from .commands import (
    benchmarks_list,
    benchmarks_validate,
    run_aws_batch,
    run_docker,
    tools_list,
    tools_validate,
)
from .logger import configure_logger, get_logger
from .tool import load_tool


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

            return run_aws_batch(
                aws=config,
                benchmark=benchmark,
                tools=tools,
                debug=ns.debug,
            )
        if ns.environment == "docker":
            return run_docker(
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
                return benchmarks_validate(ns.validate)

    if ns.command == "tools":
        if ns.list:
            tools_list()
        if ns.validate:
            if ns.list:
                get_logger().warn("Ignoring --validate because --list was passed")
            else:
                return tools_validate(ns.validate)

    return 0
