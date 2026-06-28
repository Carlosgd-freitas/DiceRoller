"""Combat Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from src.base.color import Color, ColorData, color_string
from src.logger.effects import EffectLogger
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
        if not self.enabled:
            return

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
        if not self.enabled:
            return

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
        color_data: ColorData = None,
        effect_limit: int = 5,
    ):
        """
        Logs a Monster in combat.

        :param monster: A monster.
        :type monster: Monster

        :var color_data: Opotional data for coloring parts of the Effect.
        :vartype color_data: ColorData

        :param effect_limit: The limit of effects that will be logged. Default value
        is 5.
        :type effect_limit: int
        """
        if not self.enabled:
            return

        color_data = {} if color_data is None else color_data

        # Name
        message = f"> {monster.name}"

        # Suffix
        if monster.suffix:
            message += f" {monster.suffix}"
        message += " - "

        self.log(
            message=color_string(message, **color_data),
            end="",
        )

        # HP
        self.log(
            message=self.get_message(
                namespace="base",
                message_group="ATTRIBUTES",
                key="hp",
            ),
            end="",
        )

        message = f": {monster.hp}/{monster.max_hp}"
        self.log(
            message=color_string(message, **color_data),
            end="",
        )

        # Mana
        if monster.mana > 0:
            message = " - "
            self.log(
                message=color_string(message, **color_data),
                end="",
            )

            self.log(
                message=self.get_message(
                    namespace="base",
                    message_group="ATTRIBUTES",
                    key="mana",
                ),
                end="",
            )

            message = f": {monster.mana}"
            self.log(
                message=color_string(message, **color_data),
                end="",
            )

        # Effects
        effect_logger = EffectLogger(language=self.language)

        if len(monster.effects) > 0:
            # Start
            self.log(
                message=color_string(" [ ", **color_data),
                end="",
            )

            # Effects themselves
            message = effect_logger.get_multiple_effects_message(
                effects=monster.effects,
                separator=" - ",
                color_data=color_data,
                limit=effect_limit,
            )
            self.log(message, end="")

            # End
            self.log(
                message=color_string(" ]", **color_data),
                end="",
            )

        self.log("")

    def log_monster_death(
        self,
        monster: Monster,
    ):
        """
        Logs a Monster death.

        :param monster: A monster.
        :type monster: Monster
        """
        if not self.enabled:
            return

        message = monster.name

        if monster.suffix:
            message += f" {monster.suffix}"

        message += (
            " "
            + self.get_message(
                namespace="combat",
                message_group="COMBAT",
                key="died",
            )
            + "!"
        )

        self.log(message=message)

    def log_teams(
        self,
        teams: List[Team],
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
    ):
        """
        Logs teams of monsters in combat. Only alive monsters will be logged.

        :param teams: Teams of monsters.
        :type teams: List[Team]

        :param life_state: Whether to consider only alive, dead or any type of entities.
        Default value is "ALIVE".
        :type life_state: Literal["ALIVE", "DEAD", "ANY"]
        """
        if not self.enabled:
            return

        for index, team in enumerate(teams):
            message = self.get_message(
                namespace="combat", message_group="COMBAT", key="team"
            )

            message = color_string(f"{message} #{index+1}", intensity="BRIGHT")
            if team.name:
                message += color_string(f": {team.name}", intensity="BRIGHT")

            self.log(message=message)

            for monster in team.members:
                if life_state in ["ALIVE", "ANY"] and monster.is_alive():
                    self.log_monster(monster, {"foreground_color": None})
                elif life_state in ["DEAD", "ANY"] and not monster.is_alive():
                    self.log_monster(monster, {"foreground_color": Color.GRAY})

            self.log(message="")
