from logging import DEBUG, FATAL, INFO, WARNING, Logger, StreamHandler, getLogger


def get_logger() -> Logger:
    """
    Return the global application logger.
    """
    return getLogger("bagel")


def configure_logger(
    quiet: bool,
    debug: bool,
    verbose: bool,
) -> None:
    """
    Configure the global application logger. If ``quiet`` is ``True``, then it
    will always win, regardless of the other parameter values. Otherwise,
    ``debug`` wins over ``verbose`` since the former includes the latter.

    >>> configure_logger(True, True, True)
    >>> l = getLogger("bagel")
    >>> l.level
    50
    >>> configure_logger(False, True, True)
    >>> l.level
    10
    >>> configure_logger(False, False, True)
    >>> l.level
    20
    >>> configure_logger(False, False, False)
    >>> l.level
    30
    """
    logger = getLogger("bagel")

    if quiet:
        logger.setLevel(FATAL)
    elif debug:
        logger.setLevel(DEBUG)
    elif verbose:
        logger.setLevel(INFO)
    else:
        logger.setLevel(WARNING)

    if not quiet:
        logger.addHandler(StreamHandler())
