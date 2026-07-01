"""Effect Logger module."""

from __future__ import annotations

from math import ceil, inf
from typing import TYPE_CHECKING, Dict, List, Literal

from src.base.color import Color, ColorData, color_string
from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword, get_keyword
from src.base.monster import Monster
from src.logger.logger import Logger

if TYPE_CHECKING:
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

    def get_effect_message(
        self,
        keyword: Keyword = None,
        effect: Effect = None,
        associated: bool = True,
        color_data: ColorData = None,
    ) -> str:
        """
        Gets a message for an Effect.

        :param keyword: The effect keyword.
        :type keyword: Keyword

        :param effect: An Effect.
        :type effect: Effect

        :param associated: If the associated value or duration will also be logged.
        Default value is True.
        :type associated: bool

        :var color_data: Opotional data for coloring parts of the Effect.
        :vartype color_data: ColorData

        :return: Message containg an effect.
        :rtype: str
        """
        color_data = {} if color_data is None else color_data

        if effect and not keyword:
            keyword = effect.keyword

        message = self.get_colored_message(
            keyword=keyword,
            namespace="effects",
            message_group=keyword.name,
            key="name",
        )

        if effect and associated:
            if (
                effect.keyword
                in [
                    Keyword.DOOM,
                    Keyword.FREEZE,
                    Keyword.INVISIBLE,
                    Keyword.INVULNERABLE,
                    Keyword.REPEL,
                    Keyword.SLEEP,
                    Keyword.STUN,
                    Keyword.TAUNT,
                ]
                and effect.duration
            ):
                message += color_string(f" {effect.duration}", **color_data)

            elif effect.value:
                message += color_string(f" {effect.value}", **color_data)

        return message

    def get_multiple_effects_message(
        self,
        keywords: List[Keyword] = None,
        effects: List[Effect] = None,
        separator: str = ", ",
        associated: bool = True,
        color_data: ColorData = None,
        limit: int = 5,
    ) -> str:
        """
        Gets a message composed by multiple effects.

        :param keywords: The effects keywords.
        :type keywords: List[Keyword]

        :param effects: The effects.
        :type effects: List[Effect]

        :param separator: What string will separate each effect. Default value is ", ".
        :type separator: str

        :param associated: If the associated value or duration will also be logged.
        Default value is True.
        :type associated: bool

        :var color_data: Opotional data for coloring parts of the Effect.
        :vartype color_data: ColorData

        :param limit: The limit of effects that will compose the message. If the amount of effects exceeds
        the limit, "+X Effects..." will be appended at the end of the message. Default value is 5.
        :type limit: int

        :return: Composed message containg multiple effects.
        :rtype: str
        """
        color_data = {} if color_data is None else color_data

        message = ""

        # Less details
        if keywords:
            effects_remaining = len(keywords) - limit

            for idx, keyword in enumerate(keywords[:limit]):
                message += self.get_effect_message(
                    keyword=keyword,
                    associated=associated,
                    color_data=color_data,
                )

                if idx >= limit:
                    break

                if idx != len(keywords[:limit]) - 1:
                    message += color_string(separator, **color_data)

        # More details
        elif effects:
            effects_remaining = len(effects) - limit

            for idx, effect in enumerate(effects[:limit]):
                message += self.get_effect_message(
                    effect=effect,
                    associated=associated,
                    color_data=color_data,
                )

                if idx >= limit:
                    break

                if idx != len(effects[:limit]) - 1:
                    message += color_string(separator, **color_data)

        # Remaining effects message
        if effects_remaining > 0:
            original_intensity = color_data.get("intensity")
            color_data["intensity"] = "BRIGHT"

            lexicon_effect = self.pluralize(
                effects_remaining,
                namespace="base",
                message_group="LEXICON",
                key="effect",
            ).title()

            message += color_string(
                separator + f"+{effects_remaining} {lexicon_effect}...",
                **color_data,
            )

            color_data["intensity"] = original_intensity

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
        # Targeting self
        if source == target:
            kwargs["targeting_self"] = True
        else:
            kwargs["targeting_self"] = False

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
                keyword=keyword,
                namespace="effects",
                message_group=keyword.name,
                key="name",
            )

        # Effect keyword and variations
        for kwargs_key, key in [
            ("action", "action"),
            ("keyword", "name"),
            ("status", "status"),
        ]:
            kwargs[kwargs_key] = self.get_colored_message(
                keyword=effect.keyword,
                namespace="effects",
                message_group=effect.keyword.name,
                key=key,
            )

        # Removed effect
        if kwargs.get("removed_effect"):
            removed_effect: Effect = kwargs["removed_effect"]

            for kwargs_key, key in [
                ("removed_action", "action"),
                ("removed_keyword", "name"),
                ("removed_status", "status"),
            ]:
                kwargs[kwargs_key] = self.get_colored_message(
                    keyword=removed_effect.keyword,
                    namespace="effects",
                    message_group=removed_effect.keyword.name,
                    key=key,
                )

        # Other parameters
        kwargs.update(
            {
                # Effect parameters
                "duration": effect.duration,
                "turns": self.pluralize(
                    effect.duration,
                    namespace="base",
                    message_group="LEXICON",
                    key="turn",
                ),
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
        **kwargs,
    ) -> None:
        """
        Logs multiple messages for damage calculation:
        * Base message: how the damage was done
        * Defensive messages: which deffensive effects took place
        * Damage message: how the damage was recieved
        """
        # Base message
        key = "execution_self" if kwargs["targeting_self"] else "execution"

        message = self.get_message(
            namespace="effects", message_group=effect.keyword.name, key=key, **kwargs
        )

        self.log(message=message, end=" ", **kwargs)

        # Defensive messages
        defended_damage: DefendedDamage = kwargs.get("defended_damage", {})

        for key, value in defended_damage.items():
            if key == "total":
                continue

            defensive_keyword = get_keyword(key)

            # Defensive keyword parameters
            for kwargs_key, key in [
                ("defensive_action", "action"),
                ("defensive_status", "status"),
            ]:
                kwargs[kwargs_key] = self.get_colored_message(
                    keyword=defensive_keyword,
                    namespace="effects",
                    message_group=defensive_keyword.name,
                    key=key,
                )

            kwargs["defended_damage"] = value

            self.log(
                namespace="effects",
                message_group=defensive_keyword.name,
                key="activation",
                end=" ",
                **kwargs,
            )

        # Damage message
        if kwargs.get("damage") and kwargs["damage"] > 0:
            self.log(
                namespace="combat",
                message_group="COMBAT",
                key="damage",
                end=" ",
                **kwargs,
            )

        self.log(message="")

        return

    def _log_countdown_effect(
        self,
        effect: Effect,
        **kwargs,
    ) -> None:
        """
        Logs a message for a countdown effect activation (e.g. Doom).
        """
        key = "countdown" if effect.duration > 0 else "activation"

        self.log(
            namespace="effects", message_group=effect.keyword.name, key=key, **kwargs
        )

        return

    def _log_immunity_effect(
        self,
        effect: ImmunityEffect,
        limit: int = 5,
        **kwargs,
    ) -> None:
        """
        Logs a message for the Immunity effect execution.
        """
        immune_to: List[Keyword] = effect.effects
        count = len(immune_to)
        kwargs["count"] = color_string(
            str(count),
            intensity="BRIGHT",
        )

        # Base message
        key = "execution_self" if kwargs["targeting_self"] else "execution"
        self.log(
            namespace="effects",
            message_group=effect.keyword.name,
            key=key,
            end="",
            **kwargs,
        )

        # Immune to no effects
        if count == 0:
            self.log(message=".")
            return

        # Immune to multiple effects
        message = self.get_multiple_effects_message(
            keywords=immune_to, associated=False, limit=limit
        )
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
        limit: int = 5,
        **kwargs,
    ) -> None:
        """
        Logs a message for effects that removes multiple effects at once (e.g.
        Cleanse an Corrupt).
        """
        removed_effects: List[Effect] = kwargs["removed_effects"]
        count = len(removed_effects)
        kwargs["count"] = color_string(
            str(count),
            intensity="BRIGHT",
        )

        # Base message
        key = "execution_self" if kwargs["targeting_self"] else "execution"
        self.log(
            namespace="effects",
            message_group=effect.keyword.name,
            key=key,
            end="",
            **kwargs,
        )

        # No effects were removed
        if count == 0:
            self.log(message=".")
            return

        # Removed Effects
        message = self.get_multiple_effects_message(
            effects=removed_effects,
            associated=False,
            limit=limit,
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

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        # Specific effect logging
        if effect.keyword in [Keyword.DOOM]:
            return self._log_countdown_effect(
                effect,
                **kwargs,
            )

        # Logging effect activation
        key = "activation_self" if kwargs["targeting_self"] else "activation"

        # Specific message
        message = self.get_message(
            namespace="effects", message_group=effect.keyword.name, key=key, **kwargs
        )

        # Generic message
        if message is None:
            message = self.get_message(
                namespace="effect_types",
                message_group=effect.type.name,
                key=key,
                **kwargs,
            )

        return self.log(message=message)

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

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        # Logging offensive type effect execution
        if effect.type == EffectType.OFFENSIVE:
            return self._log_damage_calculation(
                effect,
                **kwargs,
            )

        # Specific effect logging
        if effect.keyword in [Keyword.CLEANSE, Keyword.CORRUPT]:
            return self._log_multiple_effect_removal(
                effect,
                **kwargs,
            )

        elif effect.keyword in [Keyword.IMMUNITY]:
            return self._log_immunity_effect(
                effect,
                **kwargs,
            )

        # Logging effect execution
        key = "execution_self" if kwargs["targeting_self"] else "execution"

        # Specific message
        message = self.get_message(
            namespace="effects", message_group=effect.keyword.name, key=key, **kwargs
        )

        # Generic message
        if message is None:
            message = self.get_message(
                namespace="effect_types",
                message_group=effect.type.name,
                key=key,
                **kwargs,
            )

        return self.log(message=message)

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

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        key = "execution_fail_self" if kwargs["targeting_self"] else "execution_fail"

        # Specific message
        message = self.get_message(
            namespace="effects", message_group=effect.keyword.name, key=key, **kwargs
        )

        # Generic message
        if message is None:
            message = self.get_message(
                namespace="effect_types",
                message_group=effect.type.name,
                key=key,
                **kwargs,
            )

        self.log(message=message, end=" ")

        # Fail cause message
        key: str = kwargs["fail"]

        for keyword in Keyword:
            if key == keyword.name.lower():
                kwargs["fail_status"] = self.get_colored_message(
                    keyword=keyword,
                    namespace="effects",
                    message_group=keyword.name,
                    key="status",
                )
                break

        key = key + "_self" if kwargs["targeting_self"] else key

        message = self.get_message(
            namespace="combat", message_group="FAILS", key=key, **kwargs
        )

        return self.log(message=message)

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

        kwargs = self._update_log_parameters(effect, source, target, **kwargs)

        removed_effect: Effect = kwargs["removed_effect"]

        message = self.get_message(
            namespace="effects",
            message_group=removed_effect.keyword.name,
            key="removal",
            **kwargs,
        )

        return self.log(message=message)

    def log_effect_description(
        self,
        effect: Effect,
        params: Literal["name", "value"] = "value",
        end: str = "\n",
        **kwargs,
    ) -> None:
        """
        Logs an effect description.

        :param effect: An Effect.
        :type effect: Effect

        :param params: If equal to "value", the effect's parameters values will be used to log.
        If equal to "name", their names inside a <> will be used instead. Default value is "value".
        :type params: Literal["name", "value"]

        :param end: What will be printed at the end of the message. Default value is
        \\n.
        :type end: str
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

        message = self.get_message(
            namespace="effects",
            message_group=effect.keyword.name,
            key="description",
            **kwargs,
        )

        self.log(message=message, end=end)

        return

    def log_effect_details(
        self,
        effect: Effect,
        source: Monster,
    ):
        """
        Logs an Effect details.

        :param effect: An effect.
        :type effect: Effect

        :param source: The Monster which has the effect.
        :type source: Monster
        """
        if not self.enabled:
            return

        # Name
        message = self.get_colored_message(
            keyword=effect.keyword,
            namespace="effects",
            message_group=effect.keyword.name,
            key="name",
        )
        self.log(message=message, end="")

        message = color_string(
            ": ",
            intensity="BRIGHT",
        )
        self.log(message=message, end="")

        # Description
        self.log_effect_description(
            effect=effect,
            params="value",
        )

        # Duration
        message = (
            self.get_message(
                namespace="base",
                message_group="LEXICON",
                key="duration",
            ).title()
            + ": "
        )

        self.log(message=message, end="")

        if effect.duration != inf:
            message = str(effect.duration)
        else:
            message = "∞"

        message += (
            " "
            + self.pluralize(
                effect.duration,
                namespace="base",
                message_group="LEXICON",
                key="turn",
            ).title()
        )

        self.log(message=message)

        return
