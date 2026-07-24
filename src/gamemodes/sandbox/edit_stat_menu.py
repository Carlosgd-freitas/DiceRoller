"""Edit Stat Menu module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.stat import Stat
from src.menus.edit_menu import EditMenu
from src.menus.option import Option
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.systems.settings import Settings


class EditStatMenu(EditMenu):
    """
    Edit Stat Menu class.

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
            message_group="EDIT_STAT",
            logging=logging,
            randomizer=randomizer,
        )
        self.editing: Stat = None

    def get_options(self) -> List[Option]:
        """
        Returns the options that will be used by the Menu.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="EDIT_FLAT",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_flat",
                ),
            ),
            Option(
                id="EDIT_PERCENT",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="edit_percent",
                ),
                isolate_after=True,
            ),
            Option(
                id="RANDOMIZE_STAT",
                key="R",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group=self.message_group,
                    key="randomize_stat",
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

    def is_option_valid(self, option: Option) -> bool:
        """
        Returns if the option can be selected or not.
        """
        if option.id == "EDIT_FLAT":
            return self.editing.flat is not None

        elif option.id == "EDIT_PERCENT":
            return self.editing.percent is not None

        return True

    def process_option(self, option: Option):
        """
        Processes an option.

        :param side: Side to be edited.
        :type side: Side
        """
        if option.id == "EDIT_FLAT":
            self.edit_attribute("flat", int)

        if option.id == "EDIT_PERCENT":
            self.edit_attribute("percent", float)

        elif option.id == "RANDOMIZE_STAT":
            randomized_stat = self.randomizer.get_random_stat()
            self.editing = randomized_stat

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
        self.logger.log_stat_details(self.editing)
