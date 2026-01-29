from tests.utils.services import (
    ServiceWithAsyncContextManagerAndNoDependencies,
    ServiceWithSyncContextManagerAndNoDependencies,
)
from wirio.service_collection import ServiceCollection
from wirio.service_container_engine_scope import (
    ServiceContainerEngineScope,
)


class TestServiceProviderEngineScope:
    async def test_resolve_scoped_sync_context_manager_service(
        self,
    ) -> None:
        services = ServiceCollection()
        services.add_scoped(ServiceWithSyncContextManagerAndNoDependencies)

        async with (
            services.build_service_provider() as service_provider,
            service_provider.create_scope() as service_scope,
        ):
            assert isinstance(service_scope, ServiceContainerEngineScope)

            resolved_service = await service_scope.get(
                ServiceWithSyncContextManagerAndNoDependencies
            )

            assert isinstance(
                resolved_service, ServiceWithSyncContextManagerAndNoDependencies
            )

    async def test_resolve_scoped_async_context_manager_service(
        self,
    ) -> None:
        services = ServiceCollection()
        services.add_scoped(ServiceWithAsyncContextManagerAndNoDependencies)

        async with (
            services.build_service_provider() as service_provider,
            service_provider.create_scope() as service_scope,
        ):
            assert isinstance(service_scope, ServiceContainerEngineScope)

            resolved_service = await service_scope.get(
                ServiceWithAsyncContextManagerAndNoDependencies
            )

            assert isinstance(
                resolved_service, ServiceWithAsyncContextManagerAndNoDependencies
            )
