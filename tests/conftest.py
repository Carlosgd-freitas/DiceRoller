"""Pytest configuration file for tests."""

from typing import Dict

from pytest import fixture

from src.base.monster import Monster
from src.combat.manager import CombatManager, OrderStrategy
from src.combat.team import Team
from src.locales.languages import Language
from src.logger.attributes import AttributeLogger
from src.logger.combat import CombatLogger
from src.logger.dice import DiceLogger
from src.logger.effects import EffectLogger
from src.logger.file import FileLogger
from src.logger.logger import Logger
from src.logger.monster import MonsterLogger
from src.systems.settings import Settings


@fixture()
def loggers() -> Dict:
    logger = Logger(enabled=False, language=Language.EN_US)
    attribute_logger = AttributeLogger(enabled=False, language=Language.EN_US)
    combat_logger = CombatLogger(enabled=False, language=Language.EN_US)
    dice_logger = DiceLogger(enabled=False, language=Language.EN_US)
    effect_logger = EffectLogger(enabled=False, language=Language.EN_US)
    file_logger = FileLogger(enabled=False, language=Language.EN_US)
    monster_logger = MonsterLogger(enabled=False, language=Language.EN_US)

    return {
        "logger": logger,
        "attribute_logger": attribute_logger,
        "combat_logger": combat_logger,
        "dice_logger": dice_logger,
        "effect_logger": effect_logger,
        "file_logger": file_logger,
        "monster_logger": monster_logger,
    }


@fixture()
def combat() -> Dict:
    monster_0 = Monster(
        local_id="MONSTER_0",
        name="Red",
        hp=0,
        max_hp=100,
        speed=0,
    )

    monster_1 = Monster(
        local_id="MONSTER_1",
        name="Green",
        hp=1,
        max_hp=125,
        speed=5,
    )

    monster_2 = Monster(
        local_id="MONSTER_2",
        name="Yellow",
        hp=10,
        max_hp=150,
        speed=1,
    )

    monster_3 = Monster(
        local_id="MONSTER_3",
        name="Blue",
        hp=100,
        max_hp=175,
        speed=10,
    )

    monster_4 = Monster(
        local_id="MONSTER_4",
        name="Purple",
        hp=200,
        max_hp=200,
        speed=1,
    )

    team_0 = Team(
        name="Team Red",
        members=[monster_0, monster_1, monster_2],
    )

    team_1 = Team(
        name="Team Blue",
        members=[monster_3, monster_4],
    )

    teams = [team_0, team_1]
    monsters = [monster for team in teams for monster in team.members]

    combat_manager = CombatManager(
        settings=Settings(),
        teams=teams,
        order_strategy=OrderStrategy.SET,
        logging=False,
    )

    combat_manager.start_combat()

    return {
        # Variables
        "monsters": monsters,
        "teams": teams,
        # Managers
        "combat_manager": combat_manager,
        "effect_manager": combat_manager.effect_manager,
        "selector_manager": combat_manager.selector_manager,
        "suffix_manager": combat_manager.suffix_manager,
    }
