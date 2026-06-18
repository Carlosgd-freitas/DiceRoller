"""Monsters Compendium module."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, List

from src.compendium.compendium import Compendium
from src.monsters.giant_slime import GiantSlime
from src.monsters.mana_spirit import ManaSpirit
from src.monsters.slime import Slime
from src.monsters.tortuga import Tortuga
from src.monsters.training_dummy import TrainingDummy
from src.monsters.venenobra import Venenobra
from src.monsters.weeke import Weeke

if TYPE_CHECKING:
    from src.base.monster import Monster

ALL_MONSTERS = [
    GiantSlime(),
    Slime(),
    Tortuga(),
    TrainingDummy(),
    ManaSpirit(),
    Venenobra(),
    Weeke(),
]


def get_all_monsters() -> List[Monster]:
    return deepcopy(ALL_MONSTERS)


class MonsterCompendium(Compendium):
    pass
