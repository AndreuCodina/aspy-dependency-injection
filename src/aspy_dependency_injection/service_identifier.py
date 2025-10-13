from aspy_dependency_injection._equatable import Equatable


class ServiceIdentifier(Equatable["ServiceIdentifier"]):
    """Internal registered service during resolution."""

    service_type: type

    def __init__(self, service_type: type) -> None:
        self.service_type = service_type

    @staticmethod
    def from_service_type(service_type: type) -> ServiceIdentifier:
        return ServiceIdentifier(service_type)

    def equals(self, other: ServiceIdentifier | None) -> bool:
        if other is None:
            return False

        return self.service_type == other.service_type
