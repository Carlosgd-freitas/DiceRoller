"""Scenario for testing effect description logigng."""

from colorama import init

from src.base.keywords import Keyword
from src.base.stat import Stat
from src.compendium.effects import get_all_effects
from src.logger.effects import EffectLogger
from src.systems.randomizer import Randomizer
from src.systems.settings import Settings

init()

# ----------------------------

settings = Settings()
randomizer = Randomizer()

logger = EffectLogger()

all_effects = get_all_effects()

# ----------------------------

for effect in all_effects:
    message = logger.get_effect_message(effect=effect, associated=False)
    logger.log(message=message)

    effect.value = Stat(flat=1, percent=0.1)
    effect.duration = 2

    message_group = logger.get_message_group(
        namespace="effects", message_group=effect.keyword.name
    )

    for key, _value in message_group.items():
        if key.startswith("description"):
            if key == "description_all":
                effect.target_keywords = [Keyword.ALL]

            elif key == "description_specific":
                effect.target_keywords = [
                    randomizer.get_random_keyword(),
                    randomizer.get_random_keyword(),
                ]

            logger.log_effect_description(effect=effect, key=key)

    logger.log(message="")
