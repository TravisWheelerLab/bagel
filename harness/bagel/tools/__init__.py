from ..tool import Tool


TOOLS = [
    Tool(
        name="mock-search",
        version="1.0.0",
        image="traviswheelerlab/bagel-mock-search:1.0.0",
        benchmarks=["transmark"],
    ),
]
