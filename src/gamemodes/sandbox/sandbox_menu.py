"""Sandbox Menu module."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Dict, List

from src.base.color import color_string
from src.base.life_state import LifeState
from src.base.team import Team
from src.combat.manager import CombatData, CombatManager
from src.combat.order_strategy import OrderStrategy
from src.compendium.effects import get_all_effects
from src.compendium.monsters import get_all_monsters
from src.gamemodes.sandbox.edit_team_menu import EditTeamMenu
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.menus.edit_menu import EditMenu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.systems.randomizer import Randomizer
    from src.systems.settings import Settings

EXTENSION = ".combat.dat"


class SandboxMenu(EditMenu):
    """
    Sandbox Menu class.

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
        super().__init__(
            settings,
            message_group="SANDBOX",
            logging=logging,
            randomizer=randomizer,
        )
        self.editing: CombatData = None

        self.edit_team_menu = EditTeamMenu(
            settings,
            logging=logging,
            randomizer=randomizer,
        )

        self.logger: CombatLogger

        # Attributes
        self.all_effects = get_all_effects()
        self.all_monsters = get_all_monsters()

        # Managers
        self.combat_manager = CombatManager(settings)

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.
        """
        options = [
            Option(
                id="START_COMBAT",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="start_combat",
                ),
                isolate_after=True,
            ),
            Option(
                id="CHANGE_COMBAT_ORDER",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="change_combat_order",
                ),
            ),
            Option(
                id="EDIT_TEAM",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_team",
                ),
            ),
            Option(
                id="ADD_TEAM",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="add_team",
                ),
            ),
            Option(
                id="REMOVE_TEAM",
                key="5",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="remove_team",
                ),
                isolate_after=True,
            ),
            Option(
                id="IMPORT_COMBAT",
                key="I",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="import_combat",
                ),
            ),
            Option(
                id="EXPORT_COMBAT",
                key="E",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="export_combat",
                ),
            ),
            Option(
                id="RANDOMIZE_COMBAT",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="randomize_combat",
                ),
                isolate_after=True,
            ),
            Option(
                id="EXIT",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="exit",
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

        self.combat_manager.logger.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled
        self.combat_manager.toggle_logging(enabled)

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id in ["EDIT_TEAM", "REMOVE_TEAM"]:
            return len(self.editing["teams"]) > 0

        return True

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "START_COMBAT":
            self.start_combat()

        elif option.id == "CHANGE_COMBAT_ORDER":
            self.change_combat_order()

        elif option.id == "EDIT_TEAM":
            self.edit_team()

        elif option.id == "ADD_TEAM":
            self.add_team()

        elif option.id == "REMOVE_TEAM":
            self.remove_team()

        elif option.id == "IMPORT_COMBAT":
            self.import_object("combat", EXTENSION)

        elif option.id == "EXPORT_COMBAT":
            self.export_object("combat", EXTENSION)

        elif option.id == "RANDOMIZE_COMBAT":
            randomized_combat = self.randomizer.get_random_combat()
            self.editing = randomized_combat

        elif option.id == "EXIT":
            pass

        return

    def change_combat_order(self):
        """
        Changes the order strategy of the Combat being edited.
        """
        # Defining options
        options = []
        selected_option = None

        for index, order_strategy in enumerate(OrderStrategy):
            message = self.logger.get_message(
                namespace="combat",
                message_group="ORDER",
                key=order_strategy.value.lower(),
            )

            option = Option(
                id=f"ORDER_STRATEGY_{index + 1}",
                key=str(index + 1),
                message=message,
                obj=order_strategy,
            )
            options.append(option)

            if order_strategy == self.editing["order_strategy"]:
                selected_option = option

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
        self.logger.log(message="")
        self.show_options(options, validate=False, selected_option=selected_option)

        # Selecting an option
        message = self.logger.get_message(
            namespace="menus",
            message_group="SANDBOX",
            key="select_combat_order_prompt",
        )

        selected_option = self.select(options, message, validate=False)

        if selected_option.id != "CANCEL":
            self.editing["order_strategy"] = selected_option.obj

        return

    def _select_team(self) -> Option:
        """
        Shows the teams of the combat being edited and prompts the user to select one of
        them, returning the corresponding option.

        :return: Option selected by the user.
        :rtype: Option
        """
        options = []

        # Defining options
        self.logger.log(message="")

        for index, team in enumerate(self.editing["teams"]):
            option = Option(
                id=f"TEAM_{index + 1}",
                key=str(index + 1),
                message=team.name,
                obj=team,
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
        selected_option = self.select_attribute_option(options, "team")

        return selected_option

    def edit_team(self):
        """
        Edits a Team of the Combat being edited.
        """
        selected_option = self._select_team()

        if selected_option.id != "CANCEL":
            selected_team: Team = selected_option.obj
            index = self.editing["teams"].index(selected_team)

            edited_team: Team = self.edit_team_menu.open(selected_team)

            self.editing["teams"][index] = edited_team

        return

    def add_team(self):
        """
        Adds a new Team to the Combat being edited, and opens the Edit Team
        Menu with it.
        """
        name = self.randomizer.get_random_team_name()
        new_team = Team(name=name)

        new_team = self.edit_team_menu.open(new_team)
        self.editing["teams"].append(new_team)

        return

    def remove_team(self):
        """
        Removes a Team of the Combat being edited.
        """
        selected_option = self._select_team()

        if selected_option.id != "CANCEL":
            selected_team: Team = selected_option.obj
            self.editing["teams"].remove(selected_team)

        return

    def start_combat(self):
        """
        Starts a combat between the current set teams.
        """
        original_combat_data = deepcopy(self.editing)
        self.combat_manager.set_combat_data(self.editing)

        self.combat_manager.run()
        self.combat_manager.set_combat_data(original_combat_data)
        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_editing_details(self):
        """
        Shows the details of the object being edited.
        """
        # Order Strategy
        message = (
            self.logger.get_message(
                namespace="combat",
                message_group="ORDER",
                key="order",
            )
            + ": "
        )
        message = color_string(message, intensity="BRIGHT")

        message += (
            self.logger.get_message(
                namespace="combat",
                message_group="ORDER",
                key=self.editing["order_strategy"].value.lower(),
            )
            + "\n"
        )

        self.logger.log(message=message)

        # Teams
        self.logger.log_teams(
            self.editing["teams"],
            life_state=LifeState.ANY,
            control_type=True,
        )
