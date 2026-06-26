"""Effect Compendium module."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Callable, List

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
from src.effects.doom import DoomEffect
from src.effects.drain import DrainEffect
from src.effects.execute import ExecuteEffect
from src.effects.focus import FocusEffect
from src.effects.fortify import FortifyEffect
from src.effects.fragile import FragileEffect
from src.effects.freeze import FreezeEffect
from src.effects.frostburn import FrostburnEffect
from src.effects.haste import HasteEffect
from src.effects.heal import HealEffect
from src.effects.immunity import ImmunityEffect
from src.effects.invisible import InvisibleEffect
from src.effects.invulnerable import InvulnerableEffect
from src.effects.mana import ManaEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.nothing import NothingEffect
from src.effects.oil import OilEffect
from src.effects.pain import PainEffect
from src.effects.pierce import PierceEffect
from src.effects.poison import PoisonEffect
from src.effects.regen import RegenEffect
from src.effects.revive import ReviveEffect
from src.effects.sacred_block import SacredBlockEffect
from src.effects.sleep import SleepEffect
from src.effects.slow import SlowEffect
from src.effects.strength import StrengthEffect
from src.effects.stun import StunEffect
from src.effects.taunt import TauntEffect
from src.effects.thorns import ThornsEffect
from src.effects.weak import WeakEffect
from src.logger.effects import EffectLogger
from src.menus.option import Option

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.systems.settings import Settings

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
    DoomEffect(),
    DrainEffect(),
    ExecuteEffect(),
    FocusEffect(),
    FortifyEffect(),
    FragileEffect(),
    FreezeEffect(),
    FrostburnEffect(),
    HasteEffect(),
    HealEffect(),
    ImmunityEffect(),
    InvisibleEffect(),
    InvulnerableEffect(),
    ManaEffect(),
    ManaRegenEffect(),
    NothingEffect(),
    OilEffect(),
    PainEffect(),
    PierceEffect(),
    PoisonEffect(),
    RegenEffect(),
    ReviveEffect(),
    SacredBlockEffect(),
    SleepEffect(),
    SlowEffect(),
    StrengthEffect(),
    StunEffect(),
    TauntEffect(),
    ThornsEffect(),
    WeakEffect(),
]


def get_all_effects() -> List[Effect]:
    return deepcopy(ALL_EFFECTS)


class EffectCompendium(Compendium):
    """
    Effect Compendium class.

    :var settings: Game settings.
    :vartype settings: Settings

    :var logging: If logging is enabled. Default value is True.
    :vartype logging: bool
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        settings: Settings,
        logging: bool = True,
    ):
        items = get_all_effects()

        logger = EffectLogger(enabled=logging, language=settings.language)

        super().__init__(
            logger=logger,
            settings=settings,
            items=items,
            alignments=("right", "left", "left"),
        )

        self.logger: EffectLogger

    def get_title(self) -> str:
        """
        Returns the Compendium title.

        :return: Compendium title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="compendium", message_group="EFFECTS", key="title"
        )

    def get_columns(self) -> List[str]:
        """
        Returns the Compendium columns.

        :return: List of Compendium columns.
        :rtype: List[str]
        """
        columns = ["#"]

        columns.append(
            self.logger.get_message(
                namespace="base",
                message_group="LEXICON",
                key="name",
            )
        )

        columns.append(
            self.logger.get_message(
                namespace="base",
                message_group="LEXICON",
                key="type",
            )
        )

        columns = [column.title() for column in columns]

        return columns

    def get_item_options(self) -> List[Option]:
        """
        Returns the options that will be used in the Compendium at ITEM level.

        :return: List of options that can be selected at ITEM level.
        :rtype: List[Option]
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
                isolate_before=True,
                isolate_after=True,
            ),
        ]

        return options

    def get_messages(self) -> CompendiumMessages:
        """
        Returns messages that will be used by the Compendium.

        :return: Messages that will be used by the Compendium.
        :rtype: CompendiumMessages
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

        :param items: Compendium items.
        :type items: List

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

        :param item: A Compendium item.
        :type item: Effect

        :return: The Compendium item name.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="effects",
            message_group="KEYWORDS",
            key=item.keyword.value.lower(),
        )

    # =========================================================================
    # Options
    # =========================================================================

    def get_sort_key(self, column_index: int) -> Callable:
        """
        Returns a key (lambda function) to be used in the sort option.

        :param column_index: Index of the column used to sort the Compendium items.
        :type column_index: int

        :return: Key (lambda function) to sort the Compendium items.
        :rtype: Callable
        """
        if column_index == 1:
            return lambda x: self.get_item_name(x)

        elif column_index == 2:
            return lambda x: self.logger.get_message(
                namespace="effects",
                message_group="TYPES",
                key=x.type.value.lower(),
            )

        return

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
