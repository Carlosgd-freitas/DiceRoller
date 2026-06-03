"""Logger module."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING, Dict, List

from src.base.color import color_string
from src.base.keywords import Keyword, get_keyword_color
from src.logger.logger import Logger

if TYPE_CHECKING:
    from src.base.effect import Effect
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

    def _update_log_parameters(
        self,
        effect: Effect = None,
        source: Monster = None,
        target: Monster = None,
        **kwargs,
    ) -> Dict:
        """
        Updates the log parameters with effect, source, target and the data that can be
        derived from that.
        """
        # Source and target monsters
        if source:
            kwargs["source"] = source.name

            if source.suffix:
                kwargs["source"] += " " + source.suffix

        if target:
            kwargs["target"] = target.name

            if target.suffix:
                kwargs["target"] += " " + target.suffix

        # Keyword variations
        for parameter, category in [
            ("action", "ACTIONS"),
            ("status", "STATUS"),
            ("keyword", "KEYWORDS"),
        ]:
            kwargs[parameter] = self.get_colored_message(
                category=category,
                keyword=effect.keyword,
            )

        # Removed effect
        if kwargs.get("removed_effect"):
            removed_effect: Effect = kwargs["removed_effect"]

            kwargs["removed_keyword"] = self.get_colored_message(
                category="KEYWORDS",
                keyword=removed_effect.keyword,
            )

        # Specific attribute
        if kwargs.get("attribute"):
            kwargs["attribute"] = self.get_message(
                category="ATTRIBUTES",
                key=kwargs["attribute"],
            )

        kwargs.update(
            {
                # Effect parameters
                "duration": effect.duration,
                "value": effect.value,
                "value_perc": ceil(effect.value * 100),
                # General attributes
                "hp": self.get_message(category="ATTRIBUTES", key="hp"),
                "mana": self.get_message(category="ATTRIBUTES", key="mana"),
            }
        )

        return kwargs

    def _log_damage_calculation(
        self,
        effect: Effect,
        source: Monster,
        target: Monster,
        **kwargs,
    ) -> None:
        """
        Logs multiple messages for damage calculation:
        * Base message: how the damage was done
        * Defensive messages: which deffensive effects took place
        * Damage message: how the damage was recieved
        """
        # Part 1: Base message
        key = "base"
        if source == target:
            key += "_self"

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        self.log(category="DAMAGE", key=key, end=" ", **kwargs)

        # Part 2: Defensive messages
        if kwargs.get("absorbed_damage"):
            defensive_action = self.get_colored_message(
                category="ACTIONS",
                keyword=Keyword.ABSORB,
            )

            self.log(
                category="DAMAGE",
                key="absorb",
                end=" ",
                absorbed_damage=kwargs["absorbed_damage"],
                action=defensive_action,
            )

        if kwargs.get("blocked_damage"):
            defensive_action = self.get_colored_message(
                category="ACTIONS",
                keyword=Keyword.BLOCK,
            )

            self.log(
                category="DAMAGE",
                key="block",
                end=" ",
                blocked_damage=kwargs["blocked_damage"],
                action=defensive_action,
            )

        # Part 3: Damage message
        self.log(
            category="DAMAGE",
            key="damage",
            **kwargs,
        )

        return

    def log_effect_activation(
        self,
        effect: Effect,
        source: Monster,
        target: Monster,
        **kwargs,
    ) -> None:
        """
        Logs an effect activation.

        :param effect: An Effect.
        :type effect: Effect

        :param source: The Monster which activated the effect.
        :type source: Monster

        :param target: The Monster targeted by the effect activation.
        :type target: Monster
        """
        key = effect.keyword.value.lower()

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        self.log(
            category="EFFECT_ACTIVATION",
            key=key,
            **kwargs,
        )

        return

    def log_effect_execution(
        self,
        effect: Effect,
        source: Monster,
        target: Monster,
        **kwargs,
    ) -> None:
        """
        Logs an effect execution.

        :param effect: An Effect.
        :type effect: Effect

        :param source: The Monster which executed the effect.
        :type source: Monster

        :param target: The Monster targeted by the effect execution.
        :type target: Monster
        """
        # Determining logging key
        if effect.keyword in [Keyword.REVIVE]:
            key = effect.keyword.value.lower()
        else:
            key = effect.type.value.lower()

        # Logging failed effect execution
        if kwargs.get("fail"):
            kwargs = self._update_log_parameters(effect, source, target, **kwargs)

            if (source) and (target) and (source == target):
                key += "_self"

            self.log(
                category="EFFECT_EXECUTION_FAIL",
                key=key,
                end="",
                **kwargs,
            )
            self.log(message=" ", end="")

            key = kwargs["fail"]
            if (source) and (target) and (source == target):
                key += "_self"

            self.log(
                category="FAILS",
                key=key,
                **kwargs,
            )

            return

        # Logging offensive type effect execution
        if key == "offensive":
            self._log_damage_calculation(
                effect,
                source,
                target,
                **kwargs,
            )

            return

        # Logging other effect executions
        if (source) and (target) and (source == target):
            key += "_self"

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        self.log(
            category="EFFECT_EXECUTION",
            key=key,
            **kwargs,
        )

        return

    def log_effect_removal(
        self,
        effect: Effect,
        source: Monster,
        target: Monster,
        **kwargs,
    ) -> None:
        """
        Logs an effect removal.

        :param effect: An Effect.
        :type effect: Effect

        :param source: The Monster which removed the effect.
        :type source: Monster

        :param target: The Monster which had the effect removed.
        :type target: Monster
        """
        removed_effect: Effect = kwargs["removed_effect"]
        key = removed_effect.keyword.value.lower()

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        self.log(
            category="EFFECT_REMOVAL",
            key=key,
            **kwargs,
        )

        return

    def log_round(self, round: int):
        """
        Logs the round start.

        :param round: The round number.
        :type round: int
        """
        self.log(message="\n╔═══════════════╗")
        self.log(
            category="COMBAT",
            key="round",
            round=round,
        )
        self.log(message="╚═══════════════╝")

    def log_turn_start(self, monster: Monster):
        """
        Logs a Monster's turn start in combat.

        :param monster: A monster.
        :type monster: Monster
        """
        turn = self.get_message(
            category="COMBAT",
            key="turn",
        )

        message = color_string(f"\n> {turn}: ", intensity="BRIGHT")
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
                category="ATTRIBUTES",
                key="hp",
            ),
            end="",
        )
        self.log(message=f": {monster.hp}/{monster.max_hp}", end="")

        # Mana
        if monster.mana > 0:
            self.log(message=" - ", end="")
            self.log(
                message=self.get_colored_message(
                    category="KEYWORDS",
                    keyword=Keyword.MANA,
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
                color_data = get_keyword_color(effect.keyword)

                effect_keyword = self.get_message(
                    category="KEYWORDS", key=effect.keyword.value.lower()
                )
                effect_keyword = color_string(
                    effect_keyword,
                    foreground_color=color_data["foreground_color"],
                    intensity=color_data["intensity"],
                )

                self.log(message=effect_keyword, end="")

                self.log(message=f" {effect.value}", end="")

            else:
                effects_remaining = len(monster.effects) - effect_limit

                message = self.get_message(
                    category="ATTRIBUTES",
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
                category="COMBAT", key="team", index=team_index + 1, team_name=team.name
            )

            for monster in team.members:
                if monster.is_alive():
                    self.log_monster(monster)

            self.log(message="")
