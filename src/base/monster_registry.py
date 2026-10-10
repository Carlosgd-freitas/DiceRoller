"""Monster registry module."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.base.monster import Monster


MONSTER_CLASSES: dict[str, type[Monster]] = {}


def register_monster(monster_class: type[Monster]) -> None:
    """Register a Monster subclass if it defines its own global ID."""
    global_id = monster_class.__dict__.get("global_id")

    if global_id is None:
        return

    MONSTER_CLASSES[global_id] = monster_class


def load_monsters() -> None:
    """Import monster modules to register their classes automatically."""
    monsters_dir = Path(__file__).parents[1] / "monsters"

    for module in iter_modules([str(monsters_dir)]):
        if module.name.startswith("_"):
            continue

        import_module(f"src.monsters.{module.name}")
