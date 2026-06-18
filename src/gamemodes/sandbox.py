"""Sandbox mode."""

from copy import deepcopy
from random import choice

from src.combat.manager import CombatManager
from src.combat.team import Team
from src.compendium.monsters import get_all_monsters
from src.systems.settings import Settings


def run(settings: Settings, teams_size: int):
    """
    Runs a combat between two teams.

    :param settings: Game settings.
    :type settings: Settings

    :param teams_size: Number of monsters in each team.
    :type teams_size: int
    """
    all_monsters = get_all_monsters()

    monsters_0 = []
    monsters_1 = []

    for _ in range(teams_size):
        monsters_0.append(deepcopy(choice(all_monsters)))
        monsters_1.append(deepcopy(choice(all_monsters)))

    team_0 = Team(name="Alpha", members=monsters_0)
    team_1 = Team(name="Beta", members=monsters_1)

    combat_manager = CombatManager(settings, teams=[team_0, team_1])

    combat_manager.run()

    return
