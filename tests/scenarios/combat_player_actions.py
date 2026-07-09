"""Scenario for testing combat player actions logging."""

from copy import deepcopy

from colorama import init

from src.base.dice import Dice
from src.base.monster import ControlType, Monster
from src.base.side import Side
from src.base.team import Team
from src.combat.manager import CombatManager
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.execute import ExecuteEffect
from src.effects.heal import HealEffect
from src.effects.invisible import InvisibleEffect
from src.effects.invulnerable import InvulnerableEffect
from src.effects.nothing import NothingEffect
from src.effects.pain import PainEffect
from src.effects.repel import RepelEffect
from src.effects.revive import ReviveEffect
from src.effects.strength import StrengthEffect
from src.effects.taunt import TauntEffect
from src.effects.weak import WeakEffect
from src.systems.settings import Settings

init()

# ----------------------------

offensive_dice = Dice(
    sides=[
        Side(effects=[AttackEffect(1)]),
        Side(effects=[AttackEffect(100)]),
    ]
)

defensive_dice = Dice(
    sides=[
        Side(effects=[BlockEffect(1)]),
        Side(effects=[BlockEffect(100)]),
    ]
)

restoration_dice = Dice(
    sides=[
        Side(effects=[HealEffect(1)]),
        Side(effects=[HealEffect(100)]),
    ]
)

deterioration_dice = Dice(
    sides=[
        Side(effects=[ExecuteEffect(value_percent=0.01)]),
        Side(effects=[ExecuteEffect(value_percent=1)]),
    ]
)

buff_dice = Dice(
    sides=[
        Side(effects=[StrengthEffect(1)]),
        Side(effects=[StrengthEffect(100)]),
    ]
)

debuff_dice = Dice(
    sides=[
        Side(effects=[WeakEffect(1)]),
        Side(effects=[WeakEffect(100)]),
    ]
)

nothing_dice = Dice(
    sides=[
        Side(effects=[NothingEffect()]),
    ]
)

curse_dice = Dice(
    sides=[
        Side(effects=[PainEffect(1)]),
        Side(effects=[PainEffect(100)]),
    ]
)

revive_dice = Dice(
    sides=[
        Side(effects=[ReviveEffect(value_percent=0.01)]),
        Side(effects=[ReviveEffect(value_percent=1)]),
    ]
)

player_monster = Monster(
    name="Player",
    hp=50,
    max_hp=100,
    dice=[
        offensive_dice,
        defensive_dice,
        restoration_dice,
        deterioration_dice,
        buff_dice,
        debuff_dice,
        nothing_dice,
        curse_dice,
        revive_dice,
    ],
    control_type=ControlType.PLAYER,
)

# ----------------------------

dead_monster = Monster(
    name="Monster",
    hp=0,
    max_hp=100,
    dice=[
        nothing_dice,
    ],
)

alive_monster = Monster(
    name="Monster",
    hp=50,
    max_hp=100,
    dice=[
        nothing_dice,
    ],
)

invisible_monster = deepcopy(alive_monster)
invisible_monster.effects = [InvisibleEffect(duration=99)]

invulnerable_monster = deepcopy(alive_monster)
invulnerable_monster.effects = [InvulnerableEffect(duration=99)]

repelling_monster = deepcopy(alive_monster)
repelling_monster.effects = [RepelEffect(duration=99)]

taunting_monster = deepcopy(alive_monster)
taunting_monster.effects = [TauntEffect(duration=99)]

# ----------------------------

team_a = Team(
    name="Team A",
    members=[
        player_monster,
        deepcopy(dead_monster),
        deepcopy(alive_monster),
    ],
)

team_b = Team(
    name="Team B",
    members=[
        deepcopy(dead_monster),
        deepcopy(alive_monster),
    ],
)

# ----------------------------

combat_manager = CombatManager(
    settings=Settings(
        monster_end_turn="MANUAL",
    ),
    teams=[
        team_a,
        team_b,
    ],
    order_strategy="SET",
)

# ----------------------------

combat_manager.run()
