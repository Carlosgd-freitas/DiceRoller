"""Select Difficulty Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.color import color_string
from src.base.data import (
    next_value,
    previous_value,
)
from src.base.difficulties import Difficulty, get_difficulty_color
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.systems.settings import Settings


class SelectDifficultyMenu(Menu):
    """
    Select Difficulty Menu class.

    :var settings: Game settings.
    :vartype settings: Settings

    :param message_group: Message group that contains the Menu messages.
    :type message_group: str

    :var logging: If logging is enabled. Default value is True.
    :vartype logging: bool

    :var randomizer: Randomizer for randomizing options.
    :vartype randomizer: Randomizer
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        settings: Settings,
        logging: bool = True,
    ):
        # Initialization
        logger = CombatLogger(enabled=logging, language=settings.language)

        super().__init__(
            logger,
            settings,
        )

        self.logger: CombatLogger

        self.difficulty = settings.last_difficulty
        self.showing_difficulty: Difficulty = None

        self.submenu_options = self.get_submenu_options()

    def get_title(self) -> str:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="menus", message_group="SELECT_DIFFICULTY", key="title"
        )

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = []

        for index, difficulty in enumerate(list(Difficulty), start=1):
            message = self.logger.get_message(
                namespace="difficulties",
                message_group=difficulty.name,
                key="name",
            )

            color_data = get_difficulty_color(difficulty)

            options.append(
                Option(
                    id=f"DIFFICULTY_{index}",
                    key=str(index),
                    message=color_string(
                        message,
                        **color_data,
                    ),
                    obj=difficulty,
                )
            )

        options.append(
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
            )
        )

        return options

    def get_submenu_options(self) -> List[Option]:
        """
        Returns the options that will be used by the sub menu.
        """
        options = [
            Option(
                id="PREVIOUS",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="previous",
                ),
            ),
            Option(
                id="NEXT",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="next",
                ),
            ),
            Option(
                id="SELECT",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="select",
                ),
                isolate_after=True,
            ),
            Option(
                id="RETURN",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="return",
                ),
                isolate_after=True,
            ),
        ]

        return options

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
        self.submenu_options = self.get_submenu_options()

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if (option.id == "PREVIOUS") and (self.showing_difficulty == Difficulty.EASY):
            return False

        elif (option.id == "NEXT") and (
            self.showing_difficulty == Difficulty.NIGHTMARE
        ):
            return False

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param side: Side to be edited.
        :type side: Side
        """
        if "DIFFICULTY" in option.id:
            self.showing_difficulty = option.obj
            self.show_difficulty(self.showing_difficulty)

            # Showing submenu options
            self.show_options(self.submenu_options)

            # Selecting option
            message = self.logger.get_message(
                namespace="menus",
                message_group="BASE",
                key="select_option_prompt",
            )

            selected_option = self.select(self.submenu_options, message)
            if selected_option:
                self.process_option(selected_option)

        elif option.id == "PREVIOUS":
            difficulty = previous_value(list(Difficulty), self.showing_difficulty)

            for option in self.options:
                if option.obj == difficulty:
                    break

            self.process_option(option)

        elif option.id == "NEXT":
            difficulty = next_value(list(Difficulty), self.showing_difficulty)

            for option in self.options:
                if option.obj == difficulty:
                    break

            self.process_option(option)

        elif option.id == "SELECT":
            self.difficulty = self.showing_difficulty

        elif option.id == "RETURN":
            pass

        return

    def show_difficulty(self, difficulty: Difficulty, **kwargs):
        """
        Shows the difficulty details.
        """
        # Updating logging params
        kwargs.update(self.logger._get_attribute_params())
        kwargs.update(self.logger._get_keyword_params())

        # Difficulty name
        self.logger.log(message="")

        message = self.logger.get_message(
            namespace="difficulties",
            message_group=difficulty.name,
            key="name",
        )

        color_data = get_difficulty_color(difficulty)

        self.logger.log(message=color_string(message, **color_data) + "\n")

        # Difficulty modifiers
        modifiers = [
            "after_battles",
            "after_boss_battles",
            "enemy_attribute_scaling",
            "enemy_dice_items",
            "enemy_skills",
            "enemy_ai",
            "shop_pricing",
        ]

        for modifier in modifiers:
            self.logger.log(
                message="● ",
                end="",
            )

            message = color_string(
                self.logger.get_message(
                    namespace="difficulties",
                    message_group="MODIFIERS",
                    key=modifier,
                )
                + ": ",
                intensity="BRIGHT",
            )

            self.logger.log(
                message=message,
                end="",
            )

            self.logger.log(
                namespace="difficulties",
                message_group=difficulty.name,
                key=modifier,
                **kwargs,
            )

        self.logger.log(message="")

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def open(self):
        """
        Opens the Menu.
        """
        while True:
            self.show_title()

            # Logging selected difficulty
            message = color_string(
                self.logger.get_message(
                    namespace="menus",
                    message_group="SELECT_DIFFICULTY",
                    key="selected_difficulty",
                )
                + ": ",
                intensity="BRIGHT",
            )

            self.logger.log(
                message=message,
                end="",
            )

            message = self.logger.get_message(
                namespace="difficulties",
                message_group=self.difficulty.name,
                key="name",
            )

            color_data = get_difficulty_color(self.difficulty)

            self.logger.log(message=color_string(message, **color_data))

            self.logger.log(message="")

            # Logging options
            self.show_options(self.options)

            message = self.logger.get_message(
                namespace="menus",
                message_group="SELECT_DIFFICULTY",
                key="select_difficulty_prompt",
            )
            selected = self.select(self.options, message)
            self.process_option(selected)

            if selected.id in ["EXIT", "RETURN"]:
                break

            else:
                self.logger.log(message="")

        return
