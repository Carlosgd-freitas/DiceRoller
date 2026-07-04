"""Dice Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tabulate import tabulate

from src.logger.effects import EffectLogger

if TYPE_CHECKING:
    from src.base.dice import Dice


class DiceLogger(EffectLogger):
    """
    DiceLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def log_dice_details(
        self,
        dice: Dice,
        header: str = None,
    ):
        """
        Logs a Dice details.

        :param dice: A dice.
        :type dice: Dice

        :param header: An optional header when logging.
        :type header: str
        """
        if not self.enabled:
            return

        # Header
        headers = [header] if header else []

        # Sides
        rows = []
        for side in dice.sides:
            message = "● "

            message += self.get_multiple_effects_message(
                effects=side.effects,
                separator=" + ",
            )

            rows.append([message])

        table = tabulate(
            rows,
            headers=headers,
            colalign=("left",),
            headersalign=("center",),
            tablefmt="psql",
        )

        self.log(message=table)

        return
