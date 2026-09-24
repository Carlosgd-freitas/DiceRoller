"""Difficulties module."""

from enum import Enum

from src.base.color import Color, ColorData


class Difficulty(Enum):
    """Game difficulty level."""

    EASY = 0
    NORMAL = 1
    HARD = 2
    EXPERT = 3
    MASTER = 4
    NIGHTMARE = 5


def get_difficulty_color(difficulty: Difficulty) -> ColorData:
    """
    Gets a Difficulty color data.

    :param difficulty: A Difficulty.
    :type difficulty: Difficulty

    :return: The difficulty color data.
    :rtype: ColorData
    """
    foreground_color = None
    background_color = None
    intensity = "BRIGHT"

    if difficulty == Difficulty.EASY:
        foreground_color = Color.GREEN

    elif difficulty == Difficulty.NORMAL:
        foreground_color = Color.YELLOW

    elif difficulty == Difficulty.HARD:
        foreground_color = Color.ORANGE

    elif difficulty == Difficulty.EXPERT:
        foreground_color = Color.RED

    elif difficulty == Difficulty.MASTER:
        foreground_color = Color.VIOLET

    elif difficulty == Difficulty.NIGHTMARE:
        foreground_color = Color.GRAY

    return {
        "background_color": background_color,
        "foreground_color": foreground_color,
        "intensity": intensity,
    }
