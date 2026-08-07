"""Pytest configuration file for tests."""

from copy import deepcopy
from typing import Dict

from pytest import fixture

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.team import Team
from src.combat.effects import EffectManager
from src.combat.manager import CombatManager
from src.combat.order_strategy import OrderStrategy
from src.combat.suffixes import SuffixManager
from src.combat.team_manager import TeamManager
from src.compendium.effects import EffectCompendium
from src.effects.nothing import NothingEffect
from src.gamemodes.sandbox.sandbox_menu import SandboxMenu
from src.locales.languages import Language
from src.logger.attributes import AttributeLogger
from src.logger.combat import CombatLogger
from src.logger.dice import DiceLogger
from src.logger.effects import EffectLogger
from src.logger.logger import Logger
from src.logger.monster import MonsterLogger
from src.menus.compendium_menu import CompendiumMenu
from src.menus.main_menu import MainMenu
from src.menus.settings_menu import SettingsMenu
from src.systems.file import FileManager
from src.systems.manager import Manager
from src.systems.randomizer import Randomizer
from src.systems.settings import Settings
from src.systems.targeting.selectors.manager import SelectorManager


@fixture()
def settings() -> Settings:
    settings = Settings()

    return settings


@fixture()
def loggers() -> Dict:
    logger = Logger(enabled=False, language=Language.EN_US)
    attribute_logger = AttributeLogger(enabled=False, language=Language.EN_US)
    combat_logger = CombatLogger(enabled=False, language=Language.EN_US)
    dice_logger = DiceLogger(enabled=False, language=Language.EN_US)
    effect_logger = EffectLogger(enabled=False, language=Language.EN_US)
    monster_logger = MonsterLogger(enabled=False, language=Language.EN_US)

    return {
        "logger": logger,
        "attribute_logger": attribute_logger,
        "combat_logger": combat_logger,
        "dice_logger": dice_logger,
        "effect_logger": effect_logger,
        "monster_logger": monster_logger,
    }


@fixture()
def compendiums(settings: Settings) -> Dict:
    effect_compendium = EffectCompendium(
        settings=settings,
        logging=False,
    )

    return {
        "effect_compendium": effect_compendium,
    }


@fixture()
def managers(settings: Settings) -> Dict:
    logger = Logger(enabled=False, language=Language.EN_US)

    manager = Manager(logger=logger, settings=settings)

    combat_manager = CombatManager(
        settings=settings,
        logging=False,
    )

    effect_manager = EffectManager(
        settings=settings,
        logging=False,
    )

    file_manager = FileManager()

    selector_manager = SelectorManager()

    suffix_manager = SuffixManager()

    team_manager = TeamManager()

    return {
        "manager": manager,
        "combat_manager": combat_manager,
        "effect_manager": effect_manager,
        "file_manager": file_manager,
        "selector_manager": selector_manager,
        "suffix_manager": suffix_manager,
        "team_manager": team_manager,
    }


@fixture()
def menus(settings: Settings) -> Dict:
    compendium_menu = CompendiumMenu(
        settings=settings,
        logging=False,
    )

    main_menu = MainMenu(
        settings=settings,
        logging=False,
    )

    sandbox_menu = SandboxMenu(
        settings=settings,
        logging=False,
    )

    settings_menu = SettingsMenu(
        settings=settings,
        logging=False,
    )

    return {
        "compendium_menu": compendium_menu,
        "main_menu": main_menu,
        "sandbox_menu": sandbox_menu,
        "settings_menu": settings_menu,
    }


@fixture()
def combat(settings: Settings) -> Dict:
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
        settings=settings,
        teams=teams,
        order_strategy=OrderStrategy.SEQUENTIAL,
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
        "team_manager": combat_manager.team_manager,
    }


@fixture()
def combat_softlock(settings: Settings) -> Dict:
    nothing_dice = Dice(
        sides=[
            Side(effects=[NothingEffect()]),
        ]
    )

    monster_0 = Monster(
        local_id="MONSTER_0",
        name="Blue",
        hp=1,
        max_hp=1,
        speed=1,
        dice=[deepcopy(nothing_dice)],
    )

    monster_1 = Monster(
        local_id="MONSTER_1",
        name="Red",
        hp=1,
        max_hp=1,
        speed=1,
        dice=[deepcopy(nothing_dice)],
    )

    team_0 = Team(
        name="Team Blue",
        members=[monster_0],
    )

    team_1 = Team(
        name="Team Red",
        members=[monster_1],
    )

    teams = [team_0, team_1]
    monsters = [monster for team in teams for monster in team.members]

    combat_manager = CombatManager(
        settings=settings,
        teams=teams,
        order_strategy=OrderStrategy.SEQUENTIAL,
        logging=False,
        softlock_limit=3,
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
        "team_manager": combat_manager.team_manager,
    }


@fixture()
def randomizer() -> Randomizer:
    randomizer = Randomizer()

    return randomizer
