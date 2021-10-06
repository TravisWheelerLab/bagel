from typing import Any, Dict, Iterable, Optional

from .benchmarks import BENCHMARKS
from .tools import TOOLS


def benchmarks_add() -> None:
    pass


def benchmarks_list() -> None:
    print("NAME\tFAMILY\tVERSION")
    for bmark in BENCHMARKS:
        print(bmark)


def run_aws(
    benchmark: str,
    cli_path: str,
    container: str,
    params: Dict[str, Any],
    queue: str,
    region: str,
    tools: Iterable[str],
    debug: bool = False,
) -> None:
    pass


def run_docker() -> None:
    pass


def tools_add() -> None:
    pass


def tools_list(benchmark: Optional[str]) -> None:
    print("NAME\tVERSION\tBENCHMARKS")
    for tool in TOOLS:
        print(tool)
