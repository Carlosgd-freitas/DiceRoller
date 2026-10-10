"""Monster factory module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.registries.monster import REGISTRIES, MonsterRegistry

if TYPE_CHECKING:
    from src.base.monster import Monster

MonsterRegistry.load()


class MonsterFactory:
    """
    MonsterFactory class.
    """

    @staticmethod
    def create(
        global_id: str,
        **kwargs,
    ) -> Monster:
        """
        Instantiates a Monster from a register by its global ID.

        :param global_id: Monster global identifier.
        :type global_id: str

        :return: Instantiated Monster.
        :rtype: Monster
        """

        monster_class = REGISTRIES.get(global_id)

        if monster_class is None:
            raise ValueError(f"No monster registered for global ID: {global_id}")

        return monster_class(**kwargs)
