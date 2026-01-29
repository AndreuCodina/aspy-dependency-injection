from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable

from wirio._service_lookup._service_call_site import (
    ServiceCallSite,
)
from wirio.service_container_engine_scope import (
    ServiceContainerEngineScope,
)


class ServiceProviderEngine(ABC):
    @abstractmethod
    def realize_service(
        self, call_site: ServiceCallSite
    ) -> Callable[[ServiceContainerEngineScope], Awaitable[object | None]]: ...
