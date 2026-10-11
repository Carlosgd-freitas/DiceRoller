"""Monster registry module."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import TYPE_CHECKING, Dict

from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.monster import Monster

REGISTRIES: Dict[str, type[Monster]] = {}


class MonsterRegistry(Registry):
    """
    Monster Registry class.
    """

    @staticmethod
    def register(registry: type[Monster]) -> None:
        """
        Registers a class if it defines its own identifier.

        :param registry: Monster class to be registered.
        :type registry: type[Monster]
        """
        global_id = registry.__dict__.get("global_id")

        if global_id is None:
            return
        elif global_id in REGISTRIES:
            raise ValueError(f"Duplicate monster global ID: {global_id}")

        REGISTRIES[global_id] = registry

    @staticmethod
    def load() -> Dict[str, type[Monster]]:
        """
        Import registries modules.

        :return: A dictionary where each key is a global ID and each value is a
        Monster class.
        :rtype: Dict[str, type[Monster]]
        """
        monsters_dir = Path(__file__).parents[1] / "monsters"

        for module in iter_modules([str(monsters_dir)]):
            if module.name.startswith("_"):
                continue

            import_module(f"src.monsters.{module.name}")

        return REGISTRIES
