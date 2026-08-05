"""Edit Effect Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.color import Color, color_string
from src.base.effect import Effect
from src.base.keywords import Keyword
from src.base.text import numeric_to_string
from src.gamemodes.sandbox.edit_stat_menu import EditStatMenu
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings


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

        self.edit_stat_menu = EditStatMenu(
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
                id="EDIT_MIN_VALUE",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_min_value",
                ),
            ),
            Option(
                id="EDIT_MAX_VALUE",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_max_value",
                ),
            ),
            Option(
                id="EDIT_DURATION",
                key="5",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_duration",
                ),
            ),
            Option(
                id="EDIT_DELTA",
                key="6",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_delta",
                ),
            ),
            Option(
                id="EDIT_ACCURACY",
                key="7",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_accuracy",
                ),
            ),
            Option(
                id="CHANGE_REMOVABLE",
                key="8",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="change_removable",
                ),
            ),
            Option(
                id="ADD_TARGET_KEYWORD",
                key="9",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="add_target_keyword",
                ),
            ),
            Option(
                id="REMOVE_TARGET_KEYWORD",
                key="10",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="remove_target_keyword",
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
        if option.id == "EDIT_VALUE":
            return self.editing.value is not None

        elif option.id == "EDIT_MIN_VALUE":
            return self.editing.min_value is not None

        elif option.id == "EDIT_MAX_VALUE":
            return self.editing.max_value is not None

        elif option.id == "EDIT_DURATION":
            return self.editing.duration is not None

        elif option.id == "EDIT_DELTA":
            return self.editing.delta is not None

        elif option.id == "EDIT_ACCURACY":
            return self.editing.accuracy is not None

        elif option.id == "CHANGE_REMOVABLE":
            return self.editing.removable is not None

        elif option.id == "ADD_TARGET_KEYWORD":
            return self.editing.target_keywords is not None

        elif option.id == "REMOVE_TARGET_KEYWORD":
            return (
                self.editing.target_keywords is not None
                and len(self.editing.target_keywords) > 0
            )

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
            self.edit_stat_menu.open(self.editing.value)

        elif option.id == "EDIT_MIN_VALUE":
            self.edit_stat_menu.open(self.editing.min_value)

        elif option.id == "EDIT_MAX_VALUE":
            self.edit_stat_menu.open(self.editing.max_value)

        elif option.id == "EDIT_DURATION":
            self.edit_attribute("duration", int)

        elif option.id == "EDIT_DELTA":
            self.edit_stat_menu.open(self.editing.delta)

        elif option.id == "EDIT_ACCURACY":
            self.edit_attribute("accuracy", float)

        elif option.id == "CHANGE_REMOVABLE":
            self.editing.removable = not self.editing.removable

        elif option.id == "ADD_TARGET_KEYWORD":
            pass

        elif option.id == "REMOVE_TARGET_KEYWORD":
            self.remove_target_keyword()

        elif option.id == "RANDOMIZE_EFFECT":
            randomized_effect = self.randomizer.get_random_effect()
            self.editing = randomized_effect

        elif option.id == "RETURN":
            pass

        return

    def _select_target_keyword(self) -> Option:
        """
        Shows the target keywords of the Effect being edited and prompts the user to
        select one of them, returning the corresponding option.

        :return: Option selected by the user.
        :rtype: Option
        """
        options = []

        # Defining options
        self.logger.log(message="")

        for index, target_keyword in enumerate(self.editing.target_keywords):
            option = Option(
                id=f"TARGET_KEYWORD_{index + 1}",
                key=str(index + 1),
                message=self.logger.get_effect_message(keyword=target_keyword),
                obj=target_keyword,
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
        selected_option = self.select_attribute_option(options, "target_keyword")

        return selected_option

    def remove_target_keyword(self):
        """
        Removes a target keyword from the Effect being edited.
        """
        selected_option = self._select_target_keyword()

        if selected_option.id != "CANCEL":
            selected_target_keyword: Keyword = selected_option.obj
            self.editing.target_keywords.remove(selected_target_keyword)

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_editing_details(self):
        """
        Shows the details of the object being edited.
        """
        # Name
        message = self.logger.get_effect_message(
            keyword=self.editing.keyword,
            associated=False,
        )
        self.logger.log(message=message + "\n")

        # Description
        self.logger.log_effect_description(
            effect=self.editing,
            variation="variable",
        )
        self.logger.log(message="")

        # Type
        message = (
            self.logger.get_message(
                namespace="base",
                message_group="LEXICON",
                key="type",
            ).title()
            + ": "
        )
        message = color_string(message, intensity="BRIGHT")
        self.logger.log(message=message, end="")

        message = self.logger.get_message(
            namespace="effect_types",
            message_group=self.editing.type.name,
            key="name",
        ).title()

        self.logger.log(message=message)

        # Value
        if self.editing.value is not None:
            message = (
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="value",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.logger.log(message=message, end="")

            values = []
            if self.editing.value.flat is not None:
                values.append(numeric_to_string(self.editing.value.flat))
            if self.editing.value.percent is not None:
                values.append(numeric_to_string(self.editing.value.percent * 100) + "%")

            message = " + ".join(values)
            self.logger.log(message=message)

        # Min Value
        if self.editing.min_value is not None:
            message = (
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="min_value",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.logger.log(message=message, end="")

            values = []
            if self.editing.min_value.flat is not None:
                values.append(numeric_to_string(self.editing.min_value.flat))
            if self.editing.min_value.percent is not None:
                values.append(
                    numeric_to_string(self.editing.min_value.percent * 100) + "%"
                )

            message = " + ".join(values)
            self.logger.log(message=message)

        # Max Value
        if self.editing.max_value is not None:
            message = (
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="max_value",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.logger.log(message=message, end="")

            values = []
            if self.editing.max_value.flat is not None:
                values.append(numeric_to_string(self.editing.max_value.flat))
            if self.editing.max_value.percent is not None:
                values.append(
                    numeric_to_string(self.editing.max_value.percent * 100) + "%"
                )

            message = " + ".join(values)
            self.logger.log(message=message)

        # Duration
        if self.editing.duration is not None:
            message = (
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="duration",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.logger.log(message=message, end="")

            message = numeric_to_string(self.editing.duration)
            message += (
                " "
                + self.logger.pluralize(
                    self.editing.duration,
                    namespace="base",
                    message_group="LEXICON",
                    key="turn",
                ).title()
            )
            self.logger.log(message=message)

        # Delta
        if self.editing.delta is not None:
            message = (
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="delta",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.logger.log(message=message, end="")

            values = []
            if self.editing.delta.flat is not None:
                values.append(numeric_to_string(self.editing.delta.flat))
            if self.editing.delta.percent is not None:
                values.append(numeric_to_string(self.editing.delta.percent * 100) + "%")

            message = " + ".join(values)
            self.logger.log(message=message)

        # Accuracy
        if self.editing.accuracy is not None:
            message = (
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="accuracy",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.logger.log(message=message, end="")

            message = numeric_to_string(self.editing.accuracy * 100) + "%"
            self.logger.log(message=message)

        # Removable
        if self.editing.removable is not None:
            message = (
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="removable",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.logger.log(message=message, end="")

            if self.editing.removable is True:
                message = self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="yes",
                ).title()

            else:
                message = self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="no",
                ).title()

            self.logger.log_boolean(message=message, value=self.editing.removable)

        # Target Keywords
        if self.editing.target_keywords is not None:
            message = (
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="target_keywords",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.logger.log(message=message, end="")

            if len(self.editing.target_keywords) > 0:
                message = self.logger.get_multiple_effects_message(
                    keywords=self.editing.target_keywords
                )
            else:
                message = color_string("-", foreground_color=Color.RED)

            self.logger.log(message=message)

        self.logger.log(message="")
