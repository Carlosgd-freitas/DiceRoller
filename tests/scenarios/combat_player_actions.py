"""Scenario for testing combat player actions logging."""

from copy import deepcopy

from colorama import init

from src.base.dice import Dice
from src.base.monster import ControlType, Monster
from src.base.side import Side
from src.base.stat import Stat
from src.base.team import Team
from src.combat.manager import CombatManager
from src.combat.order_strategy import OrderStrategy
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.confuse import ConfuseEffect
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
        Side(effects=[AttackEffect(Stat(flat=1))]),
        Side(effects=[AttackEffect(Stat(flat=100))]),
    ]
)

defensive_dice = Dice(
    sides=[
        Side(effects=[BlockEffect(Stat(flat=1))]),
        Side(effects=[BlockEffect(Stat(flat=100))]),
    ]
)

restoration_dice = Dice(
    sides=[
        Side(effects=[HealEffect(Stat(flat=1))]),
        Side(effects=[HealEffect(Stat(flat=100))]),
    ]
)

deterioration_dice = Dice(
    sides=[
        Side(effects=[ExecuteEffect(Stat(percent=0.01))]),
        Side(effects=[ExecuteEffect(Stat(percent=1))]),
    ]
)

buff_dice = Dice(
    sides=[
        Side(effects=[StrengthEffect(Stat(flat=1))]),
        Side(effects=[StrengthEffect(Stat(flat=100))]),
    ]
)

debuff_dice = Dice(
    sides=[
        Side(effects=[WeakEffect(Stat(flat=1))]),
        Side(effects=[WeakEffect(Stat(flat=100))]),
    ]
)

nothing_dice = Dice(
    sides=[
        Side(effects=[NothingEffect()]),
    ]
)

curse_dice = Dice(
    sides=[
        Side(effects=[PainEffect(Stat(flat=1))]),
        Side(effects=[PainEffect(Stat(flat=100))]),
    ]
)

revive_dice = Dice(
    sides=[
        Side(effects=[ReviveEffect(Stat(percent=0.01))]),
        Side(effects=[ReviveEffect(Stat(percent=1))]),
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
    effects=[],
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

taunting_monster = deepcopy(alive_monster)
taunting_monster.effects = [ConfuseEffect(Stat(percent=1), duration=99)]

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
    name="A",
    members=[
        player_monster,
        deepcopy(dead_monster),
        deepcopy(alive_monster),
    ],
)

team_b = Team(
    name="B",
    members=[
        deepcopy(dead_monster),
        deepcopy(alive_monster),
        deepcopy(invisible_monster),
        deepcopy(repelling_monster),
        deepcopy(taunting_monster),
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
    order_strategy=OrderStrategy.SEQUENTIAL,
)

# ----------------------------

combat_manager.run()
