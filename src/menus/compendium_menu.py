"""Compendium Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.compendium.effects import EffectCompendium
from src.locales.languages import Language
from src.logger.logger import Logger
from src.menus.menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.systems.settings import Settings


class CompendiumMenu(Menu):
    """
    Compendium Menu class.

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
        # Initialization
        logger = Logger(enabled=logging, language=settings.language)

        super().__init__(
            logger,
            settings,
        )

        self.effect_compendium = EffectCompendium(self.settings, self.logger.enabled)

    def get_title(self) -> str:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="compendium", message_group="BASE", key="title"
        )

    def get_options(self) -> List[Option]:
        """
        Returns the Menu options.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="EFFECT_COMPENDIUM",
                key="1",
                message=self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="effects",
                ).title(),
            ),
            Option(
                id="MONSTER_COMPENDIUM",
                key="2",
                message=self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="monsters",
                ).title(),
            ),
            Option(
                id="EQUIPMENT_COMPENDIUM",
                key="3",
                message=self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="equipment",
                ).title(),
            ),
            Option(
                id="CONSUMABLES_COMPENDIUM",
                key="3",
                message=self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="consumables",
                ).title(),
            ),
            Option(
                id="EXIT",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="exit_message",
                ),
                isolate_before=True,
                isolate_after=True,
            ),
        ]

        return options

    # =========================================================================
    # Utility
    # =========================================================================

    def change_language(self, language: Language, _messages: Dict = None):
        """
        Changes the Menu's language.

        :var language: A Language.
        :vartype language: Language

        :var _messages: Messages loaded from a locale module.
        :vartype _messages: Dict
        """
        self.logger.change_language(language, _messages)
        _messages = self.logger._messages

        self.title = self.get_title()
        self.options = self.get_options()

        self.effect_compendium.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Menu logging.

        :var enabled: If the Menu logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled
        self.effect_compendium.toggle_logging(enabled)

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.

        :param option: Menu's option.
        :type option: Option

        :return: If the option can be selected.
        :rtype: bool
        """
        if option.id in [
            "MONSTER_COMPENDIUM",
            "EQUIPMENT_COMPENDIUM",
            "CONSUMABLES_COMPENDIUM",
        ]:
            return False

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param option: Menu's option.
        :type option: Option
        """
        if option.id == "EFFECT_COMPENDIUM":
            self.effect_compendium.open()

        elif option.id == "MONSTER_COMPENDIUM":
            pass

        elif option.id == "EQUIPMENT_COMPENDIUM":
            pass

        elif option.id == "CONSUMABLES_COMPENDIUM":
            pass

        elif option.id == "EXIT":
            pass

        return
