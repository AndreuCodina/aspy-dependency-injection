from pytest_mock import MockerFixture

from tests.utils.services import ServiceWithNoDependencies
from wirio.service_container import ServiceContainer


class TestServiceContainer:
    async def test_initialize_service_provider_automatically(self) -> None:  # noqa: PLR0915
        services = ServiceContainer()
        services.add_transient(ServiceWithNoDependencies)
        assert services.service_provider is None

        try:
            await services.get_required_service(ServiceWithNoDependencies)
            assert services.service_provider is not None
            assert services.service_provider.is_fully_initialized
        finally:
            await services.aclose()

        services = ServiceContainer()
        services.add_transient(ServiceWithNoDependencies)
        assert services.service_provider is None

        try:
            await services.get_service(ServiceWithNoDependencies)
            assert services.service_provider is not None
            assert services.service_provider.is_fully_initialized
        finally:
            await services.aclose()

        service_key = "key"
        services = ServiceContainer()
        services.add_keyed_transient(service_key, ServiceWithNoDependencies)
        assert services.service_provider is None

        try:
            await services.get_required_keyed_service(
                service_key, ServiceWithNoDependencies
            )
            assert services.service_provider is not None
            assert services.service_provider.is_fully_initialized
        finally:
            await services.aclose()

        services = ServiceContainer()
        services.add_keyed_transient(service_key, ServiceWithNoDependencies)
        assert services.service_provider is None

        try:
            await services.get_keyed_service(service_key, ServiceWithNoDependencies)
            assert services.service_provider is not None
            assert services.service_provider.is_fully_initialized
        finally:
            await services.aclose()

        services = ServiceContainer()
        services.add_transient(ServiceWithNoDependencies)
        assert services.service_provider is None

        try:
            async with services.create_scope():
                assert services.service_provider is not None
                assert services.service_provider.is_fully_initialized
        finally:
            await services.aclose()

        services = ServiceContainer()
        services.add_transient(ServiceWithNoDependencies)

        async with services:
            assert services.service_provider is not None
            assert services.service_provider.is_fully_initialized

    async def test_override_service(self, mocker: MockerFixture) -> None:
        services = ServiceContainer()
        services.add_transient(ServiceWithNoDependencies)

        async with services:
            resolved_service = await services.get_required_service(
                ServiceWithNoDependencies
            )
            assert isinstance(resolved_service, ServiceWithNoDependencies)

            service_mock = mocker.create_autospec(
                ServiceWithNoDependencies, instance=True
            )

            with services.override_service(ServiceWithNoDependencies, service_mock):
                resolved_service = await services.get_required_service(
                    ServiceWithNoDependencies
                )
                assert resolved_service is service_mock
                assert isinstance(resolved_service, ServiceWithNoDependencies)

            resolved_service = await services.get_required_service(
                ServiceWithNoDependencies
            )
            assert resolved_service is not service_mock
            assert isinstance(resolved_service, ServiceWithNoDependencies)

    async def test_override_keyed_service(self, mocker: MockerFixture) -> None:
        services = ServiceContainer()
        service_key = "key"
        services.add_keyed_transient(service_key, ServiceWithNoDependencies)

        async with services:
            resolved_service = await services.get_required_keyed_service(
                service_key, ServiceWithNoDependencies
            )
            assert isinstance(resolved_service, ServiceWithNoDependencies)

            service_mock = mocker.create_autospec(
                ServiceWithNoDependencies, instance=True
            )

            with services.override_keyed_service(
                service_key, ServiceWithNoDependencies, service_mock
            ):
                resolved_service = await services.get_required_keyed_service(
                    service_key, ServiceWithNoDependencies
                )
                assert resolved_service is service_mock
                assert isinstance(resolved_service, ServiceWithNoDependencies)

            resolved_service = await services.get_required_keyed_service(
                service_key, ServiceWithNoDependencies
            )
            assert resolved_service is not service_mock
            assert isinstance(resolved_service, ServiceWithNoDependencies)
