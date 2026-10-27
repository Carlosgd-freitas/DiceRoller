"""Confirmation Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.logger.logger import Logger
from src.menus.edit_menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.systems.settings import Settings


class ConfirmationMenu(Menu):
    """
    Confirmation Menu class.

    :var settings: Game settings.
    :vartype settings: Settings

    :var logging: If logging is enabled. Default value is True.
    :vartype logging: bool

    :var message: Optional message to log before the confirmation options.
    :vartype message: sr
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        settings: Settings,
        logging: bool = True,
        message: str = None,
    ):
        # Initialization
        logger = Logger(enabled=logging, language=settings.language)

        super().__init__(
            logger,
            settings,
        )

        self.message = message

    def get_title(self) -> str:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        pass

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.
        """
        options = [
            Option(
                id="YES",
                key="Y",
                message=self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="yes",
                ).capitalize(),
            ),
            Option(
                id="NO",
                key="N",
                message=self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="no",
                ).capitalize(),
                isolate_after=True,
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

    def process_option(self, option: Option) -> bool:
        """
        Processes an option.

        :return: If the player confirmed or not.
        :rtype: bool
        """
        if option.id == "YES":
            return True

        elif option.id == "NO":
            return False

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def open(self) -> bool:
        """
        Opens the Menu.

        :return: If the player confirmed or not.
        :rtype: bool
        """
        # Logging optional message
        if self.message:
            self.logger.log(
                message=self.message,
                end="\n\n",
            )

        self.show_options(self.options)
        selected = self.select(self.options)

        confirmation = self.process_option(selected)

        return confirmation
