from typing import Final, final, override

from aspy_dependency_injection.service_lookup.service_call_site import ServiceCallSite


@final
class ConstructorCallSite(ServiceCallSite):
    _service_type: Final[type]

    def __init__(self, service_type: type) -> None:
        self._service_type = service_type

    @property
    @override
    def service_type(self) -> type:
        return self._service_type
