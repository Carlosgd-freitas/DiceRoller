"""Roguelike Gamemode Player Actions module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, TypeVar

from src.combat.effects import EffectManager
from src.combat.team_manager import TeamManager
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.menus.option import Option

T = TypeVar("T")

if TYPE_CHECKING:
    from src.base.team import Team
    from src.systems.settings import Settings


class RoguelikePlayerActionsMenu(Menu):
    """
    RoguelikePlayerActionsMenu class.

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
        teams: List[Team] = None,
    ):
        # Initialization
        logger = CombatLogger(enabled=logging, language=settings.language)

        super().__init__(
            logger,
            settings,
        )

        self.logger: CombatLogger

        # Effect Management
        self.effect_manager = EffectManager(settings, logging)

        # Team Management
        self.teams = [] if teams is None else teams
        self.team_manager = TeamManager()

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
                id="WALK",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="walk",
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
                message_invalid=self.logger.get_message(
                    namespace="combat",
                    message_group="ACTIONS",
                    key="no_skills",
                    format=False,
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
                message_invalid=self.logger.get_message(
                    namespace="combat",
                    message_group="ACTIONS",
                    key="no_consumables",
                    format=False,
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
                message_invalid=self.logger.get_message(
                    namespace="combat",
                    message_group="ACTIONS",
                    key="no_equipment",
                    format=False,
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
                message_invalid=self.logger.get_message(
                    namespace="combat",
                    message_group="ACTIONS",
                    key="no_show_details",
                    format=False,
                ),
            ),
            Option(
                id="EXIT",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="exit",
                ),
                isolate_before=True,
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

        self.options = self.get_options()

        # Managers
        self.effect_manager.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Menu logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled

        # Managers
        self.effect_manager.toggle_logging(enabled)
