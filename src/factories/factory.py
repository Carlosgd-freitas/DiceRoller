"""Factory module."""

from typing import Any, ClassVar, Generic, TypeVar

T = TypeVar("T")


class Factory(Generic[T]):
    """Base factory for registered objects."""

    registries: ClassVar[dict[str, type[T]]]

    @classmethod
    def create(cls, id: str, **kwargs: Any) -> T:
        """
        Instantiates a class from a register by its identifier.

        :param id: Class identifier.
        :type id: str

        :return: Instantiated object.
        :rtype: T
        """
        registry_class = cls.registries.get(id)

        if registry_class is None:
            raise ValueError(f"No object registered for identifier: {id}")

        return registry_class(**kwargs)

    @classmethod
    def get_all_objects(cls) -> list[T]:
        """
        Gets all objects instantiable by the factory.

        :return: A list of all objects.
        :rtype: List[T]
        """
        return [cls.create(id) for id in cls.registries]
