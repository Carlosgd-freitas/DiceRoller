"""Edit Dice Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.dice import Dice
from src.base.side import Side
from src.gamemodes.sandbox.edit_side_menu import EditSideMenu
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings


class EditDiceMenu(EditMenu):
    """
    Edit Dice Menu class.

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
        randomizer: Randomizer = None,
    ):
        super().__init__(
            settings,
            message_group="EDIT_DICE",
            logging=logging,
            randomizer=randomizer,
        )
        self.editing: Dice = None

        self.edit_side_menu = EditSideMenu(
            settings,
            logging=logging,
            randomizer=randomizer,
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
                    message_group=self.message_group,
                    key="edit_side",
                ),
            ),
            Option(
                id="ADD_SIDE",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="add_side",
                ),
            ),
            Option(
                id="REMOVE_SIDE",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="remove_side",
                ),
                isolate_after=True,
            ),
            Option(
                id="RANDOMIZE_DICE",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
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

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id in ["EDIT_SIDE", "REMOVE_SIDE"]:
            return len(self.editing.sides) > 0

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
            self.editing = randomized_dice

        elif option.id == "RETURN":
            pass

        return

    def _select_side(self) -> Option:
        """
        Shows the sides of the dice being edited and prompts the user to select one of
        them, returning the option that corresponds to them.

        :return: Option selected by the user.
        :rtype: Option
        """
        options = []

        # Defining options
        self.logger.log(message="")

        for index, side in enumerate(self.editing.sides):
            option = Option(
                id=f"SIDE_{index + 1}",
                key=str(index + 1),
                message=self.logger.get_side_effects_message(side),
                obj=side,
            )
            options.append(option)

        options.append(
            Option(
                id="CANCEL",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="cancel",
                ),
                isolate_before=True,
                isolate_after=True,
            )
        )

        # Showing options
        self.show_options(options, validate=True)

        # Selecting option
        selected_option = self.select_attribute_option(options, "side")

        return selected_option

    def edit_side(self):
        """
        Edits a Side of the Dice being edited.
        """
        selected_option = self._select_side()

        if selected_option.id != "CANCEL":
            selected_side = selected_option.obj
            selected_side = self.edit_side_menu.open(selected_side)

        return

    def add_side(self):
        """
        Adds a new Side to the Dice being edited, and opens the Edit Side
        Menu with it.
        """
        new_side = Side(effects=[])
        new_side = self.edit_side_menu.open(new_side)
        self.editing.sides.append(new_side)

        return

    def remove_side(self):
        """
        Removes a Side from the Dice being edited.
        """
        selected_option = self._select_side()

        if selected_option.id != "CANCEL":
            selected_side = selected_option.obj
            self.editing.sides.remove(selected_side)

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_editing_details(self):
        """
        Shows the details of the object being edited.
        """
        self.logger.log_dice_details(self.editing)
