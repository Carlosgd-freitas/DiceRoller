"""Sandbox Menu module."""

from __future__ import annotations

from copy import deepcopy
from random import choice
from typing import TYPE_CHECKING, Dict, List

from src.base.color import Color, color_string
from src.combat.manager import CombatData, CombatManager
from src.combat.team import Team
from src.compendium.effects import get_all_effects
from src.compendium.monsters import get_all_monsters
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.menus.option import Option
from src.systems.file import FileManager

if TYPE_CHECKING:
    from src.systems.settings import Settings


class SandboxMenu(Menu):
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
    ):
        # Initialization
        logger = CombatLogger(enabled=logging, language=settings.language)

        super().__init__(
            logger,
            settings,
        )

        self.logger: CombatLogger

        # Attributes
        self.all_effects = get_all_effects()
        self.all_monsters = get_all_monsters()

        # Managers
        self.file_manager = FileManager(settings)
        self.combat_manager = CombatManager(settings)

        combat_data = self.get_random_combat()
        self.combat_manager.set_combat_data(combat_data)

    def get_title(self) -> str:
        """
        Returns the Menu's title.
        """
        return self.logger.get_message(
            namespace="menus", message_group="SANDBOX", key="title"
        )

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
                    message_group="SANDBOX",
                    key="start_combat_message",
                ),
            ),
            Option(
                id="EDIT_COMBAT",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat_message",
                ),
            ),
            Option(
                id="IMPORT_COMBAT",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="import_combat_message",
                ),
            ),
            Option(
                id="EXPORT_COMBAT",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="export_combat_message",
                ),
            ),
            Option(
                id="RANDOMIZE_COMBAT",
                key="5",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="randomize_combat_message",
                ),
            ),
            Option(
                id="EXIT",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="exit_message",
                ),
                isolate_before=True,
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

        self.file_manager.change_language(language, _messages)
        self.combat_manager.logger.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled
        self.file_manager.toggle_logging(enabled)
        self.combat_manager.toggle_logging(enabled)

    # =========================================================================
    # Options
    # =========================================================================

    # Todo: Randomize Dice
    def get_random_combat(self, n_teams: int = 2, team_size: int = 3) -> CombatData:
        """
        Gets a random combat.

        :param n_teams: Number of teams.
        :type n_teams: int

        :param teams_size: Number of monsters in each team.
        :type teams_size: int
        """
        teams: List[Team] = []

        team_names = [
            "Alpha",
            "Beta",
            "Gamma",
            "Delta",
            "Kappa",
            "Omega",
            "Red",
            "Blue",
            "Green",
            "Yellow",
            "Purple",
            "Orange",
        ]

        for _ in range(n_teams):
            team_name = choice(team_names)
            team_names.remove(team_name)

            members = []
            for _ in range(team_size):
                members.append(deepcopy(choice(self.all_monsters)))

            message = self.logger.get_message(
                namespace="combat", message_group="COMBAT", key="team"
            )

            team = Team(name=f"{message} {team_name}", members=members)

            teams.append(team)

        return {
            "teams": teams,
        }

    def import_combat(self):
        """
        Imports combat from a file.
        """
        filename = self.file_manager.logger.input_filename()

        if self.file_manager.exists(filename):
            combat_data: CombatData = self.file_manager.load(filename)
            self.combat_manager.set_combat_data(combat_data)

        else:
            self.file_manager.logger.log_file_not_found(filename)
            self.logger.log("")

        return

    def export_combat(self):
        """
        Exports the current combat to a file.
        """
        filename = self.file_manager.logger.input_filename()
        combat_data = self.combat_manager.get_combat_data()
        self.file_manager.save(combat_data, filename)

        return

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id in ["EDIT_COMBAT"]:
            return False

        return True

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "START_COMBAT":
            self.start_combat()

        elif option.id == "EDIT_COMBAT":
            pass

        elif option.id == "IMPORT_COMBAT":
            self.import_combat()

        elif option.id == "EXPORT_COMBAT":
            self.export_combat()

        elif option.id == "RANDOMIZE_COMBAT":
            combat_data = self.get_random_combat()
            self.combat_manager.set_combat_data(combat_data)

        elif option.id == "EXIT":
            pass

        return

    def start_combat(self):
        """
        Starts a combat between the current set teams.
        """
        original_combat_data = deepcopy(self.combat_manager.get_combat_data())
        self.combat_manager.run()
        self.combat_manager.set_combat_data(original_combat_data)
        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_options(self):
        """
        Shows the Menu's options.
        """
        self.logger.log_teams(self.combat_manager.teams)
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
