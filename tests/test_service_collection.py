from aspy_dependency_injection.service_collection import ServiceCollection
from tests.utils.services import ServiceWithDependencies, ServiceWithNoDependencies


class TestServiceCollection:
    def test_resolve_trasient_service(self) -> None:
        services = ServiceCollection()
        services.add_transient(ServiceWithNoDependencies)
        service_scope = services.build_service_provider().create_scope()

        resolved_service = service_scope.service_provider.get_service(
            ServiceWithNoDependencies
        )

        assert isinstance(resolved_service, ServiceWithNoDependencies)

    def test_resolve_transient_service_with_dependencies(self) -> None:
        services = ServiceCollection()
        services.add_transient(ServiceWithNoDependencies)
        services.add_transient(ServiceWithDependencies)
        service_scope = services.build_service_provider().create_scope()

        resolved_service = service_scope.service_provider.get_service(
            ServiceWithDependencies
        )

        assert isinstance(resolved_service, ServiceWithDependencies)
        assert isinstance(
            resolved_service.service_with_no_dependencies, ServiceWithNoDependencies
        )
