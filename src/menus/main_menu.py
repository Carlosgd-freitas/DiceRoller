"""Main Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.compendium.effects import EffectCompendium
from src.gamemodes import sandbox
from src.locales.languages import Language
from src.logger.logger import Logger
from src.menus.menu import Menu
from src.menus.option import Option
from src.menus.settings_menu import SettingsMenu

if TYPE_CHECKING:
    from src.systems.settings import Settings


class MainMenu(Menu):
    """
    Main Menu class.

    :var settings: Game settings.
    :vartype settings: Settings
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        settings: Settings,
    ):
        logger = Logger(language=settings.language)

        super().__init__(
            logger,
            settings,
        )

        self.effect_compendium = EffectCompendium(self.settings)
        self.settings_menu = SettingsMenu(self.settings)

    def get_title(self) -> str:
        """
        Returns the Menu's title.
        """
        return self.logger.get_message(
            namespace="menus", message_group="MAIN", key="title"
        )

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
                    namespace="compendium",
                    message_group="EFFECTS",
                    key="title",
                ),
            ),
            Option(
                id="SETTINGS",
                key="4",
                message=self.logger.get_message(
                    namespace="settings",
                    message_group="MENU",
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
        # Changing self language
        self.logger.change_language(language)
        self.title = self.get_title()
        self.options = self.get_options()

        # Changing other menus languages
        self.effect_compendium.change_language(language)
        self.settings_menu.change_language(language)

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id in ["NEW_GAME"]:
            return False

        return True

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "NEW_GAME":
            pass

        elif option.id == "SANDBOX_MODE":
            sandbox.run(self.settings, teams_size=3)

        elif option.id == "EFFECT_COMPENDIUM":
            self.effect_compendium.open()

        elif option.id == "SETTINGS":
            self.settings_menu.open()
            self.settings.load()
            self.change_language(self.settings.language)

        elif option.id == "EXIT":
            pass

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_title(self):
        """
        Shows the Menu's title.
        """
        self.logger.box_message(
            message="DiceRoller v0.1.X",
            size=50,
        )
