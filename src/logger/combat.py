"""Combat Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.color import color_string
from src.base.keywords import Keyword
from src.logger.logger import Logger

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.team import Team


class CombatLogger(Logger):
    """
    CombatLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def log_round(self, round: int, start_line_break: bool = True):
        """
        Logs the round start.

        :param round: The round number.
        :type round: int

        :param start_line_break: If a line break will be present at the start of the
        logs. Default value is True.
        :type start_line_break: bool
        """
        message = self.get_message(
            namespace="combat",
            message_group="COMBAT",
            key="round",
        )
        message = message + " #" + str(round)

        if start_line_break:
            self.log(message="")

        self.box_message(
            message=message,
            size=24,
            isolate=False,
        )

    def log_turn_start(self, monster: Monster, start_line_break: bool = True):
        """
        Logs a Monster's turn start in combat.

        :param monster: A monster.
        :type monster: Monster

        :param start_line_break: If a line break will be present at the start of the
        logs. Default value is True.
        :type start_line_break: bool
        """
        turn = self.get_message(
            namespace="combat",
            message_group="COMBAT",
            key="turn",
        )

        if start_line_break:
            self.log(message="")

        message = color_string(f"> {turn}: ", intensity="BRIGHT")
        message += color_string(f"{monster.name}", intensity="BRIGHT", underlined=True)
        if monster.suffix:
            message += color_string(
                f" {monster.suffix}", intensity="BRIGHT", underlined=True
            )

        self.log(message=message)
        self.log(message="")

    def log_monster(
        self,
        monster: Monster,
        effect_limit: int = 6,
    ):
        """
        Logs a Monster in combat.

        :param monster: A monster.
        :type monster: Monster

        :param effect_limit: The limit of effects that will be logged. Default value
        is 6.
        :type effect_limit: int
        """
        # Name
        self.log(message=f"> {monster.name}", end="")

        # Suffix
        if monster.suffix:
            self.log(message=f" {monster.suffix}", end="")

        self.log(message=" - ", end="")

        # HP
        self.log(
            message=self.get_message(
                namespace="base",
                message_group="ATTRIBUTES",
                key="hp",
            ),
            end="",
        )
        self.log(message=f": {monster.hp}/{monster.max_hp}", end="")

        # Mana
        if monster.mana > 0:
            self.log(message=" - ", end="")
            self.log(
                message=self.get_message(
                    namespace="base",
                    message_group="ATTRIBUTES",
                    key="mana",
                ),
                end="",
            )
            self.log(message=f": {monster.mana}", end="")

        # Effects
        for idx, effect in enumerate(monster.effects):
            if idx == 0:
                self.log(message=" [ ", end="")
            else:
                self.log(message=" - ", end="")

            if idx < effect_limit:
                self.log(
                    message=self.get_colored_message(
                        namespace="effects",
                        message_group="KEYWORDS",
                        keyword=effect.keyword,
                    ),
                    end="",
                )

                if (
                    effect.keyword
                    in [
                        Keyword.DOOM,
                        Keyword.FREEZE,
                        Keyword.INVISIBLE,
                        Keyword.INVULNERABLE,
                        Keyword.SLEEP,
                        Keyword.STUN,
                        Keyword.TAUNT,
                    ]
                    and effect.duration
                ):
                    self.log(message=f" {effect.duration}", end="")

                elif effect.value:
                    self.log(message=f" {effect.value}", end="")

            else:
                effects_remaining = len(monster.effects) - effect_limit

                message = self.get_message(
                    namespace="base",
                    message_group="WORDS",
                    key="effects",
                ).capitalize()

                message = color_string(
                    f"+{effects_remaining} {message}...",
                    intensity="BRIGHT",
                )
                self.log(message=message, end="")

                self.log(message=" ]", end="")
                break

            if idx == len(monster.effects) - 1:
                self.log(message=" ]", end="")

        self.log("")

    def log_teams(self, teams: List[Team]):
        """
        Logs teams of monsters in combat. Only alive monsters will be logged.

        :param teams: Teams of monsters.
        :type teams: List[Team]
        """
        for team_index, team in enumerate(teams):
            self.log(
                namespace="combat",
                message_group="COMBAT",
                key="team",
                index=team_index + 1,
                team_name=team.name,
            )

            for monster in team.members:
                if monster.is_alive():
                    self.log_monster(monster)

            self.log(message="")
