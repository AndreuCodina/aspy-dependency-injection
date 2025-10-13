from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aspy_dependency_injection.service_lifetime import ServiceLifetime


class ServiceDescriptor:
    """Service registration."""

    service_type: type[object]
    lifetime: ServiceLifetime

    def __init__(self, service_type: type, lifetime: ServiceLifetime) -> None:
        self.service_type = service_type
        self.lifetime = lifetime
