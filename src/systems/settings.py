"""Settings module."""

from enum import Enum
from typing import ClassVar, Literal

from src.base.character import Character
from src.base.difficulties import Difficulty
from src.characters.warrior import Warrior
from src.locales.languages import Language

BASENAME = "settings"
EXTENSION = ".dat"
FILENAME = BASENAME + EXTENSION


class Toggle(Enum):
    """
    On/off state for a toggleable setting.
    """

    ON = True
    OFF = False


class Settings:
    """
    Settings class.

    :var language: Language that will be used in the game. Default value is
    Language.EN_US.
    :vartype language: Language

    :var monster_end_turn: If ending a AI-controlled monster's turn needs an input
    from the player ("MANUAL") or not ("AUTO"). Default value is "MANUAL".
    :vartype monster_end_turn: Literal["AUTO", "MANUAL"]

    :var exit_confirmation: If confirmation will be prompted to the user on major exit
    operations. Default value is Toggle.ON.
    :vartype exit_confirmation: Toggle

    :var last_difficulty: Last difficulty chosen by the player. Default value is
    Difficulty.NORMAL.
    :vartype last_difficulty: Difficulty

    :var last_character: Last character chosen by the player. Default value is
    Warrior.
    :vartype last_character: Difficulty
    """

    # Default values
    _DEFAULT_LANGUAGE: ClassVar[Language] = Language.EN_US
    _DEFAULT_MONSTER_END_TURN: ClassVar[Literal["AUTO", "MANUAL"]] = "MANUAL"
    _DEFAULT_EXIT_CONFIRMATION: ClassVar[Toggle] = Toggle.ON
    _DEFAULT_LAST_DIFFICULTY: ClassVar[Difficulty] = Difficulty.NORMAL
    _DEFAULT_CHARACTER_FACTORY: ClassVar[type[Character]] = Warrior

    # Defaults for settings that don't require a factory
    _DEFAULTS: ClassVar[dict[str, object]] = {
        "language": _DEFAULT_LANGUAGE,
        "monster_end_turn": _DEFAULT_MONSTER_END_TURN,
        "exit_confirmation": _DEFAULT_EXIT_CONFIRMATION,
        "last_difficulty": _DEFAULT_LAST_DIFFICULTY,
    }

    def __init__(
        self,
        language: Language = _DEFAULT_LANGUAGE,
        monster_end_turn: Literal["AUTO", "MANUAL"] = _DEFAULT_MONSTER_END_TURN,
        exit_confirmation: Toggle = _DEFAULT_EXIT_CONFIRMATION,
        last_character: Character = None,
        last_difficulty: Difficulty = _DEFAULT_LAST_DIFFICULTY,
    ):
        # Changeable on settings menu
        self.language = language
        self.monster_end_turn = monster_end_turn
        self.exit_confirmation = exit_confirmation

        # Changeable by other means
        if last_character is None:
            last_character = self._DEFAULT_CHARACTER_FACTORY()
        self.last_character = last_character

        self.last_difficulty = last_difficulty

    def migrate(self) -> bool:
        """
        Add missing settings while preserving existing values.

        :return: If the Settings object was modified.
        :rtype: bool
        """
        changed = False

        for name, default in self._DEFAULTS.items():
            if not hasattr(self, name):
                setattr(self, name, default)
                changed = True

        if not hasattr(self, "last_character") or self.last_character is None:
            self.last_character = self._DEFAULT_CHARACTER_FACTORY()
            changed = True

        return changed
