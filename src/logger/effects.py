"""Effect Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Literal

from src.base.color import ColorData, color_string
from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword, get_keyword
from src.base.monster import Monster
from src.base.text import numeric_to_string
from src.logger.stat import StatLogger

if TYPE_CHECKING:
    from src.effects.immunity import ImmunityEffect
    from src.processors.damage import DefendedDamage


class EffectLogger(StatLogger):
    """
    EffectLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _get_effect_params(
        self,
        effect: Effect = None,
        source: Monster = None,
        target: Monster = None,
        **kwargs,
    ) -> Dict:
        """
        Returns common effect parameters for logging.

        :return: Parameters for logging.
        :rtype: Dict
        """
        params = {}

        # Targeting self
        if source == target:
            params["targeting_self"] = True
        else:
            params["targeting_self"] = False

        # Source and target monsters
        if source:
            params["source"] = source.name

            if source.suffix:
                params["source"] += " " + source.suffix

        if target:
            params["target"] = target.name

            if target.suffix:
                params["target"] += " " + target.suffix

        # All keywords
        for keyword in Keyword:
            params[keyword.name.lower()] = self.get_colored_message(
                keyword=keyword,
                namespace="effects",
                message_group=keyword.name,
                key="name",
            )

        # Effect keyword and variations
        for params_key, key in [
            ("action", "action"),
            ("keyword", "name"),
            ("status", "status"),
        ]:
            params[params_key] = self.get_colored_message(
                keyword=effect.keyword,
                namespace="effects",
                message_group=effect.keyword.name,
                key=key,
            )

        # Removed effect
        if kwargs.get("removed_effect"):
            removed_effect: Effect = kwargs["removed_effect"]

            for params_key, key in [
                ("removed_action", "action"),
                ("removed_keyword", "name"),
                ("removed_status", "status"),
            ]:
                params[params_key] = self.get_colored_message(
                    keyword=removed_effect.keyword,
                    namespace="effects",
                    message_group=removed_effect.keyword.name,
                    key=key,
                )

        # Value
        value_flat = None
        value_percent = None

        buffs = None
        debuffs = None

        if effect.value is not None:
            if effect.value.flat is not None:
                value_flat = numeric_to_string(effect.value.flat)

                buffs = self.pluralize(
                    effect.value.flat,
                    namespace="base",
                    message_group="LEXICON",
                    key="buff",
                )

                debuffs = self.pluralize(
                    effect.value.flat,
                    namespace="base",
                    message_group="LEXICON",
                    key="debuff",
                )

            if effect.value.percent is not None:
                value_percent = numeric_to_string(effect.value.percent * 100)

        # Min Value
        min_value_flat = None
        min_value_percent = None

        if effect.min_value is not None:
            if effect.min_value.flat is not None:
                min_value_flat = numeric_to_string(effect.min_value.flat)

            if effect.min_value.percent is not None:
                min_value_percent = numeric_to_string(effect.min_value.percent * 100)

        # Max Value
        max_value_flat = None
        max_value_percent = None

        if effect.max_value is not None:
            if effect.max_value.flat is not None:
                max_value_flat = numeric_to_string(effect.max_value.flat)

            if effect.max_value.percent is not None:
                max_value_percent = numeric_to_string(effect.max_value.percent * 100)

        # Effective value
        effective_value = effect.get_effective_value(source=source, target=target)
        if effective_value is not None:
            effective_value = numeric_to_string(effective_value)

        # Delta
        delta_flat = None
        delta_percent = None

        if effect.delta is not None:
            if effect.delta.flat is not None:
                delta_flat = numeric_to_string(effect.delta.flat)

            if effect.delta.percent is not None:
                delta_percent = numeric_to_string(effect.delta.percent * 100)

        # Duration
        duration = None
        turns = None

        if effect.duration is not None:
            duration = numeric_to_string(effect.duration)
            turns = self.pluralize(
                effect.duration,
                namespace="base",
                message_group="LEXICON",
                key="turn",
            )

        # Accuracy
        accuracy = None

        if effect.accuracy is not None:
            accuracy = numeric_to_string(effect.accuracy * 100)

        # Target Keywords
        target_keywords = None

        if effect.target_keywords is not None:
            target_keywords = self.get_multiple_effects_message(
                keywords=effect.target_keywords
            )

        # Effect params
        params.update(
            {
                "accuracy": color_string(accuracy, intensity="BRIGHT"),
                "delta_flat": color_string(delta_flat, intensity="BRIGHT"),
                "delta_percent": color_string(delta_percent, intensity="BRIGHT"),
                "duration": color_string(duration, intensity="BRIGHT"),
                "effective_value": color_string(effective_value, intensity="BRIGHT"),
                "max_value_flat": color_string(max_value_flat, intensity="BRIGHT"),
                "max_value_percent": color_string(
                    max_value_percent, intensity="BRIGHT"
                ),
                "min_value_flat": color_string(min_value_flat, intensity="BRIGHT"),
                "min_value_percent": color_string(
                    min_value_percent, intensity="BRIGHT"
                ),
                "target_keywords": target_keywords,
                "value_flat": color_string(value_flat, intensity="BRIGHT"),
                "value_percent": color_string(value_percent, intensity="BRIGHT"),
            }
        )

        # Lexicon words
        params.update(
            {
                "buffs": buffs,
                "debuffs": debuffs,
                "turns": turns,
            }
        )

        # Attribute params
        params.update(self._get_attribute_params())

        return params

    def get_effect_name(self, effect: Effect) -> str:
        """
        Gets an effect name.

        :param effect: An effect.
        :type effect: Effect

        :return: Effect name.
        :rtype: str
        """
        name = self.get_message(
            namespace="effects",
            message_group=effect.keyword.name,
            key="name",
        )

        return name

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
            params = self._get_effect_params(effect)

            # Duration-based effects
            if (
                effect.keyword
                in [
                    Keyword.DOOM,
                    Keyword.FREEZE,
                    Keyword.IMMUNITY,
                    Keyword.INVISIBLE,
                    Keyword.INVULNERABLE,
                    Keyword.REPEL,
                    Keyword.SLEEP,
                    Keyword.STUN,
                    Keyword.TAUNT,
                ]
                and effect.duration
            ):
                message += " " + color_string(params["duration"], **color_data)

            # Value-based effects
            elif effect.value and (effect.value.flat or effect.value.percent):
                message += " "

                if not effect.value.flat and not effect.value.percent:
                    message += color_string(params["value_flat"], **color_data)

                elif effect.value.flat and not effect.value.percent:
                    message += color_string(params["value_flat"], **color_data)

                elif not effect.value.flat and effect.value.percent:
                    message += color_string(params["value_percent"] + "%", **color_data)

                else:
                    message += color_string(params["value_flat"] + " + ", **color_data)
                    message += color_string(params["value_percent"] + "%", **color_data)

            # Effects with target keywords
            if (effect.target_keywords) and (Keyword.ALL not in effect.target_keywords):
                keywords = self.get_multiple_effects_message(
                    keywords=effect.target_keywords,
                    associated=False,
                )
                message += color_string(f" [ {keywords} ]", **color_data)

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
        effects_remaining = 0

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
        if kwargs.get("damage") is not None:
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
        immune_to: List[Keyword] = effect.target_keywords
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

        kwargs.update(self._get_effect_params(effect, source, target, **kwargs))

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

        kwargs.update(self._get_effect_params(effect, source, target, **kwargs))

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

        kwargs.update(self._get_effect_params(effect, source, target, **kwargs))

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
        fail: str = kwargs["fail"]
        possible_fail_keyword = fail.removeprefix("source_").removeprefix("target_")

        for keyword in Keyword:
            if possible_fail_keyword == keyword.name.lower():
                kwargs["fail_status"] = self.get_colored_message(
                    keyword=keyword,
                    namespace="effects",
                    message_group=keyword.name,
                    key="status",
                )
                break

        message = self.get_message(
            namespace="combat", message_group="FAILS", key=fail, **kwargs
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

        kwargs.update(self._get_effect_params(effect, source, target, **kwargs))

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
        variation: Literal["static", "variable"] = "static",
        key: str = None,
        end: str = "\n",
        **kwargs,
    ) -> None:
        """
        Logs an effect description.

        :param effect: An Effect.
        :type effect: Effect

        :param variation: If equal to "variable" the effect description that takes its parameters into
        consideration will be logged; if equal to "static", they will not be. Default value is "static".
        :type variation: Literal["static", "variable"]

        :param key: The message key.
        :type key: str

        :param end: What will be printed at the end of the message. Default value is
        \\n.
        :type end: str
        """
        if not self.enabled:
            return

        kwargs.update(self._get_effect_params(effect, **kwargs))

        if (key is None) and (variation == "static"):
            key = "description"
        elif (key is None) and (variation == "variable"):
            key = effect.get_description_variable_key()

        message = self.get_message(
            namespace="effects",
            message_group=effect.keyword.name,
            key=key,
            **kwargs,
        )

        self.log(message=message, end=end)

        return

    def log_effect_details(
        self,
        effect: Effect,
    ):
        """
        Logs an Effect details.

        :param effect: An effect.
        :type effect: Effect
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
            variation="variable",
        )

        # Duration
        if effect.duration is not None:
            message = (
                self.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="duration",
                ).title()
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            self.log(message=message, end="")

            message = numeric_to_string(effect.duration)
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
