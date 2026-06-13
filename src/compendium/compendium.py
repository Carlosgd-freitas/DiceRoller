"""Compendium module."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from math import ceil
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, TypedDict

from tabulate import tabulate

from src.base.color import Color, color_string
from src.base.text import normalize
from src.menus.menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.logger.logger import Logger


class CompendiumLevel(Enum):
    """Compendium Level."""

    ITEM = "ITEM"
    PAGE = "PAGE"


class CompendiumMessages(TypedDict):
    """
    Compendium Messages.

    :var item_not_found_message: 'Item not found' message.
    :vartype item_not_found_message: str

    :var search_prompt: Message for the 'Search' input prompt.
    :vartype search_prompt: str

    :var select_item_prompt: Message for the 'Select Item' input prompt.
    :vartype select_item_prompt: str
    """

    item_not_found_message: str
    search_prompt: str
    select_item_prompt: str


class Compendium(Menu):
    """
    Compendium class.

    :var logger: Logger used to print the Compendium.
    :vartype logger: Logger

    :var title: Compendium's title.
    :vartype title: str

    :var items: Compendium's main content.
    :vartype items: List

    :var page_headers: Headers of the Compendium's columns.
    :vartype page_headers: List[str]

    :var page_colalign: Alignment of the Compendium's columns. Default value is None
    (`tabulate` default column alignment).
    :vartype page_colalign: Tuple[str]

    :var page_number: Compendium's current page number. Default value is 1.
    :vartype page_number: int

    :var page_size: Compendium's page size. Default value is 15.
    :vartype page_size: int
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        logger: Logger,
        title: str,
        items: List,
        page_headers: List[str],
        page_colalign: Tuple[str] = None,
        page_number: int = 1,
        page_size: int = 15,
    ):
        # Compendium Attributes
        super().__init__(
            logger,
        )
        self.title = title
        self.items = items

        # Page Attributes
        self.page_number = page_number
        self.page_size = page_size
        self.num_pages = ceil(len(self.items) / self.page_size)
        self.pages_data = self.get_pages_data(self.items)

        self.page_headers = page_headers
        self.page_colalign = page_colalign

        self.item_number = 1

        # Setup
        self.level: CompendiumLevel = CompendiumLevel.PAGE
        self.options = self.get_options()
        self.messages = self.get_messages()

    def get_options(self) -> Dict:
        """
        Returns the options that will be used by the Compendium.
        """
        options = {
            "ITEM": self.get_item_options(),
            "PAGE": self.get_page_options(),
        }

        return options

    def get_page_options(self) -> List[Option]:
        """
        Returns the options that will be used in the Compendium at PAGE level.
        """
        options = [
            Option(
                id="PREVIOUS_PAGE",
                key="1",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="previous_page_message",
                ),
            ),
            Option(
                id="NEXT_PAGE",
                key="2",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="next_page_message",
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
                id="SHOW_DETAILS",
                key="4",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="show_details_message",
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

    @abstractmethod
    def get_item_options(self) -> List[Option]:
        """
        Returns the options that will be used in the Compendium at ITEM level.
        """
        raise NotImplementedError

    def select_option(self) -> Option:
        """
        Prompts the user to select one of the Compendium's options:
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

            for option in self.options[self.level.value]:
                option: Option

                if selected == option.key:
                    return option

    @abstractmethod
    def get_messages(self) -> CompendiumMessages:
        """
        Returns messages that will be used by the Compendium.
        """
        raise NotImplementedError

    # =========================================================================
    # Data access
    # =========================================================================

    @abstractmethod
    def get_pages_data(self, items: List) -> List[List]:
        """
        Returns all the tabulated data that will be used on the Compendium.

        :var items: Compendium items.
        :vartype items: List

        :return: Compendium items structured as tabulated data.
        :rtype: List[List]
        """
        raise NotImplementedError

    def get_page_data(self, page_number: int) -> List[List]:
        """
        Returns the tabulated data from a Compendium's page.

        :var page_number: Compendium's page number.
        :vartype page_number: int

        :return: Compendium items structured as tabulated data for one page.
        :rtype: List[List]
        """
        return self.pages_data[
            ((page_number - 1) * self.page_size) : (page_number * self.page_size)
        ]

    def get_page_items(self, page_number: int) -> List:
        """
        Returns the items from a Compendium's page.

        :var page_number: Compendium's page number.
        :vartype page_number: int

        :return: Compendium items structured as tabulated data for one page.
        :rtype: List[List]
        """
        return self.items[
            ((page_number - 1) * self.page_size) : (page_number * self.page_size)
        ]

    def get_page_items_indexes(self, page_number: int) -> List[int]:
        """
        Returns the items indexes from a Compendium's page.

        :var page_number: Compendium's page number.
        :vartype page_number: int

        :return: Compendium items structured as tabulated data for one page.
        :rtype: List[int]
        """
        page_items = self.get_page_items(page_number)
        initial_index = ((page_number - 1) * self.page_size) + 1

        return range(initial_index, initial_index + len(page_items))

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id == "PREVIOUS_PAGE":
            return self.page_number > 1

        elif option.id == "NEXT_PAGE":
            return self.page_number < self.num_pages

        elif option.id == "PREVIOUS_ITEM":
            return self.item_number > 1

        elif option.id == "NEXT_ITEM":
            return self.item_number < len(self.items)

        return True

    @abstractmethod
    def get_item_name(self, item: Any) -> str:
        """
        Returns the name of an item.

        :var item: A Compendium's item.
        :vartype item: Any

        :return: The Compendium's item name.
        :rtype: str
        """
        raise NotImplementedError

    # =========================================================================
    # Options
    # =========================================================================

    def search_item(self):
        """
        Prompts the user to type an item's name, and if the item is:
        * found, switches the Compedium's level to "ITEM" and updates the current item
        number.
        * not found, logs a message.
        """
        name = self.logger.input(message=self.messages["search_prompt"])
        normalized_name = normalize(name)

        item_number = None

        for index, item in enumerate(self.items):
            item_name = normalize(self.get_item_name(item))

            if normalized_name == item_name:
                item_number = index + 1
                break

        if item_number:
            self.level = CompendiumLevel.ITEM
            self.item_number = item_number

        else:
            self.logger.log(message=self.messages["item_not_found_message"], end="")
            self.logger.input(message="")

        return

    def select_item(self) -> int:
        """
        Prompts the user to select one of the Compendium page's items:
        * if a valid index is selected, it will be returned.
        * if an invalid index is selected, the prompt will repeat.

        A valid index is either 0 (which will cancel the operation) or an item index
        that shows in the page.

        :return: The index of the selected item.
        :rtype: int
        """
        page_items_idx = self.get_page_items_indexes(self.page_number)

        while True:
            selected_item_number = self.logger.input(
                message=self.messages["select_item_prompt"]
            )

            try:
                selected_item_number = int(selected_item_number)

                if selected_item_number == 0 or selected_item_number in page_items_idx:
                    break

            except Exception:
                continue

        return selected_item_number

    # =========================================================================
    # Rendering
    # =========================================================================

    @abstractmethod
    def show_item(self):
        """
        Shows the current item.
        """
        raise NotImplementedError

    def show_options(self, level: CompendiumLevel):
        """
        Shows the options based on the Compendium level.

        :var level: Compendium level.
        :vartype level: CompendiumLevel
        """
        for option in self.options[level.value]:
            option: Option
            message = ""

            if option.isolate:
                message += "\n"

            message = f"[{option.key}] {option.message}"

            if option.isolate:
                message += "\n"

            if not self.is_option_valid(option):
                message = color_string(message, foreground_color=Color.RED)

            self.logger.log(message=message)

        if not self.options[level.value][-1].isolate:
            self.logger.log(message="")

        return

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "PREVIOUS_PAGE":
            if self.page_number > 1:
                self.page_number -= 1

        elif option.id == "NEXT_PAGE":
            if self.page_number < self.num_pages:
                self.page_number += 1

        elif option.id == "PREVIOUS_ITEM":
            if self.item_number > 1:
                self.item_number -= 1
            self.page_number = ceil(self.item_number / self.page_size)

        elif option.id == "NEXT_ITEM":
            if self.item_number < len(self.items):
                self.item_number += 1
            self.page_number = ceil(self.item_number / self.page_size)

        elif option.id == "SEARCH":
            self.search_item()
            self.page_number = ceil(self.item_number / self.page_size)

        elif option.id == "SHOW_DETAILS":
            selected_item_number = self.select_item()

            if selected_item_number:
                self.item_number = selected_item_number
                self.level = CompendiumLevel.ITEM
            else:
                self.level = CompendiumLevel.PAGE

        elif option.id == "RETURN":
            self.level = CompendiumLevel.PAGE

        elif option.id == "EXIT":
            pass

        return

    def show_page(self):
        """
        Shows the current page.
        """
        message = self.logger.get_message(
            namespace="compendium", message_group="BASE", key="page"
        )
        message = self.title + ": " + message + " " + str(self.page_number)

        self.logger.box_message(
            message=message,
            size=50,
        )

        page_data = self.get_page_data(self.page_number)

        table = tabulate(
            page_data,
            headers=self.page_headers,
            colalign=self.page_colalign,
            tablefmt="psql",
        )

        self.logger.log(message=table + "\n")

    def open(self):
        """
        Opens the Compendium on current page.
        """
        # Current page showing
        self.show_page()

        while True:
            # Options
            self.show_options(self.level)
            selected = self.select_option()

            # Option processing
            if selected.id == "EXIT":
                break

            elif self.is_option_valid(selected):
                self.process_option(selected)

            else:
                self.logger.log(message="")

            # Showing Content
            if self.level == CompendiumLevel.PAGE:
                self.show_page()
            elif self.level == CompendiumLevel.ITEM:
                self.show_item()

        return
