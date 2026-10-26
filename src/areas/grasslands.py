"""Grasslands module."""

from typing import List

from src.base.area import Area, EncounterEntryData


class Grasslands(Area):
    """
    Grasslands class.
    """

    id = "GRASSLANDS"

    def __init__(self, **kwargs):
        super().__init__(id=self.id, **kwargs)

    def get_enemies(self) -> List[EncounterEntryData]:
        """
        Returns a list of possible enemies on the area.

        :return: Possible enemies on the area.
        :rtype: List[EncounterEntryData]
        """
        enemies = [
            {
                "monster_global_id": "SLIME",
                "weight": 1,
                "role": "DAMAGE",
            },
            {
                "monster_global_id": "VENENOBRA",
                "weight": 1,
                "role": "DAMAGE",
            },
            {
                "monster_global_id": "WEEKE",
                "weight": 1,
                "role": "SUPPORT",
            },
            {
                "monster_global_id": "MANA_SPIRIT",
                "weight": 1,
                "role": "SUPPORT",
            },
            {
                "monster_global_id": "GIANT_SLIME",
                "weight": 0.5,
                "role": "DAMAGE",
            },
            {
                "monster_global_id": "TORTUGA",
                "weight": 0.5,
                "role": "DAMAGE",
            },
        ]

        return enemies

    def get_bosses(self) -> List[EncounterEntryData]:
        """
        Returns a list of possible bosses on the area.

        :return: Possible bosses on the area.
        :rtype: List[EncounterEntryData]
        """
        bosses = [
            {
                "monster_global_id": "TROLL",
                "weight": 1,
                "role": "DAMAGE",
            }
        ]

        return bosses
