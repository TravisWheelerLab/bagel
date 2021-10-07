from typing import IO, Dict, List, NamedTuple, TextIO, Union


class Benchmark(NamedTuple):
    """
    A benchmark (dataset) that can have compatible tools run against it.
    """

    family: str
    name: str
    version: str
    image: str
    data: Dict[str, str]

    def __str__(self) -> str:
        return f"{self.name}\t{self.family}\t{self.version}"


def load_benchmark(file: IO) -> Benchmark:
    """
    Load a benchmark metadata object from its JSON file. Raises a ``ValueError``
    if the object is malformed in any way. Use ``validate_benchmark`` to get
    more information about an error.

    TODO Adjust file paths to be relative to the metadata file location
    """
    import json

    try:
        bmark = json.load(file)
        return Benchmark(**bmark)
    except:
        raise ValueError()


def validate_benchmark(data: Union[IO, Dict]) -> List[str]:
    """
    Validate a benchmark metadata object in JSON format or a pre-loaded
    dictionary. This includes verifying that all required fields exist and that
    they are of the correct types.
    """
    import json
    from json.decoder import JSONDecodeError

    if isinstance(data, dict):
        bmark = data
    else:
        try:
            bmark = json.load(data)
        except JSONDecodeError as err:
            return [f"invalid JSON object: line {err.lineno}"]

    if not isinstance(bmark, dict):
        return [f"invalid JSON object: type is {type(bmark)}"]

    fields = [
        ("family", str),
        ("name", str),
        ("version", str),
        ("image", str),
        ("data", dict),
    ]

    msgs = []

    for key, dt in fields:
        if key not in bmark:
            msgs.append(f"required field not found: {key}")
            continue
        if not isinstance(bmark[key], dt):
            msgs.append(f"incorrect field type ({type(bmark[key])}): {key}")

    if msgs:
        return msgs

    for key, value in bmark["files"].items():
        if not isinstance(key, str):
            msgs.append(f"incorrect files key type ({type(key)}): {key}")
        if not isinstance(value, str):
            msgs.append(f"incorrect files value type ({type(value)}): {key}")

    return msgs
