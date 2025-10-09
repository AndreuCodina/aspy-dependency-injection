from aspy_dependency_injection.service_collection import ServiceCollection


class ServiceWithNoDependencies:
    pass


class ServiceWithDependencies:
    def __init__(self, service_with_no_dependencies: ServiceWithNoDependencies) -> None:
        self.service_with_no_dependencies = service_with_no_dependencies


class TestServiceCollection:
    def test_resolve_trasient_service(self) -> None:
        services = ServiceCollection()
        services.add_transient(ServiceWithNoDependencies)

        resolved_service = services.get(ServiceWithNoDependencies)

        assert isinstance(resolved_service, ServiceWithNoDependencies)

    def test_resolve_transient_service_with_dependencies(self) -> None:
        services = ServiceCollection()
        services.add_transient(ServiceWithNoDependencies)
        services.add_transient(ServiceWithDependencies)

        resolved_service = services.get(ServiceWithDependencies)

        assert isinstance(resolved_service, ServiceWithDependencies)
        assert isinstance(
            resolved_service.service_with_no_dependencies, ServiceWithNoDependencies
        )
