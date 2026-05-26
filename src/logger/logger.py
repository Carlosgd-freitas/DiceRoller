"""Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.color import Color, color_string
from src.base.keywords import get_keyword_color
from src.logger.languages.en_us import MESSAGES as EN_US
from src.logger.languages.pt_br import MESSAGES as PT_BR

if TYPE_CHECKING:
    from src.base.monster import Monster

LANGUAGES = {
    "EN-US": EN_US,
    "PT-BR": PT_BR,
}


class Logger:
    """
    Logger class.
    """

    def __init__(
        self,
        enabled: bool = True,
        language: str = "EN-US",
    ):
        self.enabled = enabled
        self.language = language

    def get_message(
        self,
        key: str,
        **kwargs,
    ) -> str:
        message: str = LANGUAGES[self.language][key]

        return message.format(**kwargs)

    def log(
        self,
        message: str = None,
        key: str = None,
        end: str = "\n",
        **kwargs,
    ) -> None:
        if not self.enabled:
            return

        if key:
            message: str = self.get_message(key, **kwargs)

        print(message, end=end)

        return

    def log_round(self, round: int):
        self.log(message="\n╔═══════════════╗")
        self.log(
            key="round",
            round=round,
        )
        self.log(message="╚═══════════════╝")

    def log_monster(self, monster: Monster):
        # Name
        self.log(message=f"> {monster.name} - ", end="")

        # HP
        self.log(
            message=color_string(
                "HP",
                foreground_color=Color.RED,
            ),
            end="",
        )
        self.log(message=f": {monster.hp}/{monster.max_hp}", end="")

        # Effects
        for effect in monster.effects:
            self.log(message=" - ", end="")

            color_data = get_keyword_color(effect.keyword)

            effect_keyword = self.get_message(
                key="status_" + effect.keyword.value.lower()
            )
            effect_keyword = color_string(
                effect_keyword,
                foreground_color=color_data["foreground_color"],
                intensity=color_data["intensity"],
            )

            self.log(message=effect_keyword, end="")

            self.log(message=f" {effect.value}", end="")

        self.log("")

    def log_teams(self, teams: List[List[Monster]]):
        for team_index, team in enumerate(teams):
            team_name = team[0].team_name
            self.log(key="team", index=team_index + 1, team_name=team_name)

            for monster in team:
                self.log_monster(monster)

            if team_index < len(teams) - 1:
                self.log(message="")
