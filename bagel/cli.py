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
from .benchmark import load_benchmark
from .exceptions import BackendError, CLIError, UnsupportedEnvironment
from .logger import configure_logger, get_logger
from .tool import load_tool


FAIL_CODE = 100


def run_cli(ns: Namespace) -> int:
    configure_logger(ns.quiet, ns.debug, ns.verbose)

    if ns.command == "run":
        with open(ns.benchmark, "r") as bmark_file:
            try:
                benchmark = load_benchmark(bmark_file)
            except ValueError:
                raise CLIError(f"Failed to load benchmark from {ns.benchmark}")

        tools = []
        for tool_path in ns.tools:
            with open(tool_path, "r") as tool_file:
                try:
                    tool = load_tool(tool_file)
                except ValueError:
                    raise CLIError(f"Failed to load tool from {tool_path}")
            tools.append(tool)

        try:
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
                )
            if ns.environment == "docker":
                run_docker(
                    benchmark=benchmark,
                    tools=tools,
                )
        except UnsupportedEnvironment:
            raise CLIError(f"Backend does not support {ns.environment} environment")
        except BackendError as err:
            raise CLIError(f"Backend {err.name} failed with message:\n{err.message}")

    if ns.command == "benchmarks":
        if ns.list:
            available_bmarks = benchmarks_list()
            if available_bmarks:
                print("NAME\tFAMILY\tVERSION")
            for bmark in available_bmarks:
                print(bmark)

        if ns.validate:
            if ns.list:
                get_logger().warn("Ignoring --validate because --list was passed")
            else:
                errors = benchmarks_validate(ns.validate)
                for error in errors:
                    print(error)
                if errors:
                    return FAIL_CODE

    if ns.command == "tools":
        if ns.list:
            available_tools = tools_list()
            if available_tools:
                print("NAME\tVERSION\tBENCHMARKS")
            for tool in available_tools:
                print(tool)

        if ns.validate:
            if ns.list:
                get_logger().warn("Ignoring --validate because --list was passed")
            else:
                errors = tools_validate(ns.validate)
                for error in errors:
                    print(error)
                if errors:
                    return FAIL_CODE

    return 0
