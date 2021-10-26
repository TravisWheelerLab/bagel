from typing import Optional

from .transmark import *


BENCHMARKS = [
    # Transmark
    PID60,
]


def get_benchmark(name: str) -> Optional[Benchmark]:
    for bmark in BENCHMARKS:
        if bmark.name == name:
            return bmark
    return None
