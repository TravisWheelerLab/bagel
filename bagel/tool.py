from typing import IO, Dict, Iterable, List, NamedTuple, TextIO, Union


class Tool(NamedTuple):
    name: str
    version: str
    benchmarks: Iterable[str]
    image: str

    def __str__(self) -> str:
        return f"{self.name}\t{self.version}\t{', '.join(self.benchmarks)}"


def load_tool(file: IO) -> Tool:
    pass


def validate_tool(file: Union[IO, Dict]) -> List[str]:
    pass
