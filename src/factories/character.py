"""Character factory module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.factories.factory import Factory
from src.registries.character import CharacterRegistry

if TYPE_CHECKING:
    from src.base.character import Character

REGISTRIES = CharacterRegistry.load()


class CharacterFactory(Factory):
    """
    CharacterFactory class.
    """

    @staticmethod
    def create(
        global_id: str,
        **kwargs,
    ) -> Character:
        """
        Instantiates a Character from a register by its global ID.

        :param global_id: Character global identifier.
        :type global_id: str

        :return: Instantiated Character.
        :rtype: Character
        """

        character_class = REGISTRIES.get(global_id)

        if character_class is None:
            raise ValueError(f"No character registered for global ID: {global_id}")

        return character_class(**kwargs)

    @staticmethod
    def get_all_objects() -> List[Character]:
        """
        Gets all Characters instantiable by the factory.

        :return: A list of all characters.
        :rtype: List[Character]
        """
        objs = []

        for key in REGISTRIES.keys():
            obj = CharacterFactory.create(key)
            objs.append(obj)

        return objs
