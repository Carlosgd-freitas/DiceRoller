"""Compendium module."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from math import ceil
from typing import TYPE_CHECKING, Callable, Dict, List, Tuple, TypedDict, TypeVar

from tabulate import tabulate

from src.base.color import Color, color_string
from src.base.text import normalize
from src.locales.languages import Language
from src.menus.menu import Menu
from src.menus.option import Option
from src.menus.sort_menu import SortMenu

T = TypeVar("T")

if TYPE_CHECKING:
    from src.logger.logger import Logger
    from src.systems.settings import Settings


class CompendiumLevel(Enum):
    """Compendium Level."""

    ITEM = "ITEM"
    PAGE = "PAGE"


class CompendiumMessages(TypedDict):
    """
    Compendium Messages.

    :var item_not_found: 'Item not found' message.
    :vartype item_not_found: str

    :var search_prompt: Message for the 'Search' input prompt.
    :vartype search_prompt: str

    :var select_item_prompt: Message for the 'Select Item' input prompt.
    :vartype select_item_prompt: str
    """

    item_not_found: str
    search_prompt: str
    select_item_prompt: str


class Compendium(Menu):
    """
    Compendium class.

    :var logger: Logger used to print the Compendium.
    :vartype logger: Logger

    :var settings: Game settings.
    :vartype settings: Settings

    :var title: Compendium's title.
    :vartype title: str

    :var items: Compendium's main content.
    :vartype items: List[T]

    :var columns: Names of the Compendium's columns (Headers).
    :vartype columns: List[str]

    :var alignments: Alignments of the Compendium's columns. Default value is None
    (`tabulate` default column alignment).
    :vartype alignments: Tuple[str]

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
        settings: Settings,
        items: List[T],
        alignments: Tuple[str] = None,
        page_number: int = 1,
        page_size: int = 15,
    ):
        # Compendium Attributes
        super().__init__(
            logger,
            settings,
        )
        self.items = items

        # Page Attributes
        self.page_number = page_number
        self.page_size = page_size
        self.num_pages = ceil(len(self.items) / self.page_size)

        # Item Attributes
        self.item_number = 1

        # Setup
        self.level: CompendiumLevel = CompendiumLevel.PAGE
        self.columns = self.get_columns()
        self.alignments = alignments
        self.options = self.get_options()
        self.messages = self.get_messages()

        # Sort Attributes
        self.column_index = 1
        self.reverse = False

        sort_menu_title = (
            self.title
            + ": "
            + self.logger.get_message(
                namespace="compendium",
                message_group="BASE",
                key="sort",
            ).title()
        )

        self.sort_menu = SortMenu(
            title=sort_menu_title,
            columns=self.columns,
            items=self.items,
            column_index=self.column_index,
            get_sort_key=self.get_sort_key,
            reverse=self.reverse,
            settings=self.settings,
        )

    @abstractmethod
    def get_columns(self) -> List[str]:
        """
        Returns the Compendium's columns.

        :return: List of Compendium's columns.
        :rtype: List[str]
        """
        raise NotImplementedError

    def get_options(self) -> Dict:
        """
        Returns the options that will be used by the Compendium.

        :return: Options that can be selected. Each key is a Compendium level and each
        value are the available options.
        :rtype: Dict
        """
        options = {
            "ITEM": self.get_item_options(),
            "PAGE": self.get_page_options(),
        }

        return options

    def get_page_options(self) -> List[Option]:
        """
        Returns the options that will be used in the Compendium at PAGE level.

        :return: List of options that can be selected at PAGE level.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="PREVIOUS_PAGE",
                key="1",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="previous_page",
                ),
            ),
            Option(
                id="NEXT_PAGE",
                key="2",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="next_page",
                ),
            ),
            Option(
                id="SEARCH",
                key="3",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="search",
                ),
            ),
            Option(
                id="SORT",
                key="4",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="sort",
                ),
            ),
            Option(
                id="SHOW_DETAILS",
                key="5",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="BASE",
                    key="show_details",
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

    @abstractmethod
    def get_item_options(self) -> List[Option]:
        """
        Returns the options that will be used in the Compendium at ITEM level.

        :return: List of options that can be selected at ITEM level.
        :rtype: List[Option]
        """
        raise NotImplementedError

    @abstractmethod
    def get_messages(self) -> CompendiumMessages:
        """
        Returns messages that will be used by the Compendium.

        :return: Messages that will be used by the Compendium.
        :rtype: CompendiumMessages
        """
        raise NotImplementedError

    # =========================================================================
    # Utility
    # =========================================================================

    def change_language(self, language: Language, _messages: Dict = None):
        """
        Changes the Compendium's language.

        :param language: A Language.
        :type language: Language

        :param _messages: Messages loaded from a locale module.
        :type _messages: Dict
        """
        self.logger.change_language(language, _messages)

        self.title = self.get_title()
        self.columns = self.get_columns()
        self.options = self.get_options()
        self.messages = self.get_messages()
        self.pages_data = self.get_pages_data(self.items)

    # =========================================================================
    # Data access
    # =========================================================================

    @abstractmethod
    def get_pages_data(self, items: List[T]) -> List[List]:
        """
        Returns all the tabulated data that will be used on the Compendium.

        :param items: Compendium items.
        :type items: List[T]

        :return: Compendium items structured as tabulated data.
        :rtype: List[List]
        """
        raise NotImplementedError

    def get_page_data(self, page_number: int) -> List[List]:
        """
        Returns the tabulated data from a Compendium's page.

        :param page_number: Compendium's page number.
        :type page_number: int

        :return: Compendium items structured as tabulated data for one page.
        :rtype: List[List]
        """
        return self.pages_data[
            ((page_number - 1) * self.page_size) : (page_number * self.page_size)
        ]

    def get_page_items(self, page_number: int) -> List:
        """
        Returns the items from a Compendium's page.

        :param page_number: Compendium's page number.
        :type page_number: int

        :return: Compendium items structured as tabulated data for one page.
        :rtype: List[List]
        """
        return self.items[
            ((page_number - 1) * self.page_size) : (page_number * self.page_size)
        ]

    def get_page_items_indexes(self, page_number: int) -> List[int]:
        """
        Returns the items indexes from a Compendium's page.

        :param page_number: Compendium's page number.
        :type page_number: int

        :return: Compendium items structured as tabulated data for one page.
        :rtype: List[int]
        """
        page_items = self.get_page_items(page_number)
        initial_index = ((page_number - 1) * self.page_size) + 1

        return range(initial_index, initial_index + len(page_items))

    @abstractmethod
    def get_item_name(self, item: T) -> str:
        """
        Returns the name of an item.

        :param item: A Compendium's item.
        :type item: T

        :return: The Compendium's item name.
        :rtype: str
        """
        raise NotImplementedError

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
        if option.id == "PREVIOUS_PAGE":
            return self.page_number > 1

        elif option.id == "NEXT_PAGE":
            return self.page_number < self.num_pages

        elif option.id == "PREVIOUS_ITEM":
            return self.item_number > 1

        elif option.id == "NEXT_ITEM":
            return self.item_number < len(self.items)

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param option: Compendium's option.
        :type option: Option
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

        elif option.id == "SORT":
            self.sort()

        elif option.id == "SHOW_DETAILS":
            self.show_details()

        elif option.id == "RETURN":
            self.level = CompendiumLevel.PAGE

        elif option.id == "EXIT":
            pass

        return

    def search_item(self):
        """
        Prompts the user to type an item's name, and if the item is:
        * found, switches the Compendium's level to ITEM and updates the current item
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
            self.page_number = ceil(self.item_number / self.page_size)

        else:
            self.logger.log(message=self.messages["item_not_found"], end="")
            self.logger.input(message="")

        return

    def show_details(self):
        """
        Prompts the user to select one of the Compendium page's items, and if:
        * the cancel index is selected, the operation is canceled.
        * a valid index is selected, switches the Compendium's level to ITEM and
        updates the current item number.
        * an invalid index is selected, the prompt will repeat.
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

        if selected_item_number:
            self.level = CompendiumLevel.ITEM
            self.item_number = selected_item_number

        else:
            self.level = CompendiumLevel.PAGE

        return

    @abstractmethod
    def get_sort_key(self, column_index: int) -> Callable:
        """
        Returns a key (lambda function) to be used in the sort option.

        :param column_index: Index of the column used to sort the Compendium items.
        :type column_index: int

        :return: Key (lambda function) to sort the Compendium items.
        :rtype: Callable
        """
        raise NotImplementedError

    def sort(self):
        """
        Opens up a Sort Menu, where the user can change the Compendium's sort settings.
        """
        sort_data = self.sort_menu.open()

        # Updating attributes
        self.column_index = sort_data["column_index"]
        self.items = sort_data["items"]
        self.reverse = sort_data["reverse"]

        self.pages_data = self.get_pages_data(self.items)

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_title(self):
        """
        Shows the Compendium's title.
        """
        pass

    def show_options(self, level: CompendiumLevel):
        """
        Shows the options based on the Compendium level.

        :param level: Compendium level.
        :type level: CompendiumLevel
        """
        for option in self.options[level.value]:
            option: Option
            message = ""

            if option.isolate_before:
                message += "\n"

            message += f"[{option.key}] {option.message}"

            if option.isolate_after:
                message += "\n"

            if not self.is_option_valid(option):
                message = color_string(message, foreground_color=Color.RED)

            self.logger.log(message=message)

        if not self.options[level.value][-1].isolate_after:
            self.logger.log(message="")

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
            headers=self.columns,
            colalign=self.alignments,
            tablefmt="psql",
        )

        self.logger.log(message=table + "\n")

    @abstractmethod
    def show_item(self):
        """
        Shows the current item.
        """
        raise NotImplementedError

    def open(self):
        """
        Opens the Compendium on current page.
        """
        # Default sorting
        self.items = self.sort_menu.sort(self.column_index, self.reverse)
        self.pages_data = self.get_pages_data(self.items)

        # Current page showing
        self.show_page()

        while True:
            # Options
            self.show_options(self.level)

            message = self.logger.get_message(
                namespace="menus",
                message_group="BASE",
                key="select_option_prompt",
            )
            selected = self.select(self.options[self.level.value], message)

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
