from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aspy_dependency_injection._service_lookup._call_site_kind import CallSiteKind
    from aspy_dependency_injection._service_lookup._result_cache import ResultCache


class ServiceCallSite(ABC):
    """Representation of how a service must be created."""

    @property
    @abstractmethod
    def cache(self) -> ResultCache: ...

    @property
    @abstractmethod
    def service_type(self) -> type: ...

    @property
    @abstractmethod
    def kind(self) -> CallSiteKind: ...
