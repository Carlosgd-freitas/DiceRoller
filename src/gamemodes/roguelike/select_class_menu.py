"""Select Class Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.color import color_string
from src.base.data import (
    next_value,
    previous_value,
)
from src.classes.mage import Mage
from src.classes.ranger import Ranger
from src.classes.rogue import Rogue
from src.classes.warrior import Warrior
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.classes.base_class import BaseClass
    from src.systems.settings import Settings


class SelectClassMenu(Menu):
    """
    Select Class Menu class.

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
    ):
        # Initialization
        logger = CombatLogger(enabled=logging, language=settings.language)

        self.class_ = settings.last_class
        self.classes: List[BaseClass] = [
            Warrior(),
            Mage(),
            Ranger(),
            Rogue(),
        ]
        self.showing_class: BaseClass = None

        super().__init__(
            logger,
            settings,
        )

        self.logger: CombatLogger

        self.submenu_options = self.get_submenu_options()

    def get_title(self) -> str:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="menus", message_group="SELECT_CLASS", key="title"
        )

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = []

        for index, class_ in enumerate(self.classes, start=1):
            message = self.logger.get_message(
                namespace="classes",
                message_group=class_.global_id,
                key="name",
            )

            color_data = class_.get_color()

            options.append(
                Option(
                    id=f"CLASS_{index}",
                    key=str(index),
                    message=color_string(
                        message,
                        **color_data,
                    ),
                    obj=class_,
                )
            )

        options.append(
            Option(
                id="RETURN",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="return",
                ),
                isolate_before=True,
                isolate_after=True,
            )
        )

        return options

    def get_submenu_options(self) -> List[Option]:
        """
        Returns the options that will be used by the sub menu.
        """
        options = [
            Option(
                id="PREVIOUS",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="previous",
                ),
            ),
            Option(
                id="NEXT",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="next",
                ),
            ),
            Option(
                id="SELECT",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="select",
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

        :param language: A Language.
        :type language: Language

        :param _messages: Messages loaded from a locale module.
        :type _messages: Dict
        """
        if self.logger:
            self.logger.change_language(language, _messages)

        self.title = self.get_title()
        self.options = self.get_options()
        self.submenu_options = self.get_submenu_options()

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if (option.id == "PREVIOUS") and (
            self.showing_class.global_id == self.classes[0].global_id
        ):
            return False

        elif (option.id == "NEXT") and (
            self.showing_class.global_id == self.classes[-1].global_id
        ):
            return False

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param option: Menu option.
        :type option: Option
        """
        if "CLASS" in option.id:
            self.showing_class = option.obj
            self.show_class(self.showing_class)

            # Showing submenu options
            self.show_options(self.submenu_options)

            # Selecting option
            message = self.logger.get_message(
                namespace="menus",
                message_group="BASE",
                key="select_option_prompt",
            )

            selected_option = self.select(self.submenu_options, message)
            if selected_option:
                self.process_option(selected_option)

        elif option.id == "PREVIOUS":
            difficulty = previous_value(self.classes, self.showing_class)

            for option in self.options:
                if option.obj == difficulty:
                    break

            self.process_option(option)

        elif option.id == "NEXT":
            difficulty = next_value(self.classes, self.showing_class)

            for option in self.options:
                if option.obj == difficulty:
                    break

            self.process_option(option)

        elif option.id == "SELECT":
            self.class_ = self.showing_class

        elif option.id == "RETURN":
            pass

        return

    def show_class(self, class_: BaseClass, **kwargs):
        """
        Shows the class details.
        """
        # Updating logging params
        kwargs.update(self.logger._get_attribute_params())
        kwargs.update(self.logger._get_keyword_params())

        self.logger.log(message="")

        # Name
        name = self.logger.get_message(
            namespace="classes",
            message_group=class_.global_id,
            key="name",
        )
        class_.name = name

        color_data = class_.get_color()

        self.logger.log(message=color_string(name, **color_data) + "\n")

        # Description
        message = self.logger.get_message(
            namespace="classes",
            message_group=class_.global_id,
            key="description",
        )

        self.logger.log(message=color_string(message, italic=True) + "\n")

        # Dice
        self.logger.log_monster_details(class_)

        self.logger.log(message="")

        return

    # =========================================================================
    # Rendering
    # =========================================================================

    def open(self):
        """
        Opens the Menu.
        """
        while True:
            self.show_title()

            # Logging selected class
            message = color_string(
                self.logger.get_message(
                    namespace="menus",
                    message_group="SELECT_CLASS",
                    key="selected_class",
                )
                + ": ",
                intensity="BRIGHT",
            )

            self.logger.log(
                message=message,
                end="",
            )

            message = self.logger.get_message(
                namespace="classes",
                message_group=self.class_.global_id,
                key="name",
            )

            color_data = self.class_.get_color()

            self.logger.log(message=color_string(message, **color_data))

            self.logger.log(message="")

            # Logging options
            self.show_options(self.options)

            message = self.logger.get_message(
                namespace="menus",
                message_group="SELECT_CLASS",
                key="select_class_prompt",
            )
            selected = self.select(self.options, message)
            self.process_option(selected)

            if selected.id in ["EXIT", "RETURN"]:
                break

            else:
                self.logger.log(message="")

        return
