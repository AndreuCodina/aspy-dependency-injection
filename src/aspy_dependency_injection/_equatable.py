from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class Equatable[T](ABC):
    @abstractmethod
    def equals(self, other: T | None) -> bool: ...
