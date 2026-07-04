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

values = [1, 2, 5, 10]
durations = [1, 2, 5, math.inf]

all_effects = get_all_effects()

for effect in all_effects:
    effect.value = choice(values)
    effect.duration = choice(durations)

    if effect.keyword in [Keyword.IMMUNITY]:
        effect.effects = [deepcopy(choice(all_effects).keyword)]

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
