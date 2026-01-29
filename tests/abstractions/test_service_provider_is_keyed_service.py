from wirio.abstractions.service_container_is_keyed_service import (
    ServiceContainerIsKeyedService,
)
from wirio.service_container import ServiceContainer


class TestServiceProviderIsKeyedService:
    async def test_resolve_service_provider_is_keyed_service(self) -> None:
        service_container = ServiceContainer()

        async with service_container:
            service_scope_factory = await service_container.get(
                ServiceContainerIsKeyedService
            )

            assert isinstance(service_scope_factory, ServiceContainerIsKeyedService)
