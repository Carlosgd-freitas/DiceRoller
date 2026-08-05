"""Edit Team Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.life_state import LifeState
from src.base.monster import Monster
from src.base.team import Team
from src.gamemodes.sandbox.edit_monster_menu import EditMonsterMenu
from src.locales.languages import Language
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings

EXTENSION = ".team.dat"


class EditTeamMenu(EditMenu):
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
    # Utility
    # =========================================================================

    def change_language(self, language: Language, _messages: Dict = None):
        """
        Changes the Manager language.

        :var language: A Language.
        :vartype language: Language

        :var _messages: Messages loaded from a locale module.
        :vartype _messages: Dict
        """
        self.logger.change_language(language, _messages)
        _messages = self.logger._messages

        self.title = self.get_title()
        self.options = self.get_options()

        self.edit_monster_menu.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled

        self.edit_monster_menu.toggle_logging(enabled)

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

        elif option.id == "EDIT_MONSTER":
            self.edit_monster()

        elif option.id == "ADD_MONSTER":
            self.add_monster()

        elif option.id == "REMOVE_MONSTER":
            self.remove_monster()

        elif option.id == "IMPORT_TEAM":
            self.import_object("team", EXTENSION)

        elif option.id == "EXPORT_TEAM":
            self.export_object("team", EXTENSION)

        elif option.id == "RANDOMIZE_TEAM":
            randomized_team = self.randomizer.get_random_team()
            self.editing = randomized_team

        elif option.id == "RETURN":
            pass

        return

    def _select_monster(self) -> Option:
        """
        Shows the monsters of the Team being edited and prompts the user to select one of
        them, returning the corresponding option.

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
        self.show_options(
            options,
            validate=False,
        )

        # Selecting option
        selected_option = self.select_attribute_option(options, "monster")

        return selected_option

    def edit_monster(self):
        """
        Edits a Monster of the Team being edited.
        """
        selected_option = self._select_monster()

        if selected_option.id != "CANCEL":
            selected_monster: Monster = selected_option.obj
            index = self.editing.members.index(selected_monster)

            edited_monster: Monster = self.edit_monster_menu.open(selected_monster)

            self.editing.members[index] = edited_monster

        return

    def add_monster(self):
        """
        Adds a new Monster to the Team being edited, and opens the Edit Monster
        Menu with it.
        """
        name = self.randomizer.get_random_monster_name()
        new_monster = Monster(name=name)

        new_monster = self.edit_monster_menu.open(new_monster)
        self.editing.members.append(new_monster)

        return

    def remove_monster(self):
        """
        Removes a Monster from the Team being edited.
        """
        selected_option = self._select_monster()

        if selected_option.id != "CANCEL":
            selected_monster: Monster = selected_option.obj
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
        self.logger.log(message="")
