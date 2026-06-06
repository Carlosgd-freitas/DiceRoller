"""Effect Compendium module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.color import color_string
from src.base.keywords import get_keyword_color
from src.compendium.compendium import Compenidum, CompenidumOptionsMessages
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.bleed import BleedEffect
from src.effects.blind import BlindEffect
from src.effects.block import BlockEffect
from src.effects.burn import BurnEffect
from src.effects.confuse import ConfuseEffect
from src.effects.curse import CurseEffect
from src.effects.doom import DoomEffect
from src.effects.drain import DrainEffect
from src.effects.execute import ExecuteEffect
from src.effects.freeze import FreezeEffect
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.nothing import NothingEffect
from src.effects.pierce import PierceEffect
from src.effects.poison import PoisonEffect
from src.effects.regen import RegenEffect
from src.effects.revive import ReviveEffect
from src.effects.sleep import SleepEffect
from src.effects.stun import StunEffect
from src.effects.thorns import ThornsEffect
from src.locales.languages import Language
from src.logger.effects import EffectLogger

if TYPE_CHECKING:
    from src.base.effect import Effect


class EffectCompenidum(Compenidum):
    """
    Effect Compendium class.
    """

    def __init__(
        self,
        language: Language = Language.EN_US,
    ):
        items = [
            AbsorbEffect(1),
            AttackEffect(1),
            BleedEffect(1),
            BlindEffect(1),
            BlockEffect(1),
            BurnEffect(1),
            ConfuseEffect(1),
            CurseEffect(1),
            DoomEffect(1),
            DrainEffect(1),
            ExecuteEffect(1),
            FreezeEffect(1),
            HealEffect(1),
            ManaEffect(1),
            ManaRegenEffect(1),
            NothingEffect(1),
            PierceEffect(1),
            PoisonEffect(1),
            RegenEffect(1),
            ReviveEffect(1),
            SleepEffect(1),
            StunEffect(1),
            ThornsEffect(1),
        ]

        super().__init__(
            items=items,
            page_headers=["#", "Name", "Type"],
            page_colalign=("right", "left", "left"),
            logger=EffectLogger(language=language),
        )

    def get_page_data(self, page_items: List[Effect]) -> List[List[Effect]]:
        """."""
        page_data = []

        for idx, item in enumerate(page_items):
            keyword_color = get_keyword_color(item.keyword)
            keyword = color_string(item.keyword.value, **keyword_color)

            page_data.append(
                [
                    f"[{idx+1}]",
                    keyword,
                    item.type.value.capitalize(),
                ]
            )

        return page_data

    def get_options_messages(self) -> CompenidumOptionsMessages:
        """."""
        return {
            "exit": "Exit",
            "next_item": "Next Effect",
            "next_page": "Next Page",
            "previous_item": "Previous Effectt",
            "previous_page": "Previous Page",
            "return_to_pages": "Return",
            "show_item_details": "See Effect Details",
        }

    def show_item(self):
        """."""
        item: Effect = self.items[self.item_number - 1]

        self.logger.log(message="\n╔══════════════════════════════════╗")
        self.logger.log(message="║ Effect Compendium:               ║")
        self.logger.log(message="║ Compêndio de Efeitos:            ║")
        self.logger.log(message="╚══════════════════════════════════╝\n")

        # Keyword
        message = self.logger.get_colored_message(
            namespace="effects",
            message_group="KEYWORDS",
            keyword=item.keyword,
        )
        self.logger.log(message=message + "\n")

        # Description
        self.logger.log(
            namespace="effects",
            message_group="DESCRIPTION",
            key=item.keyword.name.lower(),
        )
        self.logger.log(message="")
