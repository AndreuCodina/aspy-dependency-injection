from collections.abc import Generator
from contextlib import AbstractAsyncContextManager, contextmanager
from types import TracebackType
from typing import Self, final, override

from wirio.abstractions.service_scope import ServiceScope
from wirio.exceptions import ServiceContainerNotBuiltError
from wirio.service_collection import ServiceCollection
from wirio.service_provider import ServiceProvider


@final
class ServiceContainer(
    ServiceCollection, AbstractAsyncContextManager["ServiceContainer"]
):
    """Collection of resolvable services."""

    _service_provider: ServiceProvider | None

    def __init__(self) -> None:
        super().__init__()
        self._service_provider = None

    @property
    def service_provider(self) -> ServiceProvider | None:
        return self._service_provider

    async def get_required_service[TService](
        self, service_type: type[TService]
    ) -> TService:
        service_provider = await self._get_service_provider()
        return await service_provider.get_required_service(service_type)

    async def get_service[TService](
        self, service_type: type[TService]
    ) -> TService | None:
        service_provider = await self._get_service_provider()
        return await service_provider.get_service(service_type)

    async def get_required_keyed_service[TService](
        self, service_key: object | None, service_type: type[TService]
    ) -> TService:
        service_provider = await self._get_service_provider()
        return await service_provider.get_required_keyed_service(
            service_key=service_key, service_type=service_type
        )

    async def get_keyed_service[TService](
        self, service_key: object | None, service_type: type[TService]
    ) -> TService | None:
        service_provider = await self._get_service_provider()
        return await service_provider.get_keyed_service(
            service_key=service_key, service_type=service_type
        )

    def create_scope(self) -> ServiceScope:
        """Create a new :class:`ServiceScope` that can be used to resolve scoped services."""
        if self._service_provider is None:
            self._service_provider = self.build_service_provider()

        return self._service_provider.create_scope()

    async def aclose(self) -> None:
        if self._service_provider is not None:
            await self._service_provider.__aexit__(None, None, None)

        self._service_provider = None

    @contextmanager
    def override_service(
        self, service_type: type, implementation_instance: object | None
    ) -> Generator[None]:
        """Override a service registration within the context manager scope.

        It can be used to temporarily replace a service for testing specific scenarios. Don't use it in production.
        """
        self._ensure_service_container_is_built()
        assert self._service_provider is not None

        with self._service_provider.override_service(
            service_type=service_type,
            implementation_instance=implementation_instance,
        ):
            yield

    @contextmanager
    def override_keyed_service(
        self,
        service_key: object | None,
        service_type: type,
        implementation_instance: object | None,
    ) -> Generator[None]:
        """Override a keyed service registration within the context manager scope.

        It can be used to temporarily replace a service for testing specific scenarios. Don't use it in production.
        """
        self._ensure_service_container_is_built()
        assert self._service_provider is not None

        with self._service_provider.override_keyed_service(
            service_key=service_key,
            service_type=service_type,
            implementation_instance=implementation_instance,
        ):
            yield

    async def _get_service_provider(self) -> ServiceProvider:
        if self._service_provider is None:
            self._service_provider = self.build_service_provider()
            await self._service_provider.__aenter__()

        return self._service_provider

    def _ensure_service_container_is_built(self) -> None:
        if self._service_provider is None:
            raise ServiceContainerNotBuiltError

    @override
    async def __aenter__(self) -> Self:
        await self._get_service_provider()
        return self

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        assert self._service_provider is not None
        await self._service_provider.__aexit__(exc_type, exc_val, exc_tb)
        self._service_provider = None
