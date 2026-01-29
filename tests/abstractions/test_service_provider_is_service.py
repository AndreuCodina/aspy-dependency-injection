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
from wirio.service_container import ServiceContainer


class TestServiceProviderIsService:
    async def test_resolve_service_provider_is_service(self) -> None:
        service_container = ServiceContainer()

        async with service_container:
            service_provider_is_service = await service_container.get(
                ServiceContainerIsService
            )

            assert isinstance(service_provider_is_service, ServiceContainerIsService)

    async def test_built_in_services_with_is_service_returns_true(
        self,
    ) -> None:
        service_container = ServiceContainer()
        service_container.add_transient(ServiceWithNoDependencies)

        async with service_container:
            service_provider_is_service = await service_container.get(
                ServiceContainerIsService
            )

            assert service_provider_is_service.is_service(BaseServiceContainer)
            assert service_provider_is_service.is_service(ServiceScopeFactory)
            assert service_provider_is_service.is_service(ServiceContainerIsService)
            assert service_provider_is_service.is_service(
                ServiceContainerIsKeyedService
            )
