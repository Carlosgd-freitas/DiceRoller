"""Registry module."""

from abc import abstractmethod
from typing import TypeVar

T = TypeVar("T")


class Registry:
    """
    Registry class.
    """

    @staticmethod
    @abstractmethod
    def register(registry: type[T]) -> None:
        """
        Registers a class if it defines its own identifier.

        :param registry: Class to be registered.
        :type registry: type[T]
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def load() -> None:
        """
        Import registries modules.
        """
        raise NotImplementedError
