"""Grasslands module."""

from typing import List

from src.base.area import Area, EncounterData


class Grasslands(Area):
    """
    Grasslands class.
    """

    global_id = "GRASSLANDS"

    def __init__(self, **kwargs):
        super().__init__(global_id=self.global_id, **kwargs)

    def get_enemies(self) -> List[EncounterData]:
        """
        Returns a list of possible enemy encounters on the area.

        :return: Possible enemy encounters on the area.
        :rtype: List[EncounterData]
        """
        enemies = [
            {
                "monster_global_id": "SLIME",
                "weight": 1,
            },
            {
                "monster_global_id": "VENENOBRA",
                "weight": 1,
            },
            {
                "monster_global_id": "WEEKE",
                "weight": 1,
            },
            {
                "monster_global_id": "MANA_SPIRIT",
                "weight": 1,
            },
            {
                "monster_global_id": "GIANT_SLIME",
                "weight": 0.5,
            },
            {
                "monster_global_id": "TORTUGA",
                "weight": 0.5,
            },
        ]

        return enemies

    def get_bosses(self) -> List[EncounterData]:
        """
        Returns a list of possible boss encounters on the area.

        :return: Possible boss encounters on the area.
        :rtype: List[EncounterData]
        """
        bosses = [
            {
                "monster_global_id": "TROLL",
                "weight": 1,
            }
        ]

        return bosses
