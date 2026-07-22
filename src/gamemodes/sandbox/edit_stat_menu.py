"""Edit Stat Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar

from src.base.life_state import LifeState
from src.base.monster import Monster
from src.base.team import Team
from src.gamemodes.sandbox.edit_monster_menu import EditMonsterMenu
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings

T = TypeVar("T")


class EditStatMenu(EditMenu):
    """
    Edit Team Menu class.

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
            message_group="EDIT_TEAM",
            logging=logging,
            randomizer=randomizer,
        )
        self.editing: Team = None

        self.edit_monster_menu = EditMonsterMenu(
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
                id="EDIT_NAME",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_name",
                ),
            ),
            Option(
                id="EDIT_MONSTER",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_monster",
                ),
            ),
            Option(
                id="ADD_MONSTER",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="add_monster",
                ),
            ),
            Option(
                id="REMOVE_MONSTER",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="remove_monster",
                ),
                isolate_after=True,
            ),
            Option(
                id="IMPORT_TEAM",
                key="I",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="import_team",
                ),
                isolate_before=True,
            ),
            Option(
                id="EXPORT_TEAM",
                key="X",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="export_team",
                ),
            ),
            Option(
                id="RANDOMIZE_TEAM",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="randomize_team",
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
        if option.id in ["EDIT_MONSTER", "REMOVE_MONSTER"]:
            return len(self.editing.members) > 0

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param side: Side to be edited.
        :type side: Side
        """
        if option.id == "EDIT_NAME":
            self.edit_attribute("name", str)

        if option.id == "EDIT_MONSTER":
            self.edit_monster()

        elif option.id == "ADD_MONSTER":
            self.add_monster()

        elif option.id == "REMOVE_MONSTER":
            self.remove_monster()

        elif option.id == "RANDOMIZE_TEAM":
            randomized_team = self.randomizer.get_random_team()
            self.editing = randomized_team

        elif option.id == "RETURN":
            pass

        return

    def _select_monster(self) -> Option:
        """
        Shows the monsters of the team being edited and prompts the user to select one of
        them, returning the option that corresponds to them.

        :return: Option selected by the user.
        :rtype: Option
        """
        options = []

        # Defining options
        self.logger.log(message="")

        for index, member in enumerate(self.editing.members):
            option = Option(
                id=f"MONSTER_{index + 1}",
                key=str(index + 1),
                message=self.logger.get_monster_name(member),
                obj=member,
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
        selected_option = self.select_attribute_option(options, "monster")

        return selected_option

    def edit_monster(self):
        """
        Edits a Monster of the Team being edited.
        """
        selected_option = self._select_monster()

        if selected_option.id != "CANCEL":
            selected_monster = selected_option.obj
            selected_monster = self.edit_monster_menu.open(selected_monster)

        return

    def add_monster(self):
        """
        Adds a new Monster to the Team being edited, and opens the Edit Monster
        Menu with it.
        """
        new_monster = Monster()
        new_monster = self.edit_monster_menu.open(new_monster)
        self.editing.members.append(new_monster)

        return

    def remove_monster(self):
        """
        Removes a Monster from the Team being edited.
        """
        selected_option = self._select_monster()

        if selected_option.id != "CANCEL":
            selected_monster = selected_option.obj
            self.editing.members.remove(selected_monster)

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_editing_details(self):
        """
        Shows the details of the object being edited.
        """
        self.logger.log_team(
            self.editing,
            life_state=LifeState.ANY,
            control_type=True,
        )
