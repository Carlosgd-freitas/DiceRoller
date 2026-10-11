"""Factory module."""

from abc import abstractmethod
from typing import List, TypeVar

T = TypeVar("T")


class Factory:
    """
    Factory class.
    """

    @staticmethod
    @abstractmethod
    def create(id: str) -> T:
        """
        Instantiates a class from a register by its identifier.

        :param id: Class identifier.
        :type id: str

        :return: Instantiated object.
        :rtype: T
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_all_objects() -> List[T]:
        """
        Gets all objects instantiable by the factory.

        :return: A list of all objects.
        :rtype: List[T]
        """
        raise NotImplementedError
