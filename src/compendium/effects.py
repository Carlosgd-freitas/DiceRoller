"""Effect Compendium module."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, List

from src.compendium.compendium import Compendium, CompendiumMessages
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.bleed import BleedEffect
from src.effects.blind import BlindEffect
from src.effects.block import BlockEffect
from src.effects.burn import BurnEffect
from src.effects.cleanse import CleanseEffect
from src.effects.confuse import ConfuseEffect
from src.effects.corrupt import CorruptEffect
from src.effects.curse import CurseEffect
from src.effects.doom import DoomEffect
from src.effects.drain import DrainEffect
from src.effects.execute import ExecuteEffect
from src.effects.focus import FocusEffect
from src.effects.freeze import FreezeEffect
from src.effects.heal import HealEffect
from src.effects.invisible import InvisibleEffect
from src.effects.mana import ManaEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.nothing import NothingEffect
from src.effects.pierce import PierceEffect
from src.effects.poison import PoisonEffect
from src.effects.regen import RegenEffect
from src.effects.revive import ReviveEffect
from src.effects.sacred_block import SacredBlockEffect
from src.effects.sleep import SleepEffect
from src.effects.stun import StunEffect
from src.effects.thorns import ThornsEffect
from src.locales.languages import Language
from src.logger.effects import EffectLogger
from src.menus.option import Option

if TYPE_CHECKING:
    from src.base.effect import Effect


ALL_EFFECTS = [
    AbsorbEffect(),
    AttackEffect(),
    BleedEffect(),
    BlindEffect(),
    BlockEffect(),
    BurnEffect(),
    CleanseEffect(),
    ConfuseEffect(),
    CorruptEffect(),
    CurseEffect(),
    DoomEffect(),
    DrainEffect(),
    ExecuteEffect(),
    FocusEffect(),
    FreezeEffect(),
    HealEffect(),
    InvisibleEffect(),
    ManaEffect(),
    ManaRegenEffect(),
    NothingEffect(),
    PierceEffect(),
    PoisonEffect(),
    RegenEffect(),
    ReviveEffect(),
    SacredBlockEffect(),
    SleepEffect(),
    StunEffect(),
    ThornsEffect(),
]


def get_all_effects() -> List[Effect]:
    return deepcopy(ALL_EFFECTS)


class EffectCompendium(Compendium):
    """
    Effect Compendium class.
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        language: Language = Language.EN_US,
    ):
        items = get_all_effects()

        logger = EffectLogger(language=language)

        title = logger.get_message(
            namespace="compendium", message_group="EFFECTS", key="title"
        )

        super().__init__(
            logger=logger,
            title=title,
            items=items,
            page_headers=["#", "Name", "Type"],
            page_colalign=("right", "left", "left"),
        )

        self.logger: EffectLogger

    def get_item_options(self) -> List[Option]:
        """
        Returns the options that will be used in the Compendium at ITEM level.
        """
        options = [
            Option(
                id="PREVIOUS_ITEM",
                key="1",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="EFFECTS",
                    key="previous_item_message",
                ),
            ),
            Option(
                id="NEXT_ITEM",
                key="2",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="EFFECTS",
                    key="next_item_message",
                ),
            ),
            Option(
                id="SEARCH",
                key="3",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="search_message",
                ),
            ),
            Option(
                id="RETURN",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="return_message",
                ),
                isolate=True,
            ),
        ]

        return options

    def get_messages(self) -> CompendiumMessages:
        """
        Returns messages that will be used by the Compendium.
        """
        messages = {}

        for key in [
            "item_not_found_message",
            "search_prompt",
            "select_item_prompt",
        ]:
            messages[key] = self.logger.get_message(
                namespace="compendium",
                message_group="EFFECTS",
                key=key,
            )

        return messages

    # =========================================================================
    # Data access
    # =========================================================================

    def get_pages_data(self, items: List[Effect]) -> List[List]:
        """
        Returns all the tabulated data that will be used on the Compendium.

        :var items: Compendium items.
        :vartype items: List

        :return: Compendium items structured as tabulated data.
        :rtype: List[List]
        """
        pages_data = []

        for idx, item in enumerate(items):
            effect_keyword = self.logger.get_colored_message(
                namespace="effects",
                message_group="KEYWORDS",
                keyword=item.keyword,
            )

            effect_type = self.logger.get_message(
                namespace="effects", message_group="TYPES", key=item.type.value.lower()
            )

            pages_data.append(
                [
                    f"[{idx+1}]",
                    effect_keyword,
                    effect_type,
                ]
            )

        return pages_data

    def get_item_name(self, item: Effect) -> str:
        """
        Returns the name of an item.

        :var item: A Compendium's item.
        :vartype item: Any

        :return: The Compendium's item name.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="effects",
            message_group="KEYWORDS",
            key=item.keyword.value.lower(),
        )

    # =========================================================================
    # Rendering
    # =========================================================================

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
