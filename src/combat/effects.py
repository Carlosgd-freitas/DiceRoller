"""Effect Manager module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger
from src.logger.effects import EffectLogger

if TYPE_CHECKING:
    from src.base.entity import Entity
    from src.base.side import Side
    from src.effects.immunity import ImmunityEffect
    from src.logger.effects import EffectLogger


class EffectManager:
    """
    Effect Manager class.

    :var logger: A combat logger to log messages for effect management.
    :vartype logger: EffectLogger
    """

    def __init__(
        self,
        logger: EffectLogger,
    ):
        self.logger = logger

    def process_trigger(
        self,
        trigger: Trigger,
        target: Entity,
        source: Entity | None = None,
    ) -> None:
        """
        Activates all effects of a target entity that have the specified trigger type.
        The following triggers will invert the target and source entities on
        activation:
        * BEING_ATTACKED

        :param trigger: A trigger.
        :type trigger: Trigger

        :param target: The entity which will have their effects activated.
        :type target: Entity

        :param source: An optional entity responsible for the effect being triggered.
        :type source: Entity
        """
        if not target:
            return

        for effect in target.effects[:]:

            # Invert target and source monsters
            if trigger == Trigger.BEING_ATTACKED:
                aux = target
                target = source
                source = aux

            if effect.trigger == trigger:
                effect_data = effect.activate(
                    target=target,
                    source=source,
                )

                # Logging triggered effect
                self.logger.log_effect_activation(
                    effect=effect,
                    source=source,
                    target=target,
                    **effect_data,
                )

        return

    def execute_effect(
        self,
        effect: Effect,
        source: Entity,
        target: Entity,
        check_can_act: bool = True,
        check_immunity: bool = True,
        check_accuracy: bool = True,
    ) -> bool:
        """
        Executes an Effect through a series of checks. If the Effect is persistent, it
        will be applied to the target. Otherwise, it will be activated on the target.

        :param effect: An Effect.
        :type effect: Effect

        :param source: The entity where the effect is from.
        :type source: Entity

        :param target: The entity which the effect will be applied.
        :type target: Entity

        :param check_can_act: If True, a check if the source can act will be done
        before trying do activate the Effect. Default value is True.
        :type check_can_act: bool

        :param check_immunity: If True, an immunity check will be done before
        trying do activate the Effect. Default value is True.
        :type check_immunity: bool

        :param check_accuracy: If True, an accuracy check will be done before
        trying do activate the Effect. Default value is True.
        :type check_accuracy: bool

        :return: If the effect was executed.
        :rtype: bool
        """
        # Check can act
        if (check_can_act) and (not source.can_act()):
            return False

        # Check immunity
        if check_immunity:
            immunity: ImmunityEffect = target.get_effect(Keyword.IMMUNITY)

            if immunity and effect.keyword in immunity.effects:
                self.logger.log_effect_execution_fail(
                    effect=effect,
                    source=source,
                    target=target,
                    fail="immunity",
                )
                return False

        # Check accuracy
        if check_accuracy:
            accuracy = effect.accuracy

            # Blind check
            blinded = source.get_effect(Keyword.BLIND)

            if blinded and source != target:
                accuracy -= blinded.value

            # Focus check
            focusing = source.get_effect(Keyword.FOCUS)

            if focusing:
                accuracy += focusing.value

            # Effect miss
            if random() >= accuracy:
                self.logger.log_effect_execution_fail(
                    effect=effect,
                    source=source,
                    target=target,
                    fail="miss",
                )
                return False

        # Persistent effects
        if effect.persistent:
            effect_data = target.apply_effect(
                effect,
                source=source,
            )

        # Instant effects
        else:
            effect_data = effect.activate(
                source=source,
                target=target,
            )

        # Log effect execution
        self.logger.log_effect_execution(
            effect=effect,
            source=source,
            target=target,
            **effect_data,
        )

        # Log effect removals
        if effect.keyword not in [Keyword.CLEANSE, Keyword.CORRUPT]:
            for removed_effect in effect_data.get("removed_effects", []):
                self.logger.log_effect_removal(
                    effect=effect,
                    source=source,
                    target=target,
                    removed_effect=removed_effect,
                )

        # Procesing effects on being attacked
        if effect.type == EffectType.OFFENSIVE:
            self.process_trigger(
                Trigger.BEING_ATTACKED,
                source=source,
                target=target,
            )

        return True

    def roll(self, entity: Entity) -> List[Side]:
        """
        Rolls all Entity's dice and returns the rolled Sides. The entity will be
        affected by Effects that triggers on dice roll.

        :param entity: An Entity.
        :type entity: Entity

        :return: A list containing the rolled Sides.
        :rtype: List[Side]
        """
        rolled = []

        for dice in entity.dice:
            rolled.append(dice.roll())

            # Procesing effects on dice roll
            self.process_trigger(
                Trigger.ROLL,
                target=entity,
            )

        return rolled
