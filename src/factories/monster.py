"""Monster factory module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.monster_registry import MONSTER_CLASSES, load_monsters

if TYPE_CHECKING:
    from src.base.monster import Monster

load_monsters()


class MonsterFactory:
    @staticmethod
    def create_monster(
        global_id: str,
        **kwargs,
    ) -> Monster:
        monster_class = MONSTER_CLASSES.get(global_id)

        if monster_class is None:
            raise ValueError(f"No monster registered for global ID: {global_id}")

        return monster_class(**kwargs)
