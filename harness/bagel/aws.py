from typing import NamedTuple


class AWSBatchConfig(NamedTuple):
    bucket: str
    cli_path: str
    queue: str
    region: str
