"""Combat Player Actions module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from src.base.color import Color, color_string
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.menus.option import Option

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.systems.settings import Settings


class CombatPlayerActionsMenu(Menu):
    """
    CombatPlayerActionsMenu class.

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

    def get_title(self) -> None:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        pass

    def get_options(self) -> List[Option]:
        """
        Returns the Menu options.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="ROLL_DICE",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="roll_dice",
                ),
            ),
            Option(
                id="SKILLS",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="skills",
                ),
            ),
            Option(
                id="CONSUMABLES",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="consumables",
                ),
            ),
            Option(
                id="EQUIPMENT",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="equipment",
                ),
            ),
            Option(
                id="SHOW_DETAILS",
                key="5",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="show_details",
                ),
            ),
            Option(
                id="SKIP_TURN",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="skip_turn",
                ),
                isolate_before=True,
                isolate_after=True,
            ),
        ]

        return options

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option, monster: Monster) -> bool:
        """
        Returns if the option can be selected or not.

        :param option: Menu's option.
        :type option: Option

        :param monster: Monster being currently controlled by a player.
        :type monster: Monster

        :return: If the option can be selected.
        :rtype: bool
        """
        if option.id in [
            "SKILLS",
            "CONSUMABLES",
            "EQUIPMENT",
        ]:
            return False

        return True

    def process_option(self, option: Option, monster: Monster) -> bool:
        """
        Processes an option chosen by a player.

        :param option: Menu's option.
        :type option: Option

        :param monster: Monster being currently controlled by a player.
        :type monster: Monster

        :return: If the player turn has been taken or if will continue.
        :rtype: bool
        """
        if option.id == "ROLL_DICE":
            return True

        elif option.id == "SKILLS":
            return True

        elif option.id == "CONSUMABLES":
            return False

        elif option.id == "EQUIPMENT":
            return False

        elif option.id == "SHOW_DETAILS":
            return False

        elif option.id == "SKIP_TURN":
            return self.skip_turn(monster)

    def skip_turn(self, monster: Monster) -> Literal[True]:
        """
        Skips a monster's turn.

        :param monster: Monster being currently controlled by a player.
        :type monster: Monster

        :return: If the player turn has been taken or if will continue.
        :rtype: Literal[True]
        """
        self.logger.log_turn_skip(monster=monster)

        return True

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_options(self, monster: Monster):
        """
        Shows the Menu options.

        :param monster: Monster being currently controlled by a player.
        :type monster: Monster
        """
        for option in self.options:
            message = ""

            if option.isolate_before:
                message += "\n"

            message += f"[{option.key}] {option.message}"

            if option.isolate_after:
                message += "\n"

            if not self.is_option_valid(option, monster):
                message = color_string(message, foreground_color=Color.RED)

            self.logger.log(message=message)

        if not self.options[-1].isolate_after:
            self.logger.log(message="")

        return

    def open(self, monster: Monster):
        """
        Opens the Menu.

        :param monster: Monster being currently controlled by a player.
        :type monster: Monster
        """
        turn_taken = False

        while not turn_taken:
            self.show_title()
            self.show_options(monster)
            selected = self.select_option()

            if self.is_option_valid(selected, monster):
                turn_taken = self.process_option(selected, monster)

        self.logger.input(message="")

        return
