from wirio.abstractions.service_container_is_keyed_service import (
    ServiceContainerIsKeyedService,
)
from wirio.service_collection import ServiceCollection


class TestServiceProviderIsKeyedService:
    async def test_resolve_service_provider_is_keyed_service(self) -> None:
        services = ServiceCollection()

        async with services.build_service_provider() as service_provider:
            service_scope_factory = await service_provider.get(
                ServiceContainerIsKeyedService
            )

            assert isinstance(service_scope_factory, ServiceContainerIsKeyedService)
