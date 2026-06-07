"""Effect Compendium module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.compendium.compendium import Compendium, CompendiumOptionsMessages
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


class EffectCompendium(Compendium):
    """
    Effect Compendium class.
    """

    def __init__(
        self,
        language: Language = Language.EN_US,
    ):
        items = [
            AbsorbEffect(),
            AttackEffect(),
            BleedEffect(),
            BlindEffect(),
            BlockEffect(),
            BurnEffect(),
            ConfuseEffect(),
            CurseEffect(),
            DoomEffect(),
            DrainEffect(),
            ExecuteEffect(),
            FreezeEffect(),
            HealEffect(),
            ManaEffect(),
            ManaRegenEffect(),
            NothingEffect(),
            PierceEffect(),
            PoisonEffect(),
            RegenEffect(),
            ReviveEffect(),
            SleepEffect(),
            StunEffect(),
            ThornsEffect(),
        ]

        logger = EffectLogger(language=language)

        title = logger.get_message(
            namespace="effects", message_group="COMPENDIUM", key="title"
        )

        super().__init__(
            logger=logger,
            title=title,
            items=items,
            page_headers=["#", "Name", "Type"],
            page_colalign=("right", "left", "left"),
        )

    def sort(self):
        """."""
        self.items.sort(key=lambda x: x.keyword.name)

    def get_page_data(self, page_items: List) -> List[List]:
        """
        Returns tabulated data that will be used with `tabulate` package.

        :var page_items: A Compendium page's items.
        :vartype page_items: List

        :return: A Compendium page's items structured as tabulated data.
        :rtype: List[List]
        """
        page_data = []

        for idx, item in enumerate(page_items):
            effect_keyword = self.logger.get_colored_message(
                namespace="effects",
                message_group="KEYWORDS",
                keyword=item.keyword,
            )

            effect_type = self.logger.get_message(
                namespace="effects", message_group="TYPES", key=item.type.value.lower()
            )

            page_data.append(
                [
                    f"[{idx+1}]",
                    effect_keyword,
                    effect_type,
                ]
            )

        return page_data

    def get_options_messages(self) -> CompendiumOptionsMessages:
        """
        Return the messages that will be used on the Compendium's options.
        """
        options_messages = {}

        for option in [
            "exit",
            "next_page",
            "previous_page",
            "return_to_pages",
            "select_option",
        ]:
            options_messages[option] = self.logger.get_message(
                namespace="base",
                message_group="COMPENDIUM",
                key=option,
            )

        for option in [
            "next_item",
            "previous_item",
            "select_item",
            "show_item_details",
        ]:
            options_messages[option] = self.logger.get_message(
                namespace="effects",
                message_group="COMPENDIUM",
                key=option,
            )

        return options_messages

    def show_item(self):
        """
        Shows the current item.
        """
        item: Effect = self.items[self.item_number - 1]

        message = self.logger.get_message(
            namespace="effects",
            message_group="KEYWORDS",
            key=item.keyword.value.lower(),
        )
        message = self.title + ": " + message

        self.logger.box_message(
            message=message,
            size=50,
        )

        # Keyword
        message = self.logger.get_colored_message(
            namespace="effects",
            message_group="KEYWORDS",
            keyword=item.keyword,
        )
        self.logger.log(message=message + "\n")

        # Description
        self.logger.log_effect_description(
            effect=item,
            params="name",
        )
        self.logger.log(message="")
