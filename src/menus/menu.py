"""Menu module."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Dict, List

from src.base.color import Color, color_string
from src.base.manager import Manager
from src.locales.languages import Language

if TYPE_CHECKING:
    from src.logger.logger import Logger
    from src.menus.option import Option
    from src.systems.settings import Settings


class Menu(Manager):
    """
    Menu class.

    :var logger: Logger used to print the Menu.
    :vartype logger: Logger

    :var settings: Game settings.
    :vartype settings: Settings

    :var title: Menu's title.
    :vartype title: str
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        logger: Logger,
        settings: Settings,
    ):
        super().__init__(
            logger,
            settings,
        )

        self.title = self.get_title()
        self.options = self.get_options()

    @abstractmethod
    def get_title(self) -> str:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def get_options(self) -> List[Option]:
        """
        Returns the Menu options.

        :return: Menu options.
        :rtype: List[Option]
        """
        raise NotImplementedError

    # =========================================================================
    # Utility
    # =========================================================================

    def change_language(self, language: Language, _messages: Dict = None):
        """
        Changes the Manager language.

        :param language: A Language.
        :type language: Language

        :param _messages: Messages loaded from a locale module.
        :type _messages: Dict
        """
        if self.logger:
            self.logger.change_language(language, _messages)

        self.title = self.get_title()
        self.options = self.get_options()

    # =========================================================================
    # Options
    # =========================================================================

    def select_option(self) -> Option:
        """
        Prompts the user to select one of the Menu's options:
        * if a valid option is selected, it will be returned.
        * if an invalid option is selected, the prompt will repeat.

        :return: The option selected by the user.
        :rtype: Option
        """
        while True:
            message = self.logger.get_message(
                namespace="menus",
                message_group="BASE",
                key="select_option_prompt",
            )

            selected = self.logger.input(message=message)

            for option in self.options:
                if selected == option.key:
                    return option

    @abstractmethod
    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.

        :param option: Menu's option.
        :type option: Option

        :return: If the option can be selected.
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def process_option(self, option: Option):
        """
        Processes an option.

        :param option: Menu's option.
        :type option: Option
        """
        raise NotImplementedError

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_title(self):
        """
        Shows the Menu title.
        """
        self.logger.box_message(
            message=self.title,
            size=50,
        )

    def show_options(self):
        """
        Shows the Menu options.
        """
        for option in self.options:
            message = ""

            if option.isolate_before:
                message += "\n"

            message += f"[{option.key}] {option.message}"

            if option.isolate_after:
                message += "\n"

            if not self.is_option_valid(option):
                message = color_string(message, foreground_color=Color.RED)

            self.logger.log(message=message)

        if not self.options[-1].isolate_after:
            self.logger.log(message="")

        return

    def open(self):
        """
        Opens the Menu.
        """
        while True:
            self.show_title()
            self.show_options()
            selected = self.select_option()

            if self.is_option_valid(selected):
                self.process_option(selected)

            if selected.id in ["EXIT", "RETURN"]:
                break

            else:
                self.logger.log(message="")

        return
