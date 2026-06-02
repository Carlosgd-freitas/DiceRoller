from colorama import init

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.combat.manager import CombatManager
from src.combat.team import Team
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.drain import DrainEffect
from src.effects.pierce import PierceEffect

init()

# ----------------------------

attack_sides = []
drain_sides = []
pierce_sides = []

absorb_sides = []
block_sides = []

for i in range(1, 7):
    attack_sides.append(Side(effects=[AttackEffect(i)]))
    drain_sides.append(Side(effects=[DrainEffect(i)]))
    pierce_sides.append(Side(effects=[PierceEffect(i)]))

    absorb_sides.append(Side(effects=[AbsorbEffect(i)]))
    block_sides.append(Side(effects=[BlockEffect(i)]))

# ----------------------------

monster_a = Monster(
    name="Monster",
    hp=15,
    max_hp=15,
    dice=[
        Dice(sides=attack_sides),
        Dice(sides=drain_sides),
        Dice(sides=pierce_sides),
    ],
)

team_a = Team(
    name="Red Team",
    members=[monster_a],
)

monster_b = Monster(
    name="Monster",
    hp=15,
    max_hp=15,
    dice=[
        Dice(sides=absorb_sides),
        Dice(sides=block_sides),
    ],
)

team_b = Team(
    name="Blue Team",
    members=[monster_b],
)

# ----------------------------

combat_manager = CombatManager(
    teams=[
        team_a,
        team_b,
    ],
    order_strategy="SET",
    language="EN-US",
)

# ----------------------------

combat_manager.run()
