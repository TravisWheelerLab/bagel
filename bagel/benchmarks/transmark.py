from ..metadata.benchmark import Benchmark
from ..metadata.stage import Stage

PID60 = Benchmark(
    name="60% ID",
    version="1.0.0",
    family_name="transmark",
    family_version="1.0.0",
    image="traviswheelerlab/bagel-transmark:1.0.0",
    data={
        "queries_dna": "",
        "queries_protein": "",
        "targets": "",
    },
    stages=[
        Stage("post_process", True),
        Stage("collect_results", False),
    ],
)
