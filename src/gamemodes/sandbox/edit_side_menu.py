"""Edit Side Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.side import Side
from src.effects.nothing import NothingEffect
from src.gamemodes.sandbox.edit_effect_menu import EditEffectMenu
from src.locales.languages import Language
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.systems.settings import Settings


class EditSideMenu(EditMenu):
    """
    Edit Side Menu class.

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
            message_group="EDIT_SIDE",
            logging=logging,
            randomizer=randomizer,
        )
        self.editing: Side = None

        self.edit_effect_menu = EditEffectMenu(
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
                id="EDIT_WEIGHT",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_weight",
                ),
            ),
            Option(
                id="EDIT_EFFECT",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_effect",
                ),
            ),
            Option(
                id="ADD_EFFECT",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="add_effect",
                ),
            ),
            Option(
                id="REMOVE_EFFECT",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="remove_effect",
                ),
                isolate_after=True,
            ),
            Option(
                id="RANDOMIZE_SIDE",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="randomize_side",
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

        self.edit_effect_menu.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled

        self.edit_effect_menu.toggle_logging(enabled)

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id in ["EDIT_EFFECT", "REMOVE_EFFECT"]:
            return len(self.editing.effects) > 0

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param side: Side to be edited.
        :type side: Side
        """
        if option.id == "EDIT_WEIGHT":
            self.edit_attribute("weight", float)

        elif option.id == "EDIT_EFFECT":
            self.edit_effect()

        elif option.id == "ADD_EFFECT":
            self.add_effect()

        elif option.id == "REMOVE_EFFECT":
            self.remove_effect()

        elif option.id == "RANDOMIZE_SIDE":
            randomized_side = self.randomizer.get_random_side()
            self.editing = randomized_side

        elif option.id == "RETURN":
            pass

        return

    def _select_effect(self) -> Option:
        """
        Shows the effects of the Side being edited and prompts the user to select one
        of them, returning the corresponding option.

        :return: Option selected by the user.
        :rtype: Option
        """
        options = []

        # Defining options
        self.logger.log(message="")

        for index, effect in enumerate(self.editing.effects):
            option = Option(
                id=f"EFFECT_{index + 1}",
                key=str(index + 1),
                message=self.logger.get_effect_message(effect=effect),
                obj=effect,
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
        selected_option = self.select_attribute_option(options, "effect")

        return selected_option

    def edit_effect(self):
        """
        Edits an Effect of the Side being edited.
        """
        selected_option = self._select_effect()

        if selected_option.id != "CANCEL":
            selected_effect: Effect = selected_option.obj
            index = self.editing.effects.index(selected_effect)

            edited_effect: Effect = self.edit_effect_menu.open(selected_effect)

            self.editing.effects[index] = edited_effect

        return

    def add_effect(self):
        """
        Adds a new Nothing Effect to the Side being edited, and opens the Edit Effect
        Menu with it.
        """
        new_effect = NothingEffect()
        new_effect = self.edit_effect_menu.open(new_effect)
        self.editing.effects.append(new_effect)

        return

    def remove_effect(self):
        """
        Removes an Effect from the Side being edited.
        """
        selected_option = self._select_effect()

        if selected_option.id != "CANCEL":
            selected_effect: Effect = selected_option.obj
            self.editing.effects.remove(selected_effect)

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_editing_details(self):
        """
        Shows the details of the object being edited.
        """
        self.logger.log_side_details(self.editing, weight=True)
        self.logger.log(message="")
