from typing import Iterable

from .aws import AWSBatchConfig
from .benchmark import Benchmark
from .benchmarks import BENCHMARKS
from .tool import Tool
from .tools import TOOLS


def benchmarks_add() -> None:
    pass


def benchmarks_list() -> None:
    print("NAME\tFAMILY\tVERSION")
    for bmark in BENCHMARKS:
        print(bmark)


def benchmarks_validate(benchmark: Benchmark) -> None:
    pass


def run_aws_batch(
    aws: AWSBatchConfig,
    benchmark: Benchmark,
    tools: Iterable[Tool],
    debug: bool,
) -> None:
    pass


def run_docker(
    benchmark: Benchmark,
    tools: Iterable[Tool],
    debug: bool,
) -> None:
    pass


def tools_list() -> None:
    print("NAME\tVERSION\tBENCHMARKS")
    for tool in TOOLS:
        print(tool)


def tools_validate(tool: Tool) -> None:
    pass
