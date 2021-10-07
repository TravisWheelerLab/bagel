from typing import Iterable

from .aws import AWSBatchConfig
from .benchmark import Benchmark, validate_benchmark
from .benchmarks import BENCHMARKS
from .errors import FAIL_CODE
from .logger import get_logger
from .tool import Tool, validate_tool
from .tools import TOOLS


def benchmarks_list() -> None:
    print("NAME\tFAMILY\tVERSION")
    for bmark in BENCHMARKS:
        print(bmark)


def benchmarks_validate(bmark_path: str) -> int:
    with open(bmark_path, "r") as bmark_file:
        errors = validate_benchmark(bmark_file)

    if errors:
        for error in errors:
            get_logger().error(error)
            return FAIL_CODE

    return 0


def run_aws_batch(
    aws: AWSBatchConfig,
    benchmark: Benchmark,
    tools: Iterable[Tool],
    debug: bool,
) -> int:
    pass


def run_docker(
    benchmark: Benchmark,
    tools: Iterable[Tool],
    debug: bool,
) -> int:
    pass


def tools_list() -> None:
    print("NAME\tVERSION\tBENCHMARKS")
    for tool in TOOLS:
        print(tool)


def tools_validate(tool_path: str) -> int:
    with open(tool_path, "r") as tool_file:
        errors = validate_tool(tool_file)

    if errors:
        for error in errors:
            get_logger().error(error)
        return FAIL_CODE

    return 0
