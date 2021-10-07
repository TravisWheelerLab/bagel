from typing import NamedTuple


class AWSBatchConfig(NamedTuple):
    """
    Configuration for running jobs using AWS Batch.
    """

    bucket: str
    """
    The bucket to use for intermediate storage and results.
    """

    cli_path: str
    """
    The path to the ``aws`` command line application within the Batch AMI.  This
    is specifically required by the Nextflow backend, see the Nextflow
    documentation for instructions on how to construct a compatible AMI.
    """

    queue: str
    """
    The Batch queue name that will accept jobs.
    """

    region: str
    """
    The default region to use, defaults to ``us-east-1``.
    """
