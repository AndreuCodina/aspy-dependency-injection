from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aspy_dependency_injection.service_provider import ServiceProvider


class ServiceScope:
    """Disposable service scope."""

    def __init__(self, service_provider: ServiceProvider) -> None:
        self.service_provider = service_provider

    def get_service(self, service_type: type) -> object | None:
        return self.service_provider.get_service(service_type)
