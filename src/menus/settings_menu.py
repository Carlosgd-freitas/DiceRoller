"""Settings Menu module."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, List

from src.base.color import color_string
from src.locales.languages import Language
from src.logger.logger import Logger
from src.menus.menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.systems.settings import Settings


class SettingsMenu(Menu):
    """
    Settings Menu class.

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

    def get_title(self) -> str:
        """
        Returns the Menu's title.
        """
        return self.logger.get_message(
            namespace="settings", message_group="MENU", key="title"
        )

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.
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
                id="END_TURN_AI_MONSTERS",
                key="2",
                message=self.logger.get_message(
                    namespace="settings",
                    message_group="SETTINGS",
                    key="end_turn_ai_monsters",
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
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        return True

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "LANGUAGE":
            self.settings.switch_setting(
                "language",
                [Language.EN_US, Language.PT_BR],
            )
            self.change_language(self.settings.language)

        elif option.id == "END_TURN_AI_MONSTERS":
            self.settings.switch_setting(
                "end_turn_ai_monsters",
                ["AUTO", "MANUAL"],
            )

        elif option.id == "EXIT":
            self.settings.save()

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_title(self):
        """
        Shows the Menu's title.
        """
        self.logger.box_message(
            message=self.title,
            size=50,
        )

    def show_options(self):
        """
        Shows the Menu's options.
        """
        for option in self.options:
            message = ""

            if option.isolate:
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

            if option.isolate:
                message += "\n"

            self.logger.log(message=message)

        return
