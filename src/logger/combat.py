"""Combat Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from tabulate import tabulate

from src.base.color import Color, ColorData, color_string
from src.base.keywords import Keyword
from src.logger.effects import EffectLogger

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.team import Team


class CombatLogger(EffectLogger):
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
        effect_limit: int = 5,
        color_data: ColorData = None,
    ):
        """
        Logs a Monster in combat.

        :param monster: A monster.
        :type monster: Monster

        :param effect_limit: The limit of effects that will be logged. Default value
        is 5.
        :type effect_limit: int

        :var color_data: Optional color data to be used instead of the default.
        :vartype color_data: ColorData
        """
        if not self.enabled:
            return

        color_data = {} if color_data is None else color_data

        # Name
        message = self.get_message(
            namespace="monsters",
            message_group=monster.global_id,
            key="name",
        )
        if message is None:
            message = monster.name

        message = "> " + message

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
        if len(monster.effects) > 0:
            # Start
            self.log(
                message=color_string(" [ ", **color_data),
                end="",
            )

            # Effects themselves
            message = self.get_multiple_effects_message(
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

    def log_monster_details(
        self,
        monster: Monster,
        description: bool = False,
        current_hp: bool = True,
    ):
        """
        Logs a Monster details.

        :param monster: A monster.
        :type monster: Monster

        :param description: If the monster description will be logged. Default value
        is False.
        :type description: bool

        :param current_hp: If True, "hp/max_hp" will be logged, and "max_hp" only
        otherwise. Default value is True.
        :type current_hp: bool
        """
        if not self.enabled:
            return

        # Name
        message = self.get_message(
            namespace="monsters",
            message_group=monster.global_id,
            key="name",
        )
        if message is None:
            message = monster.name

        # Suffix
        if monster.suffix:
            message += f" {monster.suffix}"

        message = color_string(
            message,
            intensity="BRIGHT",
            underlined=True,
        )
        self.log(message=message + "\n")

        # Description
        if description:
            message = self.get_message(
                namespace="monsters",
                message_group=monster.global_id,
                key="description",
            )

            if message:
                self.log(message=message + "\n")

        # Atrributes
        attributes = []

        # HP
        row = []

        message = (
            self.get_message(
                namespace="base",
                message_group="ATTRIBUTES",
                key="hp",
            )
            + ":"
        )

        row.append(message)

        if current_hp:
            message = f"{monster.hp}/{monster.max_hp}"
        else:
            message = f"{monster.max_hp}"

        row.append(message)

        attributes.append(row)

        # Mana
        row = []

        message = (
            self.get_message(
                namespace="base",
                message_group="ATTRIBUTES",
                key="mana",
            )
            + ":"
        )

        row.append(message)

        message = f"{monster.mana}"

        row.append(message)

        attributes.append(row)

        # Speed
        row = []

        message = (
            self.get_message(
                namespace="base",
                message_group="ATTRIBUTES",
                key="speed",
            )
            + ":"
        )

        row.append(message)

        message = f"{monster.get_effective_speed()}"

        if monster.has_effect(Keyword.HASTE):
            message = color_string(message, foreground_color=Color.SPRING_GREEN)
        elif monster.has_effect(Keyword.SLOW):
            message = color_string(message, foreground_color=Color.TOMATO)

        row.append(message)

        attributes.append(row)

        # Logging attributes
        table = tabulate(
            attributes,
            colalign=("right", "left"),
            tablefmt="plain",
        )

        self.log(message=table)

        # Effects
        if len(monster.effects) > 0:
            # Start
            self.log(message="")

            message = (
                self.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="effects",
                ).title()
                + ":"
            )

            message = color_string(
                message,
                intensity="BRIGHT",
            )
            self.log(message=message)

            for effect in monster.effects:
                self.log(message="● ", end="")

                self.log_effect_details(
                    effect=effect,
                    source=monster,
                )

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
                    self.log_monster(monster, color_data={"foreground_color": None})
                elif life_state in ["DEAD", "ANY"] and not monster.is_alive():
                    self.log_monster(
                        monster, color_data={"foreground_color": Color.GRAY}
                    )

            self.log(message="")
