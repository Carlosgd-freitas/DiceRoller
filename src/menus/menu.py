"""Menu module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from src.base.color import Color, color_string
from src.locales.languages import Language

if TYPE_CHECKING:
    from src.logger.logger import Logger
    from src.menus.option import Option


class Menu(ABC):
    """
    Menu class.

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
        self.logger = logger
        self.options = self.get_options()

    @abstractmethod
    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.
        """
        raise NotImplementedError

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

    # =========================================================================
    # Options
    # =========================================================================

    @abstractmethod
    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        raise NotImplementedError

    @abstractmethod
    def process_option(self, option: Option):
        """
        Processes an option.
        """
        raise NotImplementedError

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

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_options(self):
        """
        Shows the Menu's options.
        """
        for option in self.options:
            message = ""

            if option.isolate:
                message += "\n"

            message = f"[{option.key}] {option.message}"

            if option.isolate:
                message += "\n"

            if not self.is_option_valid(option):
                message = color_string(message, foreground_color=Color.RED)

            self.logger.log(message=message)

        if not self.options[-1].isolate:
            self.logger.log(message="")

        return

    def open(self):
        """
        Opens the Menu.
        """
        while True:
            self.show_options()
            selected = self.select_option()

            if selected.id in ["EXIT", "RETURN"]:
                break

            elif self.is_option_valid(selected):
                self.process_option(selected)

            else:
                self.logger.log(message="")

        return
