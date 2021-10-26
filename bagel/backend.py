from abc import ABC, abstractmethod
from subprocess import run, SubprocessError
from typing import Iterable

from .aws import AWSBatchConfig
from .metadata.benchmark import Benchmark
from .metadata.tool import Tool
from .logger import get_logger
from .template import windowed


class Backend(ABC):
    """
    A backend translates the benchmark and tool metadata into actual
    computational processes. Each method instructs the backend to run jobs in a
    different environment. Implementations do not need to support all methods.
    Unimplemented methods should raise ``UnsupportedEnvironment``.

    TODO Add support for Azure Batch
    TODO Add support of AWS Lambda
    TODO Add support for GCP comp bio
    TODO Add support for Slurm scheduler
    """

    @abstractmethod
    def run_aws_batch(
        self,
        aws: AWSBatchConfig,
        benchmark: Benchmark,
        tools: Iterable[Tool],
    ) -> None:
        """
        Run the benchmark using AWS Batch.
        """
        ...

    @abstractmethod
    def run_docker(
        self,
        benchmark: Benchmark,
        tools: Iterable[Tool],
    ) -> None:
        """
        Run locally using the Docker runtime.

        This is primarily useful for testing, except on very powerful machines.
        """
        ...


class NextflowBackend(Backend):
    """
    A backend that uses the Nextflow workflow management system.
    """

    @staticmethod
    def _build_workflow(benchmark: Benchmark, tool: Tool) -> str:
        """
        Build the actual workflow content and return it as a string.
        """
        from jinja2 import Environment, PackageLoader

        env = Environment(
            loader=PackageLoader("bagel"),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters["windowed"] = windowed
        tmpl = env.get_template("nextflow.nf.jinja2")
        return tmpl.render(benchmark=benchmark, tool=tool)

    def run_aws_batch(
        self,
        aws: AWSBatchConfig,
        benchmark: Benchmark,
        tools: Iterable[Tool],
    ) -> None:
        # TODO: Fan out all tools
        # Probably end up doing this by spawning multiple subprocesses
        # asynchronously and waiting for them all to finish.

        for tool in tools:
            workflow = self._build_workflow(benchmark, tool)
            print(workflow)
            return
            args = [
                "nextflow",
                "run",
                f"{benchmark.family_name}-workflow.nf",
                "-process.executor",
                "awsbatch",
                "-process.queue",
                aws.queue,
                "-process.container",
                tool.image,
                "-aws.region",
                aws.region,
                "-aws.batch.cliPath",
                aws.cli_path,
                "-work-dir",
                aws.bucket,
            ]

            for key, value in benchmark.data.items():
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
        self,
        benchmark: Benchmark,
        tools: Iterable[Tool],
    ) -> None:
        # TODO: Fan out all tools
        # Probably end up doing this by spawning multiple subprocesses
        # asynchronously and waiting for them all to finish.

        for tool in tools:
            args = [
                "nextflow",
                "run",
                f"{benchmark.family_name}-workflow.nf",
                "-process.executor",
                "local",
                "-process.container",
                tool.image,
            ]

            for key, value in benchmark.data.items():
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
