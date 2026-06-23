"""Main Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.compendium.effects import EffectCompendium
from src.gamemodes.sandbox.sandbox_menu import SandboxMenu
from src.locales.languages import Language
from src.logger.logger import Logger
from src.menus.menu import Menu
from src.menus.option import Option
from src.menus.settings_menu import SettingsMenu
from src.systems.file import FileManager

if TYPE_CHECKING:
    from src.systems.settings import Settings


class MainMenu(Menu):
    """
    Main Menu class.

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

        # Managers
        self.file_manager = FileManager(settings, logging)

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

        self.file_manager.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Menu logging.

        :var enabled: If the Menu logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled
        self.file_manager.toggle_logging(enabled)

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
            sandbox_menu = SandboxMenu(self.settings, self.logger.enabled)
            sandbox_menu.open()

        elif option.id == "EFFECT_COMPENDIUM":
            effect_compendium = EffectCompendium(self.settings, self.logger.enabled)
            effect_compendium.open()

        elif option.id == "SETTINGS":
            settings_menu = SettingsMenu(self.settings, self.logger.enabled)
            settings_menu.open()
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
