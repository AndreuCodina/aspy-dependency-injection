from tests.utils.services import ServiceWithNoDependencies
from wirio.abstractions.service_container_is_keyed_service import (
    ServiceContainerIsKeyedService,
)
from wirio.abstractions.service_container_is_service import (
    ServiceContainerIsService,
)
from wirio.abstractions.service_scope_factory import (
    ServiceScopeFactory,
)
from wirio.base_service_container import BaseServiceContainer
from wirio.service_collection import ServiceCollection


class TestServiceProviderIsService:
    async def test_resolve_service_provider_is_service(self) -> None:
        services = ServiceCollection()

        async with services.build_service_provider() as service_provider:
            service_provider_is_service = await service_provider.get(
                ServiceContainerIsService
            )

            assert isinstance(service_provider_is_service, ServiceContainerIsService)

    async def test_built_in_services_with_is_service_returns_true(
        self,
    ) -> None:
        services = ServiceCollection()
        services.add_transient(ServiceWithNoDependencies)

        async with services.build_service_provider() as service_provider:
            service_provider_is_service = await service_provider.get(
                ServiceContainerIsService
            )

            assert service_provider_is_service.is_service(BaseServiceContainer)
            assert service_provider_is_service.is_service(ServiceScopeFactory)
            assert service_provider_is_service.is_service(ServiceContainerIsService)
            assert service_provider_is_service.is_service(
                ServiceContainerIsKeyedService
            )
