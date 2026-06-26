"""Effect Logger module."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING, Dict, List, Literal

from src.base.color import Color, color_string
from src.base.keywords import Keyword, get_keyword
from src.logger.logger import Logger

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Monster
    from src.effects.immunity import ImmunityEffect
    from src.processors.damage import DefendedDamage


class EffectLogger(Logger):
    """
    EffectLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def get_multiple_effects_message(
        self,
        keywords: List[Keyword] = None,
        effects: List[Effect] = None,
        limit: int = 3,
    ) -> str:
        """
        Gets a message composed by multiple effects. If the number of composing effects
        is:
        * 1, the message will be its colored keyword.
        * 2 or more, the message will be their colored keywords separated by ",".

        :param keywords: The effects keywords.
        :type keywords: List[Keyword]

        :param effects: The effects.
        :type effects: List[Effect]

        :param limit: The limit of effects that will compose the message. If the amount of effects exceeds
        the limit, "+X Effects..." will be appended at the end of the message. Default value is 3.
        :type limit: int

        :return: Composed message containg multiple effects.
        :rtype: str
        """
        if effects:
            keywords = [effect.keyword for effect in effects]
        elif keywords is None:
            keywords = []

        effects_remaining = len(keywords) - limit

        # Multiple effects message
        keywords = keywords[:limit]
        keywords = [
            self.get_colored_message(
                namespace="effects", message_group="KEYWORDS", keyword=keyword
            )
            for keyword in keywords
        ]

        message = ", ".join(keywords)

        # Remaining effects message
        if effects_remaining > 0:
            effect_word = self.get_message(
                namespace="base",
                message_group="LEXICON",
                key="effects",
            ).capitalize()

            message += ", " + color_string(
                f"+{effects_remaining} {effect_word}...",
                intensity="BRIGHT",
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
        # Source and target monsters
        if source:
            kwargs["source"] = source.name

            if source.suffix:
                kwargs["source"] += " " + source.suffix

        if target:
            kwargs["target"] = target.name

            if target.suffix:
                kwargs["target"] += " " + target.suffix

        # All keywords
        for keyword in Keyword:
            kwargs[keyword.name.lower()] = self.get_colored_message(
                namespace="effects",
                message_group="KEYWORDS",
                keyword=keyword,
            )

        # Effect keyword and variations
        for parameter, category in [
            (effect.keyword.name.lower(), "KEYWORDS"),
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

        # Other parameters
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
        defended_damage: DefendedDamage = kwargs.get("defended_damage", {})

        for key, value in defended_damage.items():
            if key == "total":
                continue

            defensive_keyword = get_keyword(key)

            # Defensive keyword parameters
            for parameter, category in [
                ("action", "ACTIONS"),
                ("status", "STATUS"),
            ]:
                kwargs[parameter] = self.get_colored_message(
                    namespace="effects",
                    message_group=category,
                    keyword=defensive_keyword,
                )

            kwargs["defended_damage"] = value

            self.log(
                namespace="effects",
                message_group="DAMAGE",
                key=key,
                end=" ",
                **kwargs,
            )

        # Part 3: Damage message
        if kwargs.get("damage") and kwargs["damage"] > 0:
            self.log(
                namespace="effects",
                message_group="DAMAGE",
                key="damage",
                end=" ",
                **kwargs,
            )

        self.log(message="")

        return

    def _log_countdown_effect(
        self,
        effect: Effect,
        source: Monster,
        target: Monster,
        **kwargs,
    ) -> None:
        """
        Logs a message for a countdown effect activation (e.g. Doom).
        """
        key = effect.keyword.name.lower()

        if effect.duration > 0:
            key += "_countdown"

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        self.log(namespace="effects", message_group="ACTIVATION", key=key, **kwargs)

        return

    def _log_immunity_effect(
        self,
        effect: ImmunityEffect,
        source: Monster,
        target: Monster,
        limit: int = 3,
        **kwargs,
    ) -> None:
        """
        Logs a message for the Immunity effect execution.
        """
        # Base message
        key = effect.keyword.name.lower()
        if source == target:
            key += "_self"

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        immune_to: List[Keyword] = effect.effects
        count = len(immune_to)
        kwargs["count"] = color_string(
            str(count),
            intensity="BRIGHT",
        )

        self.log(
            namespace="effects", message_group="EXECUTION", key=key, end="", **kwargs
        )

        # Immune to no effects
        if count == 0:
            self.log(message=".")
            return

        # Immune to multiple effects
        message = self.get_multiple_effects_message(keywords=immune_to, limit=limit)
        self.log(message=": " + message, end="")

        # Message ending
        if count > limit:
            self.log(message="")

        else:
            self.log(message=".")

        return

    def _log_multiple_effect_removal(
        self,
        effect: Effect,
        source: Monster,
        target: Monster,
        limit: int = 3,
        **kwargs,
    ) -> None:
        """
        Logs a message for effects that removes multiple effects at once (e.g.
        Cleanse an Corrupt).
        """
        # Base message
        key = effect.keyword.name.lower()
        if source == target:
            key += "_self"

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        removed_effects: List[Effect] = kwargs["removed_effects"]
        count = len(removed_effects)
        kwargs["count"] = color_string(
            str(count),
            intensity="BRIGHT",
        )

        self.log(
            namespace="effects", message_group="EXECUTION", key=key, end="", **kwargs
        )

        # No effects were removed
        if count == 0:
            self.log(message=".")
            return

        # Removed Effects
        message = self.get_multiple_effects_message(
            effects=removed_effects, limit=limit
        )
        self.log(message=": " + message, end="")

        # Message ending
        if count > limit:
            self.log(message="")

        else:
            self.log(message=".")

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
        if not self.enabled:
            return

        key = effect.keyword.value.lower()

        if effect.keyword == Keyword.DOOM:
            return self._log_countdown_effect(
                effect,
                source,
                target,
                **kwargs,
            )

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        return self.log(
            namespace="effects",
            message_group="ACTIVATION",
            key=key,
            **kwargs,
        )

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
        if not self.enabled:
            return

        # Determining logging key
        message_group = self.get_message_group(
            namespace="effects", message_group="EXECUTION"
        )

        if effect.keyword.name.lower() in message_group.keys():
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
            return self._log_damage_calculation(
                effect,
                source,
                target,
                **kwargs,
            )

        # Specific effect logging
        if effect.keyword in [Keyword.CLEANSE, Keyword.CORRUPT]:
            return self._log_multiple_effect_removal(
                effect,
                source,
                target,
                **kwargs,
            )

        elif effect.keyword == Keyword.IMMUNITY:
            return self._log_immunity_effect(
                effect,
                source,
                target,
                **kwargs,
            )

        # Logging other effect executions
        if (source) and (target) and (source == target):
            key += "_self"

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        return self.log(
            namespace="effects",
            message_group="EXECUTION",
            key=key,
            **kwargs,
        )

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
        if not self.enabled:
            return

        # Determining logging key
        message_group = self.get_message_group(
            namespace="effects", message_group="EXECUTION_FAIL"
        )

        if effect.keyword.name.lower() in message_group.keys():
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

        for keyword in Keyword:
            if key == keyword.name.lower():
                kwargs["status"] = self.get_colored_message(
                    namespace="effects",
                    message_group="STATUS",
                    keyword=keyword,
                )
                break

        if (source) and (target) and (source == target):
            key += "_self"

        return self.log(
            namespace="effects",
            message_group="FAILS",
            key=key,
            **kwargs,
        )

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
        if not self.enabled:
            return

        removed_effect: Effect = kwargs["removed_effect"]
        key = removed_effect.keyword.value.lower()

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        return self.log(
            namespace="effects",
            message_group="REMOVAL",
            key=key,
            **kwargs,
        )

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
        if not self.enabled:
            return

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
                    namespace="base", message_group="LEXICON", key=word
                )

                kwargs[key] = color_string(
                    f"<{translated_word.upper()}>",
                    foreground_color=Color.WHITE,
                    intensity="BRIGHT",
                )

        key = effect.keyword.value.lower()

        return self.log(
            namespace="effects",
            message_group="DESCRIPTION",
            key=key,
            **kwargs,
        )
