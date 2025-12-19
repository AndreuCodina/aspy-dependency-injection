from abc import ABC, abstractmethod


class ServiceProvider(ABC):
    @abstractmethod
    async def get_service(self, service_type: type) -> object | None: ...
