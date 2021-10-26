from typing import IO, Dict, Iterable, List, NamedTuple, Union, Tuple, Optional

from .stage import Stage


class Tool(NamedTuple):
    """
    A representation of a search tool metadata document.
    """

    name: str
    version: str

    families: Iterable[Tuple[str, str]]

    image: str
    results: Dict[str, str]

    stages: Iterable[Stage]

    @staticmethod
    def header() -> str:
        return "\t".join(
            [
                "Name",
                "Version",
            ]
        )

    def __str__(self) -> str:
        return "\t".join(
            [
                self.name,
                self.version,
            ]
        )


def load_tool(file: IO) -> Tool:
    pass


def validate_tool(file: Union[IO, Dict]) -> List[str]:
    pass
