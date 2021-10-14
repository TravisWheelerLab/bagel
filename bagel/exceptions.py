class BackendError(Exception):
    """
    An error that occurred while running a backend.
    """

    name: str
    message: str

    def __init__(self, name, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.message = message


class CLIError(Exception):
    """
    An exception raised when there is an error within the CLI code. This would
    typically be something like a parameter value that didn't make sense.

    This is generally a fatal exception, although it can always be handled
    cleanly, with an error message presented to the user.
    """

    ...


class UnsupportedEnvironment(Exception):
    """
    An exception that indicates an environment has been intentionally omitted
    from an implementation of ``Backend``.
    """

    ...
