"""Combat Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from src.base.color import Color, ColorData, color_string
from src.base.monster import ControlType, Monster
from src.logger.monster import MonsterLogger

if TYPE_CHECKING:
    from src.combat.team import Team


class CombatLogger(MonsterLogger):
    """
    CombatLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def log_round_start(self, round: int, start_line_break: bool = True):
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
        message += color_string(
            self.get_monster_name(monster), intensity="BRIGHT", underlined=True
        )

        self.log(message=message)
        self.log(message="")

    def log_monster(
        self,
        monster: Monster,
        control_type: bool = False,
        effect_limit: int = 5,
        color_data: ColorData = None,
    ):
        """
        Logs a Monster in combat.

        :param monster: A monster.
        :type monster: Monster

        :param control_type: If the monster control type will be logged. Default
        value is False.
        :type control_type: bool

        :param effect_limit: The limit of effects that will be logged. Default value
        is 5.
        :type effect_limit: int

        :var color_data: Optional color data to be used instead of the default.
        :vartype color_data: ColorData
        """
        if not self.enabled:
            return

        color_data = {} if color_data is None else color_data
        attribute_params = self._get_attribute_params()

        # Name + Suffix
        message = "> " + self.get_monster_name(monster) + " - "

        self.log(
            message=color_string(message, **color_data),
            end="",
        )

        # Control Type
        if control_type:
            if monster.control_type == ControlType.AI:
                message = self.get_message(
                    namespace="combat",
                    message_group="COMBAT",
                    key=monster.control_type.name.lower(),
                )

                foreground_color = Color.RED

            elif monster.control_type == ControlType.PLAYER:
                message = self.get_message(
                    namespace="combat",
                    message_group="COMBAT",
                    key=monster.control_type.name.lower(),
                )

                foreground_color = Color.BLUE

            message = (
                color_string(
                    message,
                    foreground_color=foreground_color,
                    intensity="BRIGHT",
                )
                + " - "
            )

            self.log(
                message=message,
                end="",
            )

        # HP
        self.log(
            message=attribute_params["hp"],
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
                message=attribute_params["mana"],
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

        message = self.get_monster_name(monster)

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

    def log_turn_skip(self, monster: Monster):
        """
        Logs a monster skipping its turn.

        :param monster: A monster.
        :type monster: Monster
        """
        if not self.enabled:
            return

        name = self.get_monster_name(monster)

        message = self.get_message(
            namespace="combat",
            message_group="ACTIONS",
            key="skip_turn",
            name=name,
        )

        self.log(message=message)

        return

    def log_teams(
        self,
        teams: List[Team],
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
        control_type: bool = False,
    ):
        """
        Logs teams of monsters in combat. Only alive monsters will be logged.

        :param teams: Teams of monsters.
        :type teams: List[Team]

        :param life_state: Whether to consider only alive, dead or any type of entities.
        Default value is "ALIVE".
        :type life_state: Literal["ALIVE", "DEAD", "ANY"]

        :param control_type: If the monsters control type will be logged. Default
        value is False.
        :type control_type: bool
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
                    self.log_monster(
                        monster,
                        control_type=control_type,
                        color_data={"foreground_color": None},
                    )
                elif life_state in ["DEAD", "ANY"] and not monster.is_alive():
                    self.log_monster(
                        monster,
                        control_type=control_type,
                        color_data={"foreground_color": Color.GRAY},
                    )

            self.log(message="")
