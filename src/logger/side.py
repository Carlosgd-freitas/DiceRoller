"""Side Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING

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

    def get_side_details(
        self,
        side: Side,
        index: int = None,
    ) -> str:
        """
        Logs a Side details.

        :param side: A side.
        :type side: Side

        :var index: Side index.
        :vartype index: int

        :return: Side details.
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
