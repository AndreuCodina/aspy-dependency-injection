import inspect
from typing import TYPE_CHECKING, final, get_type_hints

from aspy_dependency_injection._concurrent_dictionary import ConcurrentDictionary
from aspy_dependency_injection.service_identifier import ServiceIdentifier

if TYPE_CHECKING:
    from aspy_dependency_injection.service_collection import ServiceCollection


@final
class ServiceProvider:
    """Provider that resolves services."""

    services: ServiceCollection
    _service_accessors: ConcurrentDictionary[ServiceIdentifier, object | None]

    def __init__(self, services: ServiceCollection) -> None:
        self.services = services
        self._service_accessors = ConcurrentDictionary()
        # Root = new ServiceProviderEngineScope(this, isRootScope: true);

    def get_service(self, service_type: type) -> object | None:
        return self._get_service_from_service_identifier(
            ServiceIdentifier.from_service_type(service_type)
        )

    def _get_service_from_service_identifier(
        self, service_identifier: ServiceIdentifier
    ) -> object | None:
        for descriptor in self.services.descriptors:
            if descriptor.service_type == service_identifier.service_type:
                return self.create_instance(descriptor.service_type)

        return None

    # def _create_service_accessor(
    #     self, service_identifier: ServiceIdentifier
    # ) -> object | None:
    #     pass

    def create_instance(self, service_type: type) -> object:
        """Recursively create an instance of the service type."""
        is_service_registered = any(
            descriptor.service_type == service_type
            for descriptor in self.services.descriptors
        )
        if not is_service_registered:
            error_message = f"Service {service_type} not registered."
            raise ValueError(error_message)

        init_method = service_type.__init__
        init_signature = inspect.signature(init_method)
        init_type_hints = get_type_hints(init_method)
        parameter_names = init_signature.parameters.keys()
        arguments: dict[str, object] = {}

        for parameter_name in parameter_names:  # init_signature.parameters.items()
            if parameter_name in ["self", "args", "kwargs"]:
                continue

            parameter_type = init_type_hints[parameter_name]
            arguments[parameter_name] = self.create_instance(parameter_type)

        if len(arguments) == 0:
            return service_type()

        return service_type(**arguments)
