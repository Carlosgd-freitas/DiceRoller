"""Side Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.color import color_string
from src.logger.effects import EffectLogger

if TYPE_CHECKING:
    from src.base.side import Side


class SideLogger(EffectLogger):
    """
    SideLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def get_side_effects_message(
        self,
        side: Side,
        index: int = None,
    ) -> str:
        """
        Gets a message for a Side effects.

        :param side: A side.
        :type side: Side

        :var index: Side index.
        :vartype index: int

        :return: Message containg the Side effects.
        :rtype: str
        """
        if not self.enabled:
            return

        if side.effects:
            # Index
            if index is None:
                message = ""
            else:
                message = f"[{index}] "

            message += self.get_multiple_effects_message(
                effects=side.effects,
                separator=" + ",
            )

        else:
            message = self.get_message(
                namespace="base",
                message_group="DETAILS",
                key="no_effects",
            )

        return message

    def log_side_details(
        self,
        side: Side,
        index: int = None,
        weight: bool = True,
    ):
        """
        Logs a Side details.

        :param side: A side.
        :type side: Side

        :var index: Side index.
        :vartype index: int

        :param weight: If the side weight will be logged. Default value is True.
        :type weight: bool
        """
        if not self.enabled:
            return

        # Effects
        message = self.get_side_effects_message(side, index)
        self.log(message=message)

        # Weight
        if weight:
            message = self.get_message(
                namespace="base",
                message_group="LEXICON",
                key="weight",
            ).capitalize()
            message = color_string(message, intensity="BRIGHT")

            message += f": {side.weight}"

            self.log(message=message)
