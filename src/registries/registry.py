"""Registry module."""

from abc import ABC
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Any, ClassVar, Dict, Generic, TypeVar

T = TypeVar("T")


class Registry(ABC, Generic[T]):
    """
    Base class for registries.
    """

    id_name: ClassVar[str]
    dir_name: ClassVar[str]
    registries: ClassVar[dict[str, type]]

    @classmethod
    def get_id(cls, registry: type[T]) -> Any:
        """
        Return the identifier defined by a class.

        :param registry: Class to be registered.
        :type registry: type[T]

        :return: Class identifier.
        :rtype: Any
        """
        return registry.__dict__.get(cls.id_name)

    @classmethod
    def register(cls, registry: type[T]) -> None:
        """
        Register a class if it defines an identifier.

        :param registry: Class to be registered.
        :type registry: type[T]
        """
        id = cls.get_id(registry)

        if id is None:
            return

        elif id in cls.registries:
            raise ValueError(f"Duplicate identifier for registry: {id}")

        cls.registries[id] = registry

    @classmethod
    def load(cls) -> Dict[str, type[T]]:
        """
        Import registries modules.

        :return: A dictionary where each key is an identifier and each value is a class.
        :rtype: Dict[str, type[T]]
        """
        dirname = cls.dir_name
        monsters_dir = Path(__file__).parents[1] / dirname

        for module in iter_modules([str(monsters_dir)]):
            if not module.name.startswith("_"):
                import_module(f"src.{dirname}.{module.name}")

        return cls.registries
