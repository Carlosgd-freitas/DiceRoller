import math
from random import choice

from colorama import init

from src.base.effect import EffectType
from src.compendium.effects import get_all_effects
from src.logger.combat import CombatLogger
from src.monsters.slime import Slime

init()

# ----------------------------

all_effects = get_all_effects()

# ----------------------------

monster = Slime()

logger = CombatLogger()

values = [1, 2, 5, 10]
durations = [1, 2, 5, math.inf]

buffs = [effect for effect in all_effects if effect.type == EffectType.BUFF]
for buff in buffs:
    buff.value = choice(values)
    buff.duration = choice(durations)

debuffs = [effect for effect in all_effects if effect.type == EffectType.DEBUFF]
for debuff in debuffs:
    debuff.value = choice(values)
    debuff.duration = choice(durations)

# ----------------------------

print("===== Suffix + Description =====")

monster.suffix = "A"

logger.log_monster_details(monster, description=True)

monster.suffix = None

# ----------------------------

print("\n===== All Buffs + Current HP =====")

monster.effects = buffs

logger.log_monster_details(monster)

# ----------------------------

print("\n===== All Debuffs + Max HP =====")

monster.effects = debuffs

logger.log_monster_details(monster, current_hp=False)
