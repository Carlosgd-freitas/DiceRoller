"""Edit Effect Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar

from src.base.effect import Effect
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings

T = TypeVar("T")


class EditEffectMenu(EditMenu):
    """
    Edit Effect Menu class.

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
            message_group="EDIT_EFFECT",
            logging=logging,
            randomizer=randomizer,
        )
        self.editing: Effect = None

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="CHANGE_KEYWORD",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="change_keyword",
                ),
            ),
            Option(
                id="EDIT_VALUE",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_value",
                ),
            ),
            Option(
                id="EDIT_VALUE_PERCENT",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_value_percent",
                ),
            ),
            Option(
                id="EDIT_DURATION",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_duration",
                ),
            ),
            Option(
                id="EDIT_DECAY",
                key="5",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_decay",
                ),
            ),
            Option(
                id="EDIT_ACCURACY",
                key="6",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_accuracy",
                ),
            ),
            Option(
                id="EDIT_REMOVABLE",
                key="7",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_removable",
                ),
            ),
            Option(
                id="ADD_TARGET_KEYWORD",
                key="8",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="add_target_keyword",
                ),
            ),
            Option(
                id="REMOVE_TARGET_KEYWORD",
                key="9",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="remove_target_keywords",
                ),
                isolate_after=True,
            ),
            Option(
                id="RANDOMIZE_EFFECT",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="randomize_effect",
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

    def _target_keywords_as_options(self) -> List[Option]:
        """
        Returns the target keywords of the Effect being edited as Options.

        :return: Effect target keywords as options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id=f"TARGET_KEYWORD_{idx+1}",
                key=str(idx + 1),
                message=self.logger.get_effect_message(
                    keyword=keyword, associated=False
                ),
                obj=keyword,
            )
            for idx, keyword in enumerate(self.editing.target_keywords)
        ]

        options.append(
            Option(
                id="CANCEL",
                key="0",
                message=None,
            )
        )

        return options

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        ## Discuir com o GPT: Efeitos possuem apenas alguns atributos, e esses podem ser editados.
        ## Ex.: Heal pode ter value/value_percentage; Attack apenas value; etc.

        if option.id in ["REMOVE_TARGET_KEYWORD"]:
            return len(self.editing.target_keywords) > 0

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param side: Side to be edited.
        :type side: Side
        """
        if option.id == "CHANGE_KEYWORD":
            pass

        elif option.id == "EDIT_VALUE":
            self.edit_attribute("value", int)

        elif option.id == "EDIT_VALUE_PERCENT":
            self.edit_attribute("value_percent", float)

        elif option.id == "EDIT_DURATION":
            self.edit_attribute("duration", int)

        elif option.id == "EDIT_DECAY":
            self.edit_attribute("decay", int)

        elif option.id == "EDIT_ACCURACY":
            self.edit_attribute("accuracy", int)

        elif option.id == "EDIT_REMOVABLE":
            pass

        elif option.id == "ADD_TARGET_KEYWORD":
            pass

        elif option.id == "REMOVE_TARGET_KEYWORD":
            pass

        elif option.id == "RANDOMIZE_EFFECT":
            randomized_effect = self.randomizer.get_random_effect()
            self.editing = randomized_effect

        elif option.id == "RETURN":
            pass

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_editing_details(self):
        """
        Shows the details of the object being edited.
        """
        message = self.logger.get_effect_message(effect=self.editing)
        self.logger.log(message=message)
