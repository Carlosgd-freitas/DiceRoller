"""Edit Team Menu module."""

## TODO

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.color import Color, color_string
from src.base.life_state import LifeState
from src.base.team import Team
from src.combat.manager import CombatData, CombatManager
from src.compendium.effects import get_all_effects
from src.compendium.monsters import get_all_monsters
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.menus.option import Option
from src.systems.file import FileManager
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings

EXTENSION = ".team.dat"


class EditTeamMenu(Menu):
    """
    Edit Team Menu class.

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
        self.combat_manager = CombatManager(settings)
        combat_data = self.get_random_combat()
        self.combat_manager.set_combat_data(combat_data)

        self.file_manager = FileManager()
        self.randomizer = Randomizer()

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
                id="EDIT_NAME",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
                isolate_after=True,
            ),
            Option(
                id="EDIT_MONSTER",
                key="E",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="ADD_MONSTER",
                key="A",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="REMOVE_MONSTER",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
                isolate_after=True,
            ),
            Option(
                id="IMPORT_TEAM",
                key="I",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="import_combat",
                ),
                isolate_before=True,
            ),
            Option(
                id="EXPORT_TEAM",
                key="X",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="export_combat",
                ),
            ),
            Option(
                id="RANDOMIZE_TEAM",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="randomize_combat",
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

    def import_team(self):
        """
        Imports a Team from a file.
        """
        filename = self.file_manager.logger.input_filename(EXTENSION)

        if self.file_manager.exists(filename):
            combat_data: CombatData = self.file_manager.load_file(filename)
            self.combat_manager.set_combat_data(combat_data)

        else:
            self.file_manager.logger.log_file_not_found(filename)
            self.logger.log("")

        return

    def export_team(self):
        """
        Exports a Team to a file.
        """
        filename = self.file_manager.logger.input_filename(EXTENSION)
        combat_data = self.combat_manager.get_combat_data()
        self.file_manager.save_file(filename, combat_data)

        return

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        return True

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "EDIT_NAME":
            self.edit_name()

        elif option.id == "EDIT_MONSTER":
            self.edit_monster()

        elif option.id == "IMPORT_TEAM":
            self.import_team()

        elif option.id == "EXPORT_TEAM":
            self.export_team()

        elif option.id == "RANDOMIZE_TEAM":
            combat_data = self.get_random_combat()
            self.combat_manager.set_combat_data(combat_data)

        elif option.id == "EXIT":
            pass

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_options(self, options: List[Option]):
        """
        Shows options.

        :param options: Options to be showed.
        :type options: List[Option]
        """
        self.logger.log_team(self.team, life_state=LifeState.ANY, control_type=True)
        self.logger.log(message="")

        for option in options:
            message = ""

            if option.isolate_before:
                message += "\n"

            message += f"[{option.key}] {option.message}"

            if option.isolate_after:
                message += "\n"

            if not self.is_option_valid(option):
                message = color_string(message, foreground_color=Color.RED)

            self.logger.log(message=message)

        if not options[-1].isolate_after:
            self.logger.log(message="")

        return

    def open(self, team: Team):
        """
        Opens the Menu.

        :param team: Team to be edited
        :type team: Team
        """
        self.team = team

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
                self.process_option(selected, team)

            if selected.id in ["EXIT", "RETURN"]:
                break

            else:
                self.logger.log(message="")

        return
