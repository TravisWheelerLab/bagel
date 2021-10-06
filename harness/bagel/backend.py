from abc import ABC, abstractmethod
from subprocess import run, SubprocessError
from typing import Iterable

from .aws import AWSBatchConfig
from .benchmark import Benchmark
from .logger import get_logger
from .tool import Tool


class Backend(ABC):
    @abstractmethod
    def run_aws(
        aws: AWSBatchConfig,
        benchmark: Benchmark,
        tools: Iterable[Tool],
    ) -> None:
        ...

    @abstractmethod
    def run_docker(
        benchmark: Benchmark,
        tools: Iterable[Tool],
    ) -> None:
        ...


class NextflowBackend(Backend):
    def run_aws(
        aws: AWSBatchConfig,
        benchmark: Benchmark,
        tools: Iterable[Tool],
    ) -> None:
        from subprocess import run

        # TODO: Fan out all tools
        # Probably end up doing this by spawning multiple subprocesses
        # asynchronously and waiting for them all to finish.

        for tool in tools:
            args = [
                "nextflow",
                "run",
                f"{benchmark.family}-workflow.nf",
                "-process.executor",
                "awsbatch",
                "-process.queue",
                aws.queue,
                "-process.container",
                tool.container,
                "-aws.region",
                aws.region,
                "-aws.batch.cliPath",
                aws.cli_path,
                "-work-dir",
                aws.bucket,
            ]

            for key, value in benchmark.files.items():
                args.append(f"--{key}={value}")

            logger = get_logger()
            logger.debug(f'running command: {" ".join(args)}')

            try:
                proc = run(
                    args,
                    capture_output=True,
                    check=True,
                    text=True,
                )
            except SubprocessError:
                logger.fatal(f"failed to execute tool: {tool.name}", exc_info=True)
                return

            logger.debug("runner return code: %s", proc.returncode)
            logger.debug("runner stdout:\n%s", proc.stdout)
            logger.debug("runner stderr:\n%s", proc.stderr)

    def run_docker(
        benchmark: Benchmark,
        tools: Iterable[Tool],
    ) -> None:
        pass
