"""Settings module."""

import pickle
from pathlib import Path
from typing import List, Literal

from src.locales.languages import Language

FILENAME = "settings.dat"


class Settings:
    """
    Settings class.

    :var language: Language that will be used in the game. Default value is
    Language.EN_US.
    :vartype language: Language

    :var end_turn_ai_monsters: If ending a AI-controlled monster's turn needs an input
    from the player ("MANUAL") or not ("AUTO"). Default value is "MANUAL".
    :vartype end_turn_ai_monsters: Literal["AUTO", "MANUAL"]
    """

    def __init__(
        self,
        language: Language = Language.EN_US,
        end_turn_ai_monsters: Literal["AUTO", "MANUAL"] = "MANUAL",
    ):
        self.language = language
        self.end_turn_ai_monsters = end_turn_ai_monsters

    def exists(self) -> bool:
        """
        Checks if the settings file exists.

        :return: If the settings file exists or not.
        :rtype: bool
        """
        file_path = Path(FILENAME)

        return file_path.is_file()

    def save(self):
        """
        Saves the settings on a file.
        """
        with open(FILENAME, "wb") as f:
            pickle.dump(self, f)

        return

    def load(self):
        """
        Loads the settings from a file.
        """
        with open(FILENAME, "rb") as f:
            new_settings = pickle.load(f)

        self.__dict__.update(new_settings.__dict__)

    def switch_setting(self, setting_name: str, values: List):
        """
        Switches a setting for next possible value in a setting of values.
        """
        setting_value = getattr(self, setting_name)
        index = values.index(setting_value)
        new_value = values[(index + 1) % len(values)]
        setattr(self, setting_name, new_value)
