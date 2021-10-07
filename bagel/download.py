from pathlib import Path
from shutil import copyfileobj
from typing import Optional
from urllib.error import URLError
from urllib.request import urlopen

from .logger import get_logger


def fetch_file(
    url: str,
    dest_path: Path,
) -> Optional[Path]:
    """
    Efficiently download the file located at the given URL, saving it to the
    destination path provided. The path to the downloaded file itself is
    returned unless an error occurs, then ``None`` is returned.

    If the destination file already exists, then the path is returned
    immediately and no download happens.
    """
    if dest_path.exists():
        return dest_path

    try:
        with urlopen(url) as resp, open(dest_path, "wb") as dest_file:
            copyfileobj(resp, dest_file)
    except URLError as err:
        logger = get_logger()
        logger.debug(f"downloading {url} failed with code {err.errno}")
        return None

    return dest_path
