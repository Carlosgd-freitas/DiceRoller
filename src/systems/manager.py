"""Manager module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.locales.languages import Language

if TYPE_CHECKING:
    from src.logger.logger import Logger
    from src.systems.settings import Settings


class Manager:
    """
    Manager class.

    :var logger: Logger used to print throughout the Manager.
    :vartype logger: Logger

    :var settings: Game settings.
    :vartype settings: Settings
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        logger: Logger,
        settings: Settings,
    ):
        self.logger = logger
        self.settings = settings

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
        if self.logger:
            self.logger.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        if self.logger:
            self.logger.enabled = enabled
