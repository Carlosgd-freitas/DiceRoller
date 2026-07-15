"""Settings Menu module."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List

from src.base.color import color_string
from src.locales.languages import Language
from src.logger.logger import Logger
from src.menus.menu import Menu
from src.menus.option import Option
from src.systems.file import FileManager
from src.systems.settings import FILENAME, Settings


class SettingsMenu(Menu):
    """
    Settings Menu class.

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
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="settings", message_group="MENU", key="title"
        )

    def get_options(self) -> List[Option]:
        """
        Returns the Menu options.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="LANGUAGE",
                key="1",
                message=self.logger.get_message(
                    namespace="settings",
                    message_group="SETTINGS",
                    key="language",
                ),
            ),
            Option(
                id="MONSTER_END_TURN",
                key="2",
                message=self.logger.get_message(
                    namespace="settings",
                    message_group="SETTINGS",
                    key="monster_end_turn",
                ),
            ),
            Option(
                id="EXIT",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="exit",
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
        Changes the Manager language.

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
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
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

        :param option: Menu's option.
        :type option: Option

        :return: If the option can be selected.
        :rtype: bool
        """
        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param option: Menu's option.
        :type option: Option
        """
        if option.id == "LANGUAGE":
            self.settings.switch_setting(
                "language",
                [Language.EN_US, Language.PT_BR],
            )
            self.change_language(self.settings.language)

        elif option.id == "MONSTER_END_TURN":
            self.settings.switch_setting(
                "monster_end_turn",
                ["AUTO", "MANUAL"],
            )

        elif option.id == "EXIT":
            self.file_manager.save_file(FILENAME, self.settings)

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_options(self):
        """
        Shows the Menu options.
        """
        for option in self.options:
            message = ""

            if option.isolate_before:
                message += "\n"

            message += f"[{option.key}] {option.message}"

            if option.id != "EXIT":
                message += ": "

                setting_value = getattr(self.settings, option.id.lower())

                if isinstance(setting_value, str):
                    setting_value = setting_value.lower()
                elif isinstance(setting_value, Enum):
                    setting_value = setting_value.value.lower()

                message += color_string(
                    self.logger.get_message(
                        namespace="settings",
                        message_group="VALUES",
                        key=setting_value,
                    ),
                    intensity="BRIGHT",
                )

            if option.isolate_after:
                message += "\n"

            self.logger.log(message=message)

        return
