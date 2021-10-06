from typing import Iterable, List, NamedTuple, TextIO


class Tool(NamedTuple):
    name: str
    version: str
    benchmarks: Iterable[str]
    image: str

    def __str__(self) -> str:
        return f"{self.name}\t{self.version}\t{', '.join(self.benchmarks)}"


def load_tool(file: TextIO) -> Tool:
    pass


def validate_tool(file: TextIO) -> List[str]:
    pass
