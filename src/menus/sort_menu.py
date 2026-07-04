"""Sort Menu module."""

from __future__ import annotations

from typing import Callable, List, TypedDict

from src.base.color import Color, color_string
from src.base.text import unaccent
from src.logger.logger import Logger
from src.menus.menu import Menu
from src.menus.option import Option
from src.systems.settings import Settings


class SortData(TypedDict):
    """
    Sort Data.

    :var column_index: Index of the column used to sort the items.
    :vartype column_index: int

    :var items: Sortable tabular items.
    :vartype items: List

    :var reverse: If the items are sorted reversely.
    :vartype reverse: bool
    """

    column_index: int
    items: List
    reverse: bool


class SortMenu(Menu):
    """
    SortMenu class.

    :var title: Menu title.
    :vartype title: str

    :var columns: Identifiers that can sort the items.
    :vartype columns: List[str]

    :var items: Items to be sorted.
    :vartype items: List

    :param column_index: Current index of the column used to sort the items.
    :type column_index: int

    :var reverse: If the items are currently being sorted in reverse.
    :vartype reverse: bool

    :var get_sort_key: Function that returns a key (lambda function) based on a column
    to be used in sorting.
    :vartype get_sort_key: Callable

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
        title: str,
        columns: List[str],
        items: List,
        column_index: int,
        reverse: bool,
        get_sort_key: Callable,
        settings: Settings,
        logging: bool = True,
    ):
        # Initialization
        self.title = title
        self.columns = columns
        self.items = items

        self.column_index = column_index
        self.reverse = reverse
        self.get_sort_key = get_sort_key

        logger = Logger(enabled=logging, language=settings.language)

        super().__init__(
            logger,
            settings,
        )

    def get_title(self) -> str:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        return self.title

    def get_options(self) -> List[Option]:
        """
        Returns the Menu options.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = []
        index = 1

        for column in self.columns:
            if column == "#":
                continue

            option = Option(
                id=unaccent(column).upper(),
                key=str(index),
                message=column,
            )

            options.append(option)

            index += 1

        options.append(
            Option(
                id="ORDER",
                key=str(len(options) + 1),
                message=self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="order",
                ).upper(),
                isolate_before=True,
            )
        )

        options.append(
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
            )
        )

        return options

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.

        :param option: Menu option.
        :type option: Option

        :return: If the option can be selected.
        :rtype: bool
        """
        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param option: Menu option.
        :type option: Option
        """
        if option.id == "ORDER":
            self.reverse = not self.reverse
            self.sort(self.column_index, self.reverse)

        elif option.id == "EXIT":
            pass

        else:
            self.column_index = int(option.key)
            self.sort(self.column_index, self.reverse)

        return

    def sort(self, column_index: int, reverse: bool) -> List:
        """
        Sorts the Menu items.

        :param column_index: Index of the column used to sort the items.
        :type column_index: int

        :param reverse: If the items will be sorted normally or reversely.
        :type reverse: bool

        :return: Sorted menu items
        :rtype: List
        """
        key = self.get_sort_key(column_index)

        if key is None:
            raise ValueError("sort key was not defined")

        self.items.sort(key=key, reverse=reverse)
        return self.items

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_options(self):
        """
        Shows the Menu options.
        """
        message = color_string(
            self.logger.get_message(
                namespace="base", message_group="LEXICON", key="columns"
            ).title()
            + ":",
            intensity="BRIGHT",
        )

        self.logger.log(message=message)

        for option in self.options:
            message = ""

            if option.isolate_before:
                message += "\n"

            message += f"[{option.key}] {option.message}"

            # Order option
            if option.id == "ORDER":
                message += ": "

                if not self.reverse:
                    message += color_string(
                        self.logger.get_message(
                            namespace="base",
                            message_group="LEXICON",
                            key="normal",
                        ).upper(),
                        intensity="BRIGHT",
                    )

                else:
                    message += color_string(
                        self.logger.get_message(
                            namespace="menus",
                            message_group="SORT",
                            key="reverse",
                        ).upper(),
                        intensity="BRIGHT",
                    )

            # Column options
            elif int(option.key) == self.column_index:
                message = color_string(
                    message,
                    foreground_color=Color.GREEN,
                    intensity="BRIGHT",
                )

            if option.isolate_after:
                message += "\n"

            self.logger.log(message=message)

        return

    def open(self) -> SortData:
        """
        Opens the Menu.

        :return: Sort Data.
        :rtype: SortData
        """
        while True:
            self.show_title()
            self.show_options()
            selected = self.select_option()

            if self.is_option_valid(selected):
                self.process_option(selected)

            if selected.id in ["EXIT", "RETURN"]:
                break

        return {
            "column_index": self.column_index,
            "items": self.items,
            "reverse": self.reverse,
        }
