"""Edit Monster Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.data import next_value
from src.base.dice import Dice
from src.base.monster import AILevel, ControlType, Monster
from src.gamemodes.sandbox.edit_dice_menu import EditDiceMenu
from src.locales.languages import Language
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings

EXTENSION = ".monster.dat"


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
        self.editing: Monster = None

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
                    message_group=self.message_group,
                    key="edit_name",
                ),
            ),
            Option(
                id="EDIT_HP",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_hp",
                ),
            ),
            Option(
                id="EDIT_MANA",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_mana",
                ),
            ),
            Option(
                id="EDIT_SPEED",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_speed",
                ),
            ),
            Option(
                id="CHANGE_CONTROL_TYPE",
                key="5",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="change_control_type",
                ),
            ),
            Option(
                id="CHANGE_AI_LEVEL",
                key="6",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="change_ai_level",
                ),
            ),
            Option(
                id="EDIT_DICE",
                key="7",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_dice",
                ),
            ),
            Option(
                id="ADD_DICE",
                key="8",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="add_dice",
                ),
            ),
            Option(
                id="REMOVE_DICE",
                key="9",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="remove_dice",
                ),
            ),
            Option(
                id="IMPORT_MONSTER",
                key="I",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="import_monster",
                ),
                isolate_before=True,
            ),
            Option(
                id="EXPORT_MONSTER",
                key="E",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="export_monster",
                ),
            ),
            Option(
                id="RANDOMIZE_MONSTER",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="randomize_monster",
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

        self.edit_dice_menu.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled

        self.edit_dice_menu.toggle_logging(enabled)

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id in ["EDIT_DICE", "REMOVE_DICE"]:
            return len(self.editing.dice) > 0

        return True

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "EDIT_NAME":
            self.edit_attribute("name", str)

        elif option.id == "EDIT_HP":
            self.edit_attribute("hp", int)
            self.editing.max_hp = self.editing.hp

        elif option.id == "EDIT_MANA":
            self.edit_attribute("mana", int)

        elif option.id == "EDIT_SPEED":
            self.edit_attribute("speed", int)

        elif option.id == "CHANGE_CONTROL_TYPE":
            self.editing.control_type = next_value(
                [ControlType.AI, ControlType.PLAYER], self.editing.control_type
            )

        elif option.id == "CHANGE_AI_LEVEL":
            self.change_ai_level()

        elif option.id == "EDIT_DICE":
            self.edit_dice()

        elif option.id == "ADD_DICE":
            self.add_dice()

        elif option.id == "REMOVE_DICE":
            self.remove_dice()

        elif option.id == "IMPORT_MONSTER":
            self.import_object("monster", EXTENSION)

        elif option.id == "EXPORT_MONSTER":
            self.export_object("monster", EXTENSION)

        elif option.id == "RANDOMIZE_MONSTER":
            randomized_monster = self.randomizer.get_random_monster()
            self.editing = randomized_monster

        elif option.id == "EXIT":
            pass

        return

    def change_ai_level(self):
        """
        Changes the AI Level of the Monster being edited.
        """
        options = []
        selected_option: Option = None

        # Defining options
        self.logger.log(message="")

        for index, ai_level in enumerate(list(AILevel)):
            message = self.logger.get_message(
                namespace="base",
                message_group="DIFFICULTIES",
                key=ai_level.name.lower(),
            ).title()

            option = Option(
                id=f"AI_LEVEL_{index + 1}",
                key=str(index + 1),
                message=message,
                obj=ai_level,
            )
            options.append(option)

            if self.editing.ai_level == ai_level:
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
        self.show_options(
            options,
            validate=False,
            selected_option=selected_option,
        )

        # Selecting option
        selected_option = self.select_attribute_option(options, "ai_level")

        if selected_option.id != "CANCEL":
            self.editing.ai_level = selected_option.obj

        return

    def _select_dice(self) -> Option:
        """
        Shows the dice of the Monster being edited and prompts the user to select one
        of them, returning the corresponding option.

        :return: Option selected by the user.
        :rtype: Option
        """
        options = []

        # Defining + showing options
        self.logger.log(message="")

        for index, single_dice in enumerate(self.editing.dice):
            header = (
                f"[{index+1}] "
                + self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="dice",
                ).title()
                + f" #{index+1}"
            )

            self.logger.log_dice_details(
                single_dice,
                header=header,
            )

            option = Option(
                id=f"DICE_{index + 1}",
                key=str(index + 1),
                message=f"DICE_{index + 1}",
                obj=single_dice,
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

        self.logger.log(message="")

        # Selecting option
        selected_option = self.select_attribute_option(options, "dice")

        return selected_option

    def edit_dice(self):
        """
        Edits a Dice of the Monster being edited.
        """
        selected_option = self._select_dice()

        if selected_option.id != "CANCEL":
            selected_dice: Dice = selected_option.obj
            index = self.editing.dice.index(selected_dice)

            edited_dice: Dice = self.edit_dice_menu.open(selected_dice)

            self.editing.dice[index] = edited_dice

        return

    def add_dice(self):
        """
        Adds a new Dice to the Monster being edited, and opens the Edit Dice
        Menu with it.
        """
        new_dice = Dice(effects=[])
        new_dice = self.edit_dice_menu.open(new_dice)
        self.editing.dice.append(new_dice)

        return

    def remove_dice(self):
        """
        Removes a Dice from the Monster being edited.
        """
        selected_option = self._select_dice()

        if selected_option.id != "CANCEL":
            selected_dice: Dice = selected_option.obj
            self.editing.dice.remove(selected_dice)

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
