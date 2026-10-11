"""Character registry module."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import TYPE_CHECKING, Dict

from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.character import Character

REGISTRIES: Dict[str, type[Character]] = {}


class CharacterRegistry(Registry):
    """
    Character Registry class.
    """

    @staticmethod
    def register(registry: type[Character]) -> None:
        """
        Registers a class if it defines its own identifier.

        :param registry: Character class to be registered.
        :type registry: type[Character]
        """
        global_id = registry.__dict__.get("global_id")

        if global_id is None:
            return
        elif global_id in REGISTRIES:
            raise ValueError(f"Duplicate character global ID: {global_id}")

        REGISTRIES[global_id] = registry

    @staticmethod
    def load() -> Dict[str, type[Character]]:
        """
        Import registries modules.

        :return: A dictionary where each key is a global ID and each value is a
        Character class.
        :rtype: Dict[str, type[Character]]
        """
        characters_dir = Path(__file__).parents[1] / "characters"

        for module in iter_modules([str(characters_dir)]):
            if module.name.startswith("_"):
                continue

            import_module(f"src.characters.{module.name}")

        return REGISTRIES
