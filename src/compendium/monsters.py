"""Monsters Compendium module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.compendium.compendium import Compendium
from src.factories.monster import MonsterFactory
from src.logger.effects import EffectLogger

if TYPE_CHECKING:
    from src.systems.settings import Settings


class MonsterCompendium(Compendium):
    """
    Monster Compendium class.

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
        items = MonsterFactory.get_all_objects()

        logger = EffectLogger(enabled=logging, language=settings.language)

        super().__init__(
            logger=logger,
            settings=settings,
            items=items,
            alignments=("right", "left", "left"),
        )

        self.logger: EffectLogger
