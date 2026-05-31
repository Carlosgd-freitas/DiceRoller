"""Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Literal

from src.base.color import color_string
from src.base.keywords import Keyword, get_keyword_color
from src.logger.languages import en_us, pt_br

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Monster

LANGUAGES = {
    "EN-US": en_us,
    "PT-BR": pt_br,
}

type LoggingCategory = Literal[
    "ACTIONS",
    "ATTRIBUTES",
    "COMBAT",
    "DAMAGE",
    "EFFECT_ACTIVATION",
    "EFFECT_EXECUTION",
    "EFFECT_REMOVAL",
    "KEYWORDS",
    "STATUS",
]


class Logger:
    """
    Logger class.

    :var enabled: If the Logger will log the messages. Default value is True.
    :vartype enabled: bool

    :var language: What language will be logged. Default value is "EN-US".
    :vartype language: Literal["EN-US", "PT-BR"]
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
        category: LoggingCategory,
        key: str,
        **kwargs,
    ) -> str | None:
        """
        Gets a message from a language module.

        :param category: The message category.
        :type category: LoggingCategory

        :param key: The message key.
        :type key: str

        :return: A message.
        :rtype: str
        """
        language_module = LANGUAGES[self.language]
        messages: Dict = getattr(language_module, category)
        message: str = messages.get(key)

        if message:
            message = message.format(**kwargs)

        return message

    def _get_colored_message(
        self,
        category: str,
        keyword: Keyword,
    ) -> str | None:
        """
        Returns a colored message based on a Keyword.
        """
        color_data = get_keyword_color(keyword)

        message = color_string(
            self.get_message(
                category=category,
                key=keyword.value.lower(),
            ),
            **color_data,
        )

        return message

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
        if kwargs.get("attribute"):
            kwargs["attribute"] = self.get_message(
                category="ATTRIBUTES",
                key=kwargs["attribute"],
            )

        if source:
            kwargs["source"] = source.name

        if target:
            kwargs["target"] = target.name

        for parameter, category in [
            ("action", "ACTIONS"),
            ("status", "STATUS"),
            ("keyword", "KEYWORDS"),
        ]:
            kwargs[parameter] = self._get_colored_message(
                category=category,
                keyword=effect.keyword,
            )

        if kwargs.get("removed_effect"):
            removed_effect: Effect = kwargs["removed_effect"]

            kwargs["removed_keyword"] = self._get_colored_message(
                category="KEYWORDS",
                keyword=removed_effect.keyword,
            )

        kwargs.update(
            {
                "duration": effect.duration,
                "value": effect.value,
            }
        )

        return kwargs

    def log(
        self,
        message: str = None,
        category: LoggingCategory = None,
        key: str = None,
        end: str = "\n",
        **kwargs,
    ) -> None:
        """
        Logs a message in the output.

        :param message: If a message is passed as a parameter, it will be logged
        directly.
        :type message: str

        :param category: The message category from a language module.
        :type category: LoggingCategory

        :param key: The message key from a language module.
        :type key: str

        :param end: What will be printed at the end of the message. Default value is
        \\n.
        :type end: str
        """
        if not self.enabled:
            return

        if category and key:
            message: str = self.get_message(category, key, **kwargs)

        print(message, end=end)

        return

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
            defensive_action = self._get_colored_message(
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
            defensive_action = self._get_colored_message(
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
        key = effect.type.value.lower()

        if key == "offensive":
            return self._log_damage_calculation(
                effect,
                source,
                target,
                **kwargs,
            )

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

    def log_monster(self, monster: Monster):
        """
        Logs a Monster in combat.

        :param monster: A monster.
        :type monster: Monster
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
                message=self.get_message(
                    category="ATTRIBUTES",
                    key="mana",
                ),
                end="",
            )
            self.log(message=f": {monster.mana}", end="")

        # Effects
        for effect in monster.effects:
            self.log(message=" - ", end="")

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

        self.log("")

    def log_teams(self, teams: List[List[Monster]]):
        """
        Logs teams of Monsters in combat. Only alive monsters (hp > 0) will be logged.

        :param teams: A list where each element is a list of monsters.
        :type teams: List[List[Monster]]
        """
        for team_index, team in enumerate(teams):
            team_name = team[0].team_name
            self.log(
                category="COMBAT", key="team", index=team_index + 1, team_name=team_name
            )

            for monster in team:
                if monster.hp > 0:
                    self.log_monster(monster)

            if team_index < len(teams) - 1:
                self.log(message="")
