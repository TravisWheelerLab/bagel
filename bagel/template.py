from typing import Iterable, Tuple, Optional, TypeVar

T = TypeVar("T")


def windowed(values: Iterable[T]) -> Iterable[Tuple[Optional[T], T, Optional[T]]]:
    """
    Helper function to scan through stages using a three element-wide window,
    which eases template rendering.

    >>> windows = list(windowed([0, 1, 2]))
    >>> len(windows)
    3
    >>> windows[0]
    (None, 0, 1)
    >>> windows[1]
    (0, 1, 2)
    >>> windows[2]
    (1, 2, None)
    """
    curr_value = None
    next_value = None

    for value in values:
        prev_value = curr_value
        curr_value = next_value
        next_value = value

        if curr_value is None:
            continue

        assert curr_value is not None
        yield prev_value, curr_value, next_value

    prev_value = curr_value
    curr_value = next_value
    next_value = None

    assert curr_value is not None
    yield prev_value, curr_value, next_value
