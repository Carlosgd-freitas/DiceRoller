"""Effect Logger module."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING, Dict, Literal

from src.base.color import Color, color_string
from src.base.keywords import Keyword
from src.logger.logger import Logger

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Monster


class EffectLogger(Logger):
    """
    EffectLogger class.
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

        # Keywords
        for keyword in Keyword:
            kwargs[keyword.name.lower()] = self.get_colored_message(
                namespace="effects",
                message_group="KEYWORDS",
                keyword=keyword,
            )

        # Effect keyword variations
        for parameter, category in [
            ("action", "ACTIONS"),
            ("status", "STATUS"),
            ("keyword", "KEYWORDS"),
        ]:
            kwargs[parameter] = self.get_colored_message(
                namespace="effects",
                message_group=category,
                keyword=effect.keyword,
            )

        # Removed effect
        if kwargs.get("removed_effect"):
            removed_effect: Effect = kwargs["removed_effect"]

            kwargs["removed_keyword"] = self.get_colored_message(
                namespace="effects",
                message_group="KEYWORDS",
                keyword=removed_effect.keyword,
            )

        # Specific attribute
        if kwargs.get("attribute"):
            kwargs["attribute"] = self.get_message(
                namespace="base",
                message_group="ATTRIBUTES",
                key=kwargs["attribute"],
            )

        kwargs.update(
            {
                # Effect parameters
                "duration": effect.duration,
                "value": effect.value,
                "value_perc": ceil(effect.value * 100),
                # General attributes
                "hp": self.get_message(
                    namespace="base", message_group="ATTRIBUTES", key="hp"
                ),
                "mana": self.get_message(
                    namespace="base", message_group="ATTRIBUTES", key="mana"
                ),
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

        self.log(
            namespace="effects", message_group="DAMAGE", key=key, end=" ", **kwargs
        )

        # Part 2: Defensive messages
        if kwargs.get("absorbed_damage"):
            defensive_action = self.get_colored_message(
                namespace="effects",
                message_group="ACTIONS",
                keyword=Keyword.ABSORB,
            )

            self.log(
                namespace="effects",
                message_group="DAMAGE",
                key="absorb",
                end=" ",
                absorbed_damage=kwargs["absorbed_damage"],
                action=defensive_action,
            )

        if kwargs.get("blocked_damage"):
            defensive_action = self.get_colored_message(
                namespace="effects",
                message_group="ACTIONS",
                keyword=Keyword.BLOCK,
            )

            self.log(
                namespace="effects",
                message_group="DAMAGE",
                key="block",
                end=" ",
                blocked_damage=kwargs["blocked_damage"],
                action=defensive_action,
            )

        # Part 3: Damage message
        self.log(
            namespace="effects",
            message_group="DAMAGE",
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
            namespace="effects",
            message_group="ACTIVATION",
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
        if effect.keyword in [Keyword.EXECUTE, Keyword.REVIVE]:
            key = effect.keyword.value.lower()
        else:
            key = effect.type.value.lower()

        # Logging failed effect execution
        if kwargs.get("fail"):
            return self.log_effect_execution_fail(
                effect=effect,
                source=source,
                target=target,
                **kwargs,
            )

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
            namespace="effects",
            message_group="EXECUTION",
            key=key,
            **kwargs,
        )

        return

    def log_effect_execution_fail(
        self,
        effect: Effect,
        source: Monster,
        target: Monster,
        **kwargs,
    ) -> None:
        """
        Logs an effect execution fail.

        :param effect: An Effect.
        :type effect: Effect

        :param source: The Monster which executed the effect.
        :type source: Monster

        :param target: The Monster targeted by the effect execution.
        :type target: Monster
        """
        # Determining logging key
        if effect.keyword in [Keyword.EXECUTE, Keyword.REVIVE]:
            key = effect.keyword.value.lower()
        else:
            key = effect.type.value.lower()

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        if (source) and (target) and (source == target):
            key += "_self"

        # Logging fail base message
        self.log(
            namespace="effects",
            message_group="EXECUTION_FAIL",
            key=key,
            end="",
            **kwargs,
        )
        self.log(message=" ", end="")

        # Logging fail cause
        key = kwargs["fail"]
        if (source) and (target) and (source == target):
            key += "_self"

        self.log(
            namespace="effects",
            message_group="FAILS",
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
            namespace="effects",
            message_group="REMOVAL",
            key=key,
            **kwargs,
        )

        return

    def log_effect_description(
        self,
        effect: Effect,
        params: Literal["name", "value"] = "value",
        **kwargs,
    ) -> None:
        """
        Logs an effect description.

        :param effect: An Effect.
        :type effect: Effect

        :param params: If equal to "value", the effect's parameters values will be used to log.
        If equal to "name", their names inside a <> will be used instead. Default value is "value".
        :type params: Literal["name", "value"]
        """
        kwargs = self._update_log_parameters(effect, **kwargs)

        if params == "name":
            for word, key in [
                ("accuracy", "accuracy"),
                ("decay", "decay"),
                ("duration", "duration"),
                ("value", "value"),
                ("value", "value_perc"),
            ]:
                translated_word = self.get_message(
                    namespace="base", message_group="WORDS", key=word
                )

                kwargs[key] = color_string(
                    f"<{translated_word.upper()}>",
                    foreground_color=Color.WHITE,
                    intensity="BRIGHT",
                )

        key = effect.keyword.value.lower()

        self.log(
            namespace="effects",
            message_group="DESCRIPTION",
            key=key,
            **kwargs,
        )

        return
