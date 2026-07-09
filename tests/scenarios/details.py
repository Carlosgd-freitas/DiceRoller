"""Scenario for testing details logging."""

import math
from copy import deepcopy
from random import choice

from colorama import init

from src.base.dice import Dice
from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.base.side import Side
from src.compendium.effects import get_all_effects
from src.logger.combat import CombatLogger
from src.monsters.weeke import Weeke

init()

# ----------------------------

monster = Weeke()

logger = CombatLogger()

values = [1, 2, 5, 10, math.inf]
value_percents = [0.01, 0.05, 0.25, 1, math.inf]
durations = [1, 2, 5, math.inf]

all_effects = get_all_effects()

for effect in all_effects:
    effect.duration = choice(durations)

    if effect.keyword in [Keyword.BLIND, Keyword.EXECUTE, Keyword.FOCUS]:
        effect.value = 0
        effect.value_percent = choice(value_percents)

    elif effect.keyword in [Keyword.HEAL, Keyword.REGEN, Keyword.REVIVE]:
        effect.value = choice(values)
        effect.value_percent = choice(value_percents)

    elif effect.keyword not in [Keyword.NOTHING]:
        effect.value = choice(values)

    if effect.keyword in [Keyword.IMMUNITY]:
        effect.target_keywords = [deepcopy(choice(all_effects).keyword)]

buffs = [effect for effect in all_effects if effect.type == EffectType.BUFF]
debuffs = [effect for effect in all_effects if effect.type == EffectType.DEBUFF]

# ----------------------------

print("===== Dice =====")

k = 3
sides = []

for idx in range(0, len(all_effects), k):
    side = Side(all_effects[idx : idx + k])
    sides.append(side)

dice = Dice(sides)

logger.log_dice_details(dice)

# ----------------------------

print("\n===== Dice: Effect Limit =====")

side = Side(all_effects[:10])
dice = Dice([side])

logger.log_dice_details(dice)

# ----------------------------

print("\n===== Monster: Suffix + Description =====")

monster.suffix = "A"

logger.log_monster_details(monster, description=True)

monster.suffix = None

# ----------------------------

print("\n===== Monster: All Buffs + Current HP =====")

monster.effects = buffs

logger.log_monster_details(monster)

# ----------------------------

print("\n===== Monster: All Debuffs + Max HP =====")

monster.effects = debuffs

logger.log_monster_details(monster, current_hp=False)
