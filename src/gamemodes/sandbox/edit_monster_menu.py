"""Edit Monster Menu module."""

## TODO

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.team import Team
from src.combat.manager import CombatData
from src.gamemodes.sandbox.edit_dice_menu import EditDiceMenu
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings

EXTENSION = ".monster.dat"


# Generate Global ID


class EditMonsterMenu(EditMenu):
    """
    Edit Monster Menu class.

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
            message_group="EDIT_MONSTER",
            logging=logging,
            randomizer=randomizer,
        )
        self.editing: Team = None

        self.edit_dice_menu = EditDiceMenu(
            settings,
            logging=logging,
            randomizer=randomizer,
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
            ),
            Option(
                id="EDIT_HP",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="EDIT_MANA",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="EDIT_SPEED",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="EDIT_CONTROL_TYPE",
                key="5",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="EDIT_DIFFICULTY",
                key="6",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="EDIT_DICE",
                key="7",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="EDIT_EQUIPMENT",
                key="8",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="EDIT_SKILLS",
                key="9",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="edit_combat",
                ),
            ),
            Option(
                id="IMPORT_MONSTER",
                key="I",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="import_combat",
                ),
                isolate_before=True,
            ),
            Option(
                id="EXPORT_MONSTER",
                key="E",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="SANDBOX",
                    key="export_combat",
                ),
            ),
            Option(
                id="RANDOMIZE_MONSTER",
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
        if option.id == "EDIT_SKILLS":
            return False

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

    def show_editing_details(self):
        """
        Shows the details of the object being edited.
        """
        self.logger.log_monster_details(
            self.editing,
            description=False,
            control_type=True,
        )
        self.logger.log(message="")
