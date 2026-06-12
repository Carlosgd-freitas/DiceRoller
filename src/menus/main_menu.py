"""Main Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.compendium.effects import EffectCompendium
from src.locales.languages import Language
from src.menus.menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.logger.logger import Logger


class MainMenu(Menu):
    """
    Main Menu class.

    :var logger: Logger used to print the Menu.
    :vartype logger: Logger
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        logger: Logger,
    ):
        super().__init__(
            logger,
        )
        self.effect_compendium = EffectCompendium(self.logger.language)

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.
        """
        options = [
            Option(
                id="NEW_GAME",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="MAIN",
                    key="new_game",
                ),
            ),
            Option(
                id="SANDBOX_MODE",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="MAIN",
                    key="sandbox_mode",
                ),
            ),
            Option(
                id="EFFECT_COMPENDIUM",
                key="3",
                message=self.logger.get_message(
                    namespace="effects",
                    message_group="COMPENDIUM",
                    key="title",
                ),
            ),
            Option(
                id="CONFIGURATIONS",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="CONFIGURATIONS",
                    key="title",
                ),
            ),
            Option(
                id="EXIT",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="exit_message",
                ),
                isolate=True,
            ),
        ]

        return options

    # =========================================================================
    # Utility
    # =========================================================================

    def change_language(self, language: Language):
        """
        Changes the Menu's language.

        :var language: A Language.
        :vartype language: Language
        """
        self.logger.change_language(language)
        self.effect_compendium.logger._messages = self.logger._messages

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id in ["NEW_GAME", "SANDBOX_MODE", "CONFIGURATIONS"]:
            return False

        return True

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "NEW_GAME":
            pass

        elif option.id == "SANDBOX_MODE":
            pass

        elif option.id == "EFFECT_COMPENDIUM":
            self.effect_compendium.open()

        elif option.id == "CONFIGURATIONS":
            pass

        elif option.id == "EXIT":
            pass

        return
