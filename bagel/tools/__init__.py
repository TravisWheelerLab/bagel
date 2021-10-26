from typing import Optional

from ..metadata.stage import Stage
from ..metadata.tool import Tool


TOOLS = [
    Tool(
        name="mock-search",
        version="1.0.0",
        families=[("transmark", "1.0.0")],
        image="traviswheelerlab/bagel-mock-search:1.0.0",
        results={
            "matches": "matches.tar.gz",
        },
        stages=[
            Stage("prepare_data", False),
            Stage("run_tool", True),
        ],
    ),
]


def get_tool(name: str) -> Optional[Tool]:
    for tool in TOOLS:
        if tool.name == name:
            return tool
    return None
