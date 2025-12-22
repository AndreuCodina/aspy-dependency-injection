from aspy_dependency_injection.abstractions.service_provider import ServiceProvider


class ObjectDisposedError(Exception):
    """The exception that is thrown when an operation is performed on a disposed object."""

    def __init__(self) -> None:
        super().__init__(ServiceProvider.__name__)
