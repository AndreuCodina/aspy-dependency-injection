import contextlib
import importlib

from aspy_dependency_injection.types import InjectableType


def Inject() -> InjectableType:  # noqa: N802
    res = InjectableType()

    # Fastapi needs all dependencies to be wrapped with Depends.
    with contextlib.suppress(ModuleNotFoundError):

        def _inner() -> InjectableType:
            return res

        return importlib.import_module("fastapi").Depends(_inner)

    return res
