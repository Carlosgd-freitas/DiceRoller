"""Effect Manager module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.base.life_state import LifeState
from src.base.triggers import Trigger
from src.logger.effects import EffectLogger
from src.systems.manager import Manager

if TYPE_CHECKING:
    from src.base.entity import Entity
    from src.base.side import Side
    from src.systems.settings import Settings


class EffectManager(Manager):
    """
    EffectManager class.

    :var settings: Game settings.
    :vartype settings: Settings

    :var logging: If logging is enabled. Default value is True.
    :vartype logging: bool
    """

    def __init__(
        self,
        settings: Settings,
        logging: bool = True,
    ):
        # Initialization
        logger = EffectLogger(enabled=logging)

        super().__init__(
            logger,
            settings,
        )

        self.logger: EffectLogger

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
        * BEING_BUFFED
        * BEING_DEBUFFED
        * BEING_DEFENDED
        * BEING_DETERIORATED
        * BEING_ATTACKED
        * BEING_RESTORED

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
            if trigger in [
                Trigger.BEING_BUFFED,
                Trigger.BEING_DEBUFFED,
                Trigger.BEING_DEFENDED,
                Trigger.BEING_DETERIORATED,
                Trigger.BEING_ATTACKED,
                Trigger.BEING_RESTORED,
            ]:
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
        check_source_life_state: bool = True,
        check_target_life_state: bool = True,
        check_can_act: bool = True,
        check_immunity: bool = True,
        check_accuracy: bool = True,
        check_persistable: bool = True,
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

        :param check_source_life_state: If True, checks if the source has the life state
        required by the Effect. Default value is True.
        :type check_source_life_state: bool

        :param check_target_life_state: If True, checks if the target has the life state
        required by the Effect. Default value is True.
        :type check_target_life_state: bool

        :param check_can_act: If True, checks if the source can act. Default value is
        True.
        :type check_can_act: bool

        :param check_immunity: If True, checks if the target is immune to the Effect.
        Default value is True.
        :type check_immunity: bool

        :param check_accuracy: If True, checks if the Effect will hit the target with
        accuracy calculations. Default value is True.
        :type check_accuracy: bool

        :param check_persistable: If True, checks if the Effect can persist in the
        target. Default value is True.
        :type check_persistable: bool

        :return: If the effect was executed.
        :rtype: bool
        """
        fail = None
        requirements = effect.get_requirements()

        # Check source life state
        if (
            check_source_life_state
            and requirements["source_life_state"] != LifeState.ANY
            and requirements["source_life_state"] != source.get_life_state()
        ):
            life_state = source.get_life_state().value.lower()
            fail = f"source_{life_state}"

        # Check if source can act
        if fail is None and check_can_act and (not source.can_act()):
            fail = "act_disabled"

        # Check target immunity
        if fail is None and check_immunity:
            immunity = target.get_effect(Keyword.IMMUNITY)

            if immunity and (
                Keyword.ALL in immunity.target_keywords
                or effect.keyword in immunity.target_keywords
            ):
                if source == target:
                    fail = "source_immunity"
                else:
                    fail = "target_immunity"

        # Check target life state
        if (
            fail is None
            and check_target_life_state
            and requirements["target_life_state"] != LifeState.ANY
            and requirements["target_life_state"] != target.get_life_state()
        ):
            life_state = target.get_life_state().value.lower()
            fail = f"target_{life_state}"

        # Check effect accuracy
        if fail is None and check_accuracy:
            accuracy = effect.accuracy

            # Blind check
            blinded = source.get_effect(Keyword.BLIND)

            if blinded and blinded.get_effective_value() and source != target:
                accuracy -= blinded.get_effective_value()

            # Focus check
            focusing = source.get_effect(Keyword.FOCUS)

            if focusing and focusing.get_effective_value() and focusing.value.percent:
                accuracy += focusing.get_effective_value()

            # Effect miss
            if random() >= accuracy:
                if source == target:
                    fail = "source_miss"
                else:
                    fail = "target_miss"

        # Check Persistable
        if (
            fail is None
            and check_persistable
            and effect.persistent
            and effect.value is not None
            and effect.get_effective_value(source, target) == 0
        ):
            fail = "non-persistable"

        # Procesing effects before effect execution
        for effect_type, trigger in [
            (EffectType.BUFF, Trigger.BUFF),
            (EffectType.DEBUFF, Trigger.DEBUFF),
            (EffectType.DEFENSIVE, Trigger.DEFEND),
            (EffectType.DETERIORATION, Trigger.DETERIORATE),
            (EffectType.OFFENSIVE, Trigger.ATTACK),
            (EffectType.RESTORATION, Trigger.RESTORE),
        ]:
            if effect.type == effect_type:
                self.process_trigger(
                    trigger,
                    source=source,
                    target=target,
                )
                break

        if fail is None:
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

            fail = effect_data.get("fail")

        # Log failed effect execution
        if fail is not None:
            self.logger.log_effect_execution_fail(
                effect=effect,
                source=source,
                target=target,
                fail=fail,
            )
            return False

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

        # Procesing effects after effect execution
        for effect_type, trigger in [
            (EffectType.BUFF, Trigger.BEING_BUFFED),
            (EffectType.DEBUFF, Trigger.BEING_DEBUFFED),
            (EffectType.DEFENSIVE, Trigger.BEING_DEFENDED),
            (EffectType.DETERIORATION, Trigger.BEING_DETERIORATED),
            (EffectType.OFFENSIVE, Trigger.BEING_ATTACKED),
            (EffectType.RESTORATION, Trigger.BEING_RESTORED),
        ]:
            if effect.type == effect_type:
                self.process_trigger(
                    trigger,
                    source=source,
                    target=target,
                )
                break

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
