from typing import NamedTuple, Any, Dict


class Stage(NamedTuple):
    """
    A single stage within a multi-stage pipeline.
    """

    name: str
    parallel: bool

    def json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "parallel": self.parallel,
        }
