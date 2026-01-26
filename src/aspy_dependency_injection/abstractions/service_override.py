from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceOverride:
    service_type: type
    implementation_instance: object | None
