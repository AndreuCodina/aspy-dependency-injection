from dataclasses import dataclass


@dataclass(frozen=True)
class KeyedServiceOverride:
    service_key: object | None
    service_type: type
    implementation_instance: object | None
