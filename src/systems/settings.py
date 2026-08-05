"""Settings module."""

from typing import Literal

from src.locales.languages import Language

BASENAME = "settings"
EXTENSION = ".dat"
FILENAME = BASENAME + EXTENSION


class Settings:
    """
    Settings class.

    :var language: Language that will be used in the game. Default value is
    Language.EN_US.
    :vartype language: Language

    :var monster_end_turn: If ending a AI-controlled monster's turn needs an input
    from the player ("MANUAL") or not ("AUTO"). Default value is "MANUAL".
    :vartype monster_end_turn: Literal["AUTO", "MANUAL"]
    """

    def __init__(
        self,
        language: Language = Language.EN_US,
        monster_end_turn: Literal["AUTO", "MANUAL"] = "MANUAL",
    ):
        self.language = language
        self.monster_end_turn = monster_end_turn
