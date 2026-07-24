"""Stat Logger module."""

from src.base.color import Color, color_string
from src.base.stat import Stat
from src.base.text import numeric_to_string
from src.logger.attributes import AttributeLogger


class StatLogger(AttributeLogger):
    """
    StatLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def log_stat_details(
        self,
        stat: Stat,
    ):
        """
        Logs a Stat details.

        :param stat: A stat.
        :type stat: Stat
        """
        if not self.enabled:
            return

        # Flat
        message = (
            self.get_message(
                namespace="base",
                message_group="LEXICON",
                key="flat",
            ).capitalize()
            + ":"
        )
        message = color_string(message, intensity="BRIGHT") + " "

        if stat.flat is None:
            message += color_string("-", foreground_color=Color.RED)

        else:
            message += numeric_to_string(stat.flat)

        self.log(message=message)

        # Percent
        message = (
            self.get_message(
                namespace="base",
                message_group="LEXICON",
                key="percent",
            ).capitalize()
            + ":"
        )
        message = color_string(message, intensity="BRIGHT") + " "

        if stat.percent is None:
            message += color_string("-", foreground_color=Color.RED)

        else:
            message += numeric_to_string(stat.percent)
            message += f"({numeric_to_string(stat.percent * 100)}%)"

        self.log(message=message)
