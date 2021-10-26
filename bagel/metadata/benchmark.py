from typing import IO, Dict, List, NamedTuple, Union, Iterable, Tuple, Any

from .stage import Stage


class Benchmark(NamedTuple):
    """
    A benchmark (dataset) that can have compatible tools run against it.
    """

    name: str
    version: str

    family_name: str
    family_version: str

    image: str
    data: Dict[str, str]

    stages: Iterable[Stage]

    @staticmethod
    def load(data: Union[IO, Dict]) -> "Benchmark":
        """
        Load a benchmark from JSON data either as a dictionary or a file.

        >>> m = {
        ...     "name": "foo",
        ...     "version": "1.0.0",
        ...     "family_name": "bar",
        ...     "family_version": "1.0.0",
        ...     "image": "user/image:1.0.0",
        ...     "data": {"baz": "baz.txt"},
        ...     "stages": [
        ...         {"name": "stage1", "parallel": True},
        ...         {"name": "stage2", "parallel": False},
        ...     ],
        ... }
        >>> b = Benchmark.load(m)
        >>> b.name
        'foo'
        >>> list(b.stages)[0].name
        'stage1'
        """
        import json
        from json.decoder import JSONDecodeError

        if isinstance(data, dict):
            bmark = data
        else:
            try:
                bmark = json.load(data)
            except JSONDecodeError as err:
                raise ValueError() from err

        bmark["stages"] = [Stage(**s) for s in bmark["stages"]]

        return Benchmark(**bmark)

    @staticmethod
    def validate(data: Union[IO, Dict]) -> List[str]:
        """
        Validate a benchmark metadata object in JSON format or a pre-loaded
        dictionary. This includes verifying that all required fields exist and
        that they are of the correct types.
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
            ("name", str),
            ("version", str),
            ("family_name", str),
            ("family_version", str),
            ("image", str),
            ("data", dict),
            ("stages", list),
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

        for key, value in bmark["data"].items():
            if not isinstance(key, str):
                msgs.append(f"incorrect files key type ({type(key)}): {key}")
            if not isinstance(value, str):
                msgs.append(f"incorrect files value type ({type(value)}): {key}")

        # TODO: Add validation for stages

        return msgs

    @staticmethod
    def header() -> str:
        return "\t".join(
            [
                "Name",
                "Version",
                "Family Name",
                "Family Version",
            ]
        )

    def row(self) -> str:
        return "\t".join(
            [
                self.name,
                self.version,
                self.family_name,
                self.family_version,
            ]
        )

    def json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "family_name": self.family_name,
            "family_version": self.family_version,
            "image": self.image,
            "data": self.data,
            "stages": [s.json() for s in self.stages],
        }
