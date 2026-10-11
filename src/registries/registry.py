"""Registry module."""

from abc import abstractmethod
from typing import Dict, TypeVar

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
    def load() -> Dict[str, type[T]]:
        """
        Import registries modules.

        :return: A dictionary where each key is an identifier and each value is a
        class.
        :rtype: Dict[str, type[T]]
        """
        raise NotImplementedError
