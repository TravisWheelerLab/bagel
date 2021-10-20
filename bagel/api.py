from typing import Iterable

from .aws import AWSBatchConfig
from .backend import NextflowBackend
from .benchmark import Benchmark, validate_benchmark
from .benchmarks import BENCHMARKS
from .tool import Tool, validate_tool
from .tools import TOOLS


def benchmarks_list() -> Iterable[Benchmark]:
    """
    Produce a list of the available benchmarks.
    """
    return BENCHMARKS


def benchmarks_validate(bmark_path: str) -> Iterable[str]:
    """
    Validate the benchmark metadata document pointed to by the given path.
    """
    with open(bmark_path, "r") as bmark_file:
        errors = validate_benchmark(bmark_file)

    return errors


def run_aws_batch(
    aws: AWSBatchConfig,
    benchmark: Benchmark,
    tools: Iterable[Tool],
) -> None:
    """
    Run a benchmark on AWS Batch.
    """
    backend = NextflowBackend()
    backend.run_aws_batch(
        aws=aws,
        benchmark=benchmark,
        tools=tools,
    )


def run_docker(
    benchmark: Benchmark,
    tools: Iterable[Tool],
) -> None:
    """
    Run a benchmark locally using Docker.
    """
    backend = NextflowBackend()
    backend.run_docker(
        benchmark=benchmark,
        tools=tools,
    )


def tools_list() -> Iterable[Tool]:
    """
    Produce a list of available tools.
    """
    return TOOLS


def tools_validate(tool_path: str) -> Iterable[str]:
    """
    Validate the tool metadata document pointed to by the given path.
    """
    with open(tool_path, "r") as tool_file:
        errors = validate_tool(tool_file)

    return errors
