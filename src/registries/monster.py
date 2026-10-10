"""Monster registry module."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import TYPE_CHECKING

from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.monster import Monster

REGISTRIES: dict[str, type[Monster]] = {}


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
    def load() -> None:
        """
        Import registries modules.
        """
        monsters_dir = Path(__file__).parents[1] / "monsters"

        for module in iter_modules([str(monsters_dir)]):
            if module.name.startswith("_"):
                continue

            import_module(f"src.monsters.{module.name}")
