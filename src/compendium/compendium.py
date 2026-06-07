"""Compendium module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from math import ceil
from typing import TYPE_CHECKING, List, Literal, Tuple, TypedDict

from tabulate import tabulate

from src.base.color import Color, color_string

if TYPE_CHECKING:
    from src.logger.logger import Logger


class CompendiumOptionsMessages(TypedDict):
    """
    Compendium Option Messages.

    :var exit: Message for the 'Exit' option.
    :vartype exit: str

    :var next_item: Message for the 'Next Item' option.
    :vartype next_item: str

    :var next_page: Message for the 'Next Page' option.
    :vartype next_page: str

    :var previous_item: Message for the 'Previous Item' option.
    :vartype previous_item: str

    :var previous_page: Message for the 'Previous Page' option.
    :vartype previous_page: str

    :var return_to_pages: Message for the 'Return' option.
    :vartype return_to_pages: str

    :var select_item: Message for the 'Select Item' input prompt.
    :vartype select_item: str

    :var select_option: Message for the 'Select Option' input prompt.
    :vartype select_option: str

    :var show_item_details: Message for the 'Show Item Details' option.
    :vartype show_item_details: str
    """

    exit: str
    next_item: str
    next_page: str
    previous_item: str
    previous_page: str
    return_to_pages: str
    select_item: str
    select_option: str
    show_item_details: str


class Compendium(ABC):
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
        self.logger = logger
        self.title = title
        self.items = items
        self.options_messages = self.get_options_messages()

        self.page_number = page_number
        self.page_size = page_size
        self.num_pages = ceil(len(self.items) / self.page_size)

        self.item_number = 1

        # Page Attributes
        self.page_headers = page_headers
        self.page_colalign = page_colalign

        # Setup
        self.sort()

    @abstractmethod
    def sort(self):
        """
        .
        """
        raise NotImplementedError

    def get_page_items(self):
        """
        Returns the items for the current page.
        """
        return self.items[
            ((self.page_number - 1) * self.page_size) : (
                self.page_number * self.page_size
            )
        ]

    @abstractmethod
    def get_page_data(self, page_items: List) -> List[List]:
        """
        Returns tabulated data that will be used with `tabulate` package.

        :var page_items: A Compendium page's items.
        :vartype page_items: List

        :return: A Compendium page's items structured as tabulated data.
        :rtype: List[List]
        """
        raise NotImplementedError

    @abstractmethod
    def get_options_messages(self) -> CompendiumOptionsMessages:
        """
        Returns the messages that will be used on the Compendium's options.
        """
        raise NotImplementedError

    def show_options(self, level: Literal["ITEM", "PAGE"]):
        """
        Shows the options based on what is being displayed.

        :var level: What is being currently displayed.
        :vartype level: Literal["ITEM", "PAGE"]
        """
        if level == "ITEM":
            # Previous Item
            message = f"[1] {self.options_messages['previous_item']}"
            if self.item_number == 1:
                message = color_string(message, foreground_color=Color.RED)
            self.logger.log(message=message)

            # Next Item
            message = f"[2] {self.options_messages['next_item']}"
            if self.item_number == len(self.items):
                message = color_string(message, foreground_color=Color.RED)
            self.logger.log(message=message)

            # Return to Pages
            self.logger.log(
                message=f"\n[0] {self.options_messages['return_to_pages']}\n"
            )

        elif level == "PAGE":
            # Previous Page
            message = f"[1] {self.options_messages['previous_page']}"
            if self.page_number == 1:
                message = color_string(message, foreground_color=Color.RED)
            self.logger.log(message=message)

            # Next Page
            message = f"[2] {self.options_messages['next_page']}"
            if self.page_number == self.num_pages:
                message = color_string(message, foreground_color=Color.RED)
            self.logger.log(message=message)

            # Show Item Details
            self.logger.log(message=f"[3] {self.options_messages['show_item_details']}")

            # Exit
            self.logger.log(message=f"\n[0] {self.options_messages['exit']}\n")

        return

    def show_page(self):
        """
        Shows the current page.
        """
        self.logger.log(message="\n╔═══════════════════════════════════════════╗")
        self.logger.log(message="║ ", end="")

        message = self.logger.get_message(
            namespace="base", message_group="COMPENDIUM", key="page"
        )
        message = self.title + ": " + message + " " + str(self.page_number)

        self.logger.log(message=f"{message:41}", end="")
        self.logger.log(message=" ║\n", end="")
        self.logger.log(message="╚═══════════════════════════════════════════╝\n")

        page_items = self.get_page_items()
        page_data = self.get_page_data(page_items)

        table = tabulate(
            page_data,
            headers=self.page_headers,
            colalign=self.page_colalign,
            tablefmt="psql",
        )

        self.logger.log(message=table + "\n")

    @abstractmethod
    def show_item(self):
        """
        Shows the current item.
        """
        raise NotImplementedError

    def next_page(self):
        """
        Setup for the next page.
        """
        if self.page_number < self.num_pages:
            self.page_number += 1

    def previous_page(self):
        """
        Setup for the previous page.
        """
        if self.page_number > 1:
            self.page_number -= 1

    def next_item(self):
        """
        Setup for the next item.
        """
        if self.item_number < len(self.items):
            self.item_number += 1
            self.page_number = ceil(self.item_number / self.page_size)

    def previous_item(self):
        """
        Setup for the previous item.
        """
        if self.item_number > 1:
            self.item_number -= 1
            self.page_number = ceil(self.item_number / self.page_size)

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
        page_items = self.get_page_items()

        while True:
            page_item_number = self.logger.input(
                message=self.options_messages["select_item"]
            )

            try:
                page_item_number = int(page_item_number)
                if page_item_number in range(0, len(page_items) + 1):
                    break

            except Exception:
                continue

        return page_item_number

    def open(self):
        """
        Opens the Compendium on current page.
        """
        level = "PAGE"

        while True:
            # Showing content
            if level == "PAGE":
                self.show_page()
            elif level == "ITEM":
                self.show_item()

            self.show_options(level=level)

            # Player option input
            option = self.logger.input(message=self.options_messages["select_option"])

            # Option validation
            if level == "PAGE":
                if option == "0":
                    break

                elif option == "1":
                    self.previous_page()

                elif option == "2":
                    self.next_page()

                elif option == "3":
                    level = "ITEM"
                    page_item_number = self.select_item()
                    self.item_number = (
                        (self.page_number - 1) * self.page_size
                    ) + page_item_number

                    if self.item_number == 0:
                        level = "PAGE"

            elif level == "ITEM":
                if option == "0":
                    level = "PAGE"

                elif option == "1":
                    self.previous_item()

                elif option == "2":
                    self.next_item()

        return
