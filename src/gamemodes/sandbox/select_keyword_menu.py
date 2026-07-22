"""Select Keyword Menu module."""

# arquivo necessário ou transformar num método do Edit Effect Menu?

from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar

from src.base.color import Color, color_string
from src.base.dice import Dice
from src.base.side import Side
from src.gamemodes.sandbox.edit_side_menu import EditSideMenu
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings

T = TypeVar("T")


class SelectKeywordMenu(Menu):
    """
    Select Keyword Menu class.

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
        randomizer: Randomizer = None,
    ):
        # Initialization
        logger = CombatLogger(enabled=logging, language=settings.language)

        super().__init__(
            logger,
            settings,
        )

        self.logger: CombatLogger

        self.randomizer = randomizer or Randomizer()
        self.dice: Dice = None

    def get_title(self) -> str:
        """
        Returns the Menu's title.

        :return: Menu title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="menus", message_group="EDIT_KEYWORD", key="title"
        )

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="EDIT_SIDE",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="EDIT_DICE",
                    key="edit_side",
                ),
            ),
            Option(
                id="ADD_SIDE",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="EDIT_DICE",
                    key="add_side",
                ),
            ),
            Option(
                id="REMOVE_SIDE",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="EDIT_DICE",
                    key="remove_side",
                ),
                isolate_after=True,
            ),
            Option(
                id="RANDOMIZE_KEYWORD",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="EDIT_DICE",
                    key="randomize_dice",
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

    def _sides_as_options(self) -> List[Option]:
        """
        Returns the sides of the Dice being edited as Options.

        :return: Dice sides as options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="CANCEL",
                key="0",
                message=None,
            )
        ]

        options.extend(
            [
                Option(
                    id=f"SIDE_{idx+1}",
                    key=str(idx + 1),
                    message=self.logger.get_side_effects_message(side),
                    obj=side,
                )
                for idx, side in enumerate(self.dice.sides)
            ]
        )

        return options

    def _select_side(self) -> Side | None:
        """
        Prompts the user to select a side of the Dice being edited. If an invalid
        key is selected, the prompt will repeat.

        :return: Side selected by the user.
        :rtype: Side | None
        """
        options = self._sides_as_options()

        message = self.logger.get_message(
            namespace="menus",
            message_group="EDIT_SIDE",
            key="select_side_prompt",
        )

        selected_option: Option = self.select(options, message)

        return selected_option.obj

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id in ["EDIT_SIDE", "REMOVE_SIDE"]:
            return len(self.dice.sides) > 0

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param side: Side to be edited.
        :type side: Side
        """
        if option.id == "EDIT_SIDE":
            self.edit_side()

        elif option.id == "ADD_SIDE":
            self.add_side()

        elif option.id == "REMOVE_SIDE":
            self.remove_side()

        elif option.id == "RANDOMIZE_DICE":
            randomized_dice = self.randomizer.get_random_dice()
            self.dice = randomized_dice

        elif option.id == "RETURN":
            pass

        return

    def edit_side(self):
        """
        Edits a Side of the Dice being edited.
        """
        selected_side = self._select_side()

        if selected_side is not None:
            edit_side_menu = EditSideMenu(
                self.settings,
                self.logger.enabled,
                randomizer=self.randomizer,
            )

            edit_side_menu.open(selected_side)

        return

    def add_side(self):
        """
        Adds a new Side to the Dice being edited, and opens the Edit Side
        Menu with it.
        """
        new_side = Side(effects=[])

        edit_side_menu = EditSideMenu(
            self.settings,
            self.logger.enabled,
            randomizer=self.randomizer,
        )

        edit_side_menu.open(new_side)

        return

    def remove_side(self):
        """
        Removes a Side from the Dice being edited.
        """
        selected_side = self._select_side()

        if selected_side is not None:
            self.dice.sides.remove(selected_side)

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_options(self):
        """
        Shows the Menu's options.
        """
        self.logger.log_dice_details(self.dice)
        self.logger.log(message="")

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

    def open(self, dice: Dice):
        """
        Opens the Menu.

        :param dice: Dice to be edited.
        :type dice: Dice
        """
        self.dice = dice

        while True:
            self.show_title()
            self.show_options()

            message = self.logger.get_message(
                namespace="menus",
                message_group="BASE",
                key="select_option_prompt",
            )
            selected = self.select(self.options, message)

            if self.is_option_valid(selected):
                self.process_option(selected)

            if selected.id in ["EXIT", "RETURN"]:
                break

            else:
                self.logger.log(message="")

        return
