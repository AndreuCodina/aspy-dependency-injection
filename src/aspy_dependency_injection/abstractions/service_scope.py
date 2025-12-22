from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aspy_dependency_injection.abstractions.base_service_provider import (
        BaseServiceProvider,
    )


class ServiceScope(AbstractAsyncContextManager["ServiceScope"], ABC):
    """Defines a disposable service scope.

    The __aexit__ method ends the scope lifetime. Once called, any scoped
    services that have been resolved from ServiceProvider will be disposed.
    """

    @property
    @abstractmethod
    def service_provider(self) -> BaseServiceProvider:
        """Gets the ServiceProvider used to resolve dependencies from the scope."""
