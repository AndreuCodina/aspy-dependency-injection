from wirio.abstractions.base_service_provider import (
    BaseServiceProvider,
)
from wirio.base_service_container import BaseServiceContainer
from wirio.service_collection import ServiceCollection


class TestBaseServiceProvider:
    async def test_resolve_base_service_provider(self) -> None:
        services = ServiceCollection()

        async with services.build_service_provider() as service_provider:
            base_service_provider = await service_provider.get(BaseServiceContainer)

            assert isinstance(base_service_provider, BaseServiceProvider)
