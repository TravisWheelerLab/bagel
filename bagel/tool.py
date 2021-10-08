from typing import IO, Dict, Iterable, List, NamedTuple, TextIO, Union


class Tool(NamedTuple):
    """
    A tool that can run against compatible benchmarks.
    """
    name: str
    version: str
    benchmarks: Iterable[str]
    image: str

    def __str__(self) -> str:
        return f"{self.name}\t{self.version}\t{', '.join(self.benchmarks)}"


def load_tool(file: IO) -> Tool:
    """
    Load a tool metadata object from its JSON file. Raises a ``ValueError``
    if the object is malformed in any way. Use ``validate_tool`` to get
    more information about an error.

    TODO Adjust file paths to be relative to the metadata file location
    """
    import json

    try:
        tool_meta = json.load(file)
        return Tool(**tool_meta)
    except:
        raise ValueError()


def validate_tool(data: Union[IO, Dict]) -> List[str]:
    """
    Validate a tool metadata object in JSON format or a pre-loaded
    dictionary. This includes verifying that all required fields exist and that
    they are of the correct types.
    """
    import json
    from json.decoder import JSONDecodeError

    if isinstance(data, dict):
        tool_meta = data
    else:
        try:
            tool_meta = json.load(data)
        except JSONDecodeError as err:
            return [f"invalid JSON object: line {err.lineno}"]

    if not isinstance(tool_meta, dict):
        return [f"invalid JSON object: type is {type(tool_meta)}"]

    fields = [
        ("name", str),
        ("version", str),
        ("families", list),
        ("image", str),
        ("results", dict),
    ]

    msgs = []

    for key, dt in fields:
        if key not in tool_meta:
            msgs.append(f"required field not found: {key}")
            continue
        if not isinstance(tool_meta[key], dt):
            msgs.append(f"incorrect field type ({type(tool_meta[key])}): {key}")

    if msgs:
        return msgs

    for bmark_family in tool_meta["families"]:
        if not isinstance(bmark_family, str):
            msgs.append(
                f"incorrect benchmark family type ({type(bmark_family)}): {bmark_family}"
            )

    for key, value in tool_meta["results"].items():
        if not isinstance(key, str):
            msgs.append(f"incorrect results key type ({type(key)}): {key}")
        if not isinstance(value, str):
            msgs.append(f"incorrect results value type ({type(value)}): {key}")

    return msgs
