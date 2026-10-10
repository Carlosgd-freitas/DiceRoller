"""Roguelike Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.color import color_string
from src.base.difficulties import get_difficulty_color
from src.gamemodes.roguelike.select_character_menu import SelectCharacterMenu
from src.gamemodes.roguelike.select_difficulty_menu import SelectDifficultyMenu
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.menus.edit_menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.systems.settings import Settings


class RoguelikeMenu(Menu):
    """
    Roguelike Menu class.

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

        # Character
        self.character = settings.last_character
        self.select_character_menu = SelectCharacterMenu(
            settings,
            logging=logging,
        )

        # Difficulty
        self.difficulty = settings.last_difficulty
        self.select_difficulty_menu = SelectDifficultyMenu(
            settings,
            logging=logging,
        )

    def get_title(self) -> str:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="menus", message_group="ROGUELIKE", key="title"
        )

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.
        """
        options = [
            Option(
                id="NEW_RUN",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="ROGUELIKE",
                    key="new_run",
                ),
                isolate_after=True,
            ),
            Option(
                id="SELECT_CHARACTER",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="ROGUELIKE",
                    key="select_character",
                ),
            ),
            Option(
                id="SELECT_DIFFICULTY",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="ROGUELIKE",
                    key="select_difficulty",
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
        Changes the Menu language.

        :var language: A Language.
        :vartype language: Language

        :var _messages: Messages loaded from a locale module.
        :vartype _messages: Dict
        """
        self.logger.change_language(language, _messages)
        _messages = self.logger._messages

        self.title = self.get_title()
        self.options = self.get_options()

        self.select_character_menu.change_language(language, _messages)
        self.select_difficulty_menu.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Menu logging.

        :var enabled: If the Menu logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled

        self.select_character_menu.toggle_logging(enabled)
        self.select_difficulty_menu.toggle_logging(enabled)

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        return True

    def process_option(self, option: Option):
        """
        Processes an option.
        """
        if option.id == "NEW_RUN":
            self.new_run()

        elif option.id == "SELECT_CHARACTER":
            self.select_character_menu.character = self.character
            self.select_character_menu.open()
            self.character = self.select_character_menu.character
            self.settings.last_character = self.character

        elif option.id == "SELECT_DIFFICULTY":
            self.select_difficulty_menu.difficulty = self.difficulty
            self.select_difficulty_menu.open()
            self.difficulty = self.select_difficulty_menu.difficulty
            self.settings.last_difficulty = self.difficulty

        elif option.id == "EXIT":
            pass

        return

    def new_run(self):
        """
        Starts a new run in roguelike mode with the current selected game elements.
        """
        pass

    # =========================================================================
    # Rendering
    # =========================================================================

    def open(self):
        """
        Opens the Menu.
        """
        while True:
            self.show_title()

            # Logging selected character
            message = color_string(
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="character",
                ).title()
                + ": ",
                intensity="BRIGHT",
            )

            self.logger.log(
                message=message,
                end="",
            )

            message = self.logger.get_message(
                namespace="characters",
                message_group=self.character.global_id,
                key="name",
            )

            color_data = self.character.get_color()

            self.logger.log(message=color_string(message, **color_data))

            # Logging selected difficulty
            message = color_string(
                self.logger.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="difficulty",
                ).title()
                + ": ",
                intensity="BRIGHT",
            )

            self.logger.log(
                message=message,
                end="",
            )

            message = self.logger.get_message(
                namespace="difficulties",
                message_group=self.difficulty.name,
                key="name",
            )

            color_data = get_difficulty_color(self.difficulty)

            self.logger.log(message=color_string(message, **color_data))

            self.logger.log(message="")

            # Logging options
            self.show_options(self.options)

            message = self.logger.get_message(
                namespace="menus",
                message_group="BASE",
                key="select_option_prompt",
            )
            selected = self.select(self.options, message)
            self.process_option(selected)

            if selected.id in ["EXIT", "RETURN"]:
                break

            else:
                self.logger.log(message="")

        return
