from ..benchmark import Benchmark


PID60 = Benchmark(
    family="transmark",
    name="60% ID",
    version="1.0.0",
    image="traviswheelerlab/bagel-transmark:1.0.0",
    data={
        "queries_dna": "",
        "queries_protein": "",
        "targets": "",
    },
)
