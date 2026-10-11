"""Effect Compendium module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from src.base.color import Color, ColorData, color_string
from src.base.text import normalize
from src.compendium.compendium import Compendium, CompendiumMessages
from src.factories.effect import EffectFactory
from src.logger.effects import EffectLogger
from src.menus.option import Option

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.systems.settings import Settings


class EffectCompendium(Compendium):
    """
    Effect Compendium class.

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
        items = EffectFactory.get_all_objects()

        logger = EffectLogger(enabled=logging, language=settings.language)

        super().__init__(
            logger=logger,
            settings=settings,
            items=items,
            alignments=("right", "left", "left"),
        )

        self.logger: EffectLogger

    def get_title(self) -> str:
        """
        Returns the Compendium title.

        :return: Compendium title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="compendium", message_group="EFFECTS", key="title"
        )

    def get_columns(self) -> List[str]:
        """
        Returns the Compendium columns.

        :return: List of Compendium columns.
        :rtype: List[str]
        """
        columns = ["#"]

        columns.append(
            self.logger.get_message(
                namespace="base",
                message_group="LEXICON",
                key="name",
            )
        )

        columns.append(
            self.logger.get_message(
                namespace="base",
                message_group="LEXICON",
                key="type",
            )
        )

        columns = [column.title() for column in columns]

        return columns

    def get_item_options(self) -> List[Option]:
        """
        Returns the options that will be used in the Compendium at ITEM level.

        :return: List of options that can be selected at ITEM level.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="PREVIOUS_ITEM",
                key="1",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="EFFECTS",
                    key="previous_item",
                ),
            ),
            Option(
                id="NEXT_ITEM",
                key="2",
                message=self.logger.get_message(
                    namespace="compendium",
                    message_group="EFFECTS",
                    key="next_item",
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
                id="RETURN",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="return",
                ),
                isolate_before=True,
                isolate_after=True,
            ),
        ]

        return options

    def get_messages(self) -> CompendiumMessages:
        """
        Returns messages that will be used by the Compendium.

        :return: Messages that will be used by the Compendium.
        :rtype: CompendiumMessages
        """
        messages = {}

        for key in [
            "item_not_found",
            "search_prompt",
            "select_item_prompt",
        ]:
            messages[key] = self.logger.get_message(
                namespace="compendium",
                message_group="EFFECTS",
                key=key,
            )

        return messages

    # =========================================================================
    # Data access
    # =========================================================================

    def get_pages_data(
        self,
        items: List[Effect],
        selected_item: Effect = None,
        selected_color_data: ColorData = None,
    ) -> List[List]:
        """
        Returns all the tabulated data that will be used on the Compendium.

        :param items: Compendium items.
        :type items: List[Effect]

        :param selected_item: Currently selected item. Default value is None.
        :type selected_item: Effect

        :param selected_color_data: Data for coloring currently selected option.
        Default value is green foreground and bright intensity.
        :type selected_color_data: ColorData

        :return: Compendium items structured as tabulated data.
        :rtype: List[List]
        """
        # Coloring default values
        if selected_color_data is None:
            selected_color_data = {
                "foreground_color": Color.GREEN,
                "intensity": "BRIGHT",
            }

        pages_data = []

        for idx, item in enumerate(items):
            effect_keyword = self.logger.get_colored_message(
                keyword=item.keyword,
                message=self.get_item_name(item),
            )

            effect_type = self.logger.get_message(
                namespace="effect_types", message_group=item.type.name, key="name"
            )

            row_data = [
                f"[{idx+1}]",
                effect_keyword,
                effect_type,
            ]

            if selected_item is not None and item.keyword == selected_item.keyword:
                row_data = [
                    color_string(cell, **selected_color_data) for cell in row_data
                ]

            pages_data.append(row_data)

        return pages_data

    def get_item_name(self, item: Effect) -> str:
        """
        Returns the name of an item.

        :param item: A Compendium item.
        :type item: Effect

        :return: The Compendium item name.
        :rtype: str
        """
        return self.logger.get_effect_name(item)

    # =========================================================================
    # Options
    # =========================================================================

    def get_sort_key(self, column_index: int) -> Callable:
        """
        Returns a key (lambda function) to be used in the sort option.

        :param column_index: Index of the column used to sort the Compendium items.
        :type column_index: int

        :return: Key (lambda function) to sort the Compendium items.
        :rtype: Callable
        """
        if column_index == 1:
            return lambda x: normalize(self.get_item_name(x))

        elif column_index == 2:
            return lambda x: self.logger.get_message(
                namespace="effect_types",
                message_group=x.type.name,
                key="name",
            )

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_item(self):
        """
        Shows the current item.
        """
        item: Effect = self.items[self.item_number - 1]
        item_name = self.get_item_name(item)

        message = self.title + ": " + item_name

        self.logger.box_message(
            message=message,
            size=50,
        )

        # Keyword
        message = self.logger.get_colored_message(
            keyword=item.keyword,
            message=item_name,
        )
        self.logger.log(message=message + "\n")

        # Type
        message = (
            self.logger.get_message(
                namespace="base",
                message_group="LEXICON",
                key="type",
            ).upper()
            + ":"
        )
        message = color_string(message, intensity="BRIGHT")

        message += " " + self.logger.get_message(
            namespace="effect_types",
            message_group=item.type.name,
            key="name",
        )

        self.logger.log(message=message + "\n")

        # Description
        self.logger.log_effect_description(
            effect=item,
            variation="static",
        )
        self.logger.log(message="")
