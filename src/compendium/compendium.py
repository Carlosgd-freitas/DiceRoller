"""Compendium module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from math import ceil
from typing import TYPE_CHECKING, Any, List, Literal, Tuple, TypedDict

from tabulate import tabulate

from src.base.color import Color, color_string

if TYPE_CHECKING:
    from src.logger.logger import Logger


class CompenidumOptionsMessages(TypedDict):
    """."""

    exit: str
    next_item: str
    next_page: str
    previous_item: str
    previous_page: str
    return_to_pages: str
    show_item_details: str


class Compenidum(ABC):
    """
    Compenidum class.
    """

    def __init__(
        self,
        logger: Logger,
        items: List[Any],
        page_headers: List[str],
        page_colalign: Tuple[str] = None,
        page_number: int = 1,
        page_size: int = 15,
    ):
        # Compenidum Attributes
        self.items = items
        self.logger = logger
        self.options_messages = self.get_options_messages()

        self.page_number = page_number
        self.page_size = page_size
        self.num_pages = ceil(len(self.items) / self.page_size)

        self.item_number = 1

        # Page Attributes
        self.page_headers = page_headers

        if page_colalign is None:
            page_colalign = tuple(["left" for _ in self.page_headers])

        self.page_colalign = page_colalign

    def get_page_items(self):
        """."""
        return self.items[
            ((self.page_number - 1) * self.page_size) : (
                self.page_number * self.page_size
            )
        ]

    @abstractmethod
    def get_page_data(self, page_items: List[Any]) -> List[List[Any]]:
        """."""
        raise NotImplementedError

    @abstractmethod
    def get_options_messages(self) -> CompenidumOptionsMessages:
        """."""
        raise NotImplementedError

    def get_options(self, level: Literal["ITEM", "PAGE"]):
        """."""
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
        """."""
        self.logger.log(message="\n╔══════════════════════════════════╗")
        self.logger.log(
            message=f"║ Effect Compendium: Page {self.page_number:<3}      ║"
        )
        self.logger.log(
            message=f"║ Compêndio de Efeitos: Página {self.page_number:<3} ║"
        )
        self.logger.log(message="╚══════════════════════════════════╝\n")

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
        """."""
        raise NotImplementedError

    def next_page(self):
        """."""
        if self.page_number < self.num_pages:
            self.page_number += 1

    def previous_page(self):
        """."""
        if self.page_number > 1:
            self.page_number -= 1

    def next_item(self):
        """."""
        if self.item_number < len(self.items):
            self.item_number += 1
            self.page_number = ceil(self.item_number / self.page_size)

    def previous_item(self):
        """."""
        if self.item_number > 1:
            self.item_number -= 1
            self.page_number = ceil(self.item_number / self.page_size)

    def get_page_item(self) -> int:
        """."""
        page_items = self.get_page_items()

        while True:
            page_item_number = self.logger.input(
                message="> Input effect number (or 0 to return): "
            )

            try:
                page_item_number = int(page_item_number)
                if page_item_number in range(0, len(page_items) + 1):
                    break

            except Exception:
                continue

        return page_item_number

    def open(self):
        """."""
        level = "PAGE"

        while True:
            # Showing content
            if level == "PAGE":
                self.show_page()
            elif level == "ITEM":
                self.show_item()

            self.get_options(level=level)

            # Player option input
            option = self.logger.input(message="> Input your option: ")

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
                    page_item_number = self.get_page_item()
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
