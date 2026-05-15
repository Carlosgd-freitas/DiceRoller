"""Entity module."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, List, Literal
from uuid import uuid4

from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.dice import Dice
    from src.base.effect import Effect
    from src.base.entity import Entity
    from src.base.side import Side

type stack_method = Literal["add", "overwrite"]


class Entity:
    """
    Entity class.

    :var global_id: All objects of the same Entity subclass will have this same
    identifier.
    :vartype id: str

    :var local_id: Each Entity object will have its own identifier. The default value
    is a generated UUID version 4 in str format.
    :vartype id: str

    :var name: Entity's name.
    :vartype name: str

    :var description: Entity's description.
    :vartype description: str

    :var hp: Entity's current health points.
    :vartype hp: int

    :var max_hp: Entity's maximum health points.
    :vartype max_hp: int

    :var speed: Entity's speed.
    :vartype speed: int

    :var mana: Entity's mana points.
    :vartype mana: int

    :var dice: Entity's dice.
    :vartype dice: List[Dice]

    :var effects: Entity's effects.
    :vartype effects: List[Effect]
    """

    def __init__(
        self,
        global_id: str = None,
        local_id: str = str(uuid4()),
        name: str = None,
        description: str = None,
        hp: int = None,
        max_hp: int = None,
        speed: int = None,
        mana: int = None,
        dice: List[Dice] = None,
        effects: List[Effect] = None,
        **kwargs,
    ):
        self.global_id: str = global_id
        self.local_id: str = local_id

        self.name: str = name
        self.description: str = description

        self.hp: int = hp
        self.max_hp: int = max_hp
        self.speed: int = speed
        self.mana: int = mana

        self.dice: List[Dice] = dice
        self.effects: List[Effect] = effects

        self.dice = [] if dice is None else dice
        self.effects = [] if effects is None else effects

    def roll(self) -> List[Side]:
        """
        Randomly returns list of sides; one for each of this Entity's dice.

        :return: A list of Side objects.
        :rtype: List[Side]
        """
        return [dice.roll() for dice in self.dice]

    def equalize_stats(self) -> None:
        """
        Equalize stats to acceptable values:
        * Entity's HP will be changed to [0, max_hp] interval.
        """
        if self.hp < 0:
            self.hp = 0
        elif self.hp > self.max_hp:
            self.hp = self.max_hp
        return

    def get_effect(self, keyword: Keyword) -> Effect:
        """
        Returns an effect from the entity based on a keyword.

        :param keyword: A keyword.
        :type keyword: Keyword

        :return: An effect.
        :rtype: Effect
        """
        for effect in self.effects:
            if effect.keyword == keyword:
                return effect
        return None

    def apply_effect(
        self,
        effect: Effect,
        source: Entity = None,
        stack_value: stack_method = "overwrite",
        stack_duration: stack_method = "overwrite",
        stack_decay: stack_method = "overwrite",
        stack_accuracy: stack_method = "overwrite",
    ) -> None:
        """
        Add an effect to the Entity, also stacking it by the stacking parameters if the
        Entity already has an effect with that same keyword. Effects with incompatible
        keywords will also be removed from the Entity.

        :param effect: The effect that will be added to the Entity.
        :type effect: Effect

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :param stack_value: How the Effect's value is stacked. By default, this value is
        "overwrite".
        :type stack_value: stack_method

        :param stack_duration: How the Effect's duration is stacked. By default, this
        value is "overwrite".
        :type stack_duration: stack_method

        :param stack_decay: How the Effect's decay is stacked. By default, this value is
        "overwrite".
        :type stack_decay: stack_method

        :param stack_accuracy: How the Effect's accuracy is stacked. By default, this
        value is "overwrite".
        :type stack_accuracy: stack_method

        **Stack Methods**
        * ``add``: if the monster has an existing effect with the same Keyword, the values
        of the existing effect and the new effect for that parameter will be added.

        * ``overwrite``: if the monster has an existing effect with the same Keyword, the
        value of the existing effect will be overwritten by the new effect for that
        parameter.
        """
        current_effect = self.get_effect(effect.keyword)

        # Stack existing effect
        if current_effect:
            for parameter, method in [
                ("value", stack_value),
                ("duration", stack_duration),
                ("decay", stack_decay),
                ("accuracy", stack_accuracy),
            ]:
                current_value = getattr(current_effect, parameter)
                new_value = getattr(effect, parameter)

                if method == "overwrite":
                    setattr(
                        current_effect,
                        parameter,
                        new_value,
                    )

                elif method == "add":
                    current_value = current_value if current_value else 0
                    new_value = new_value if new_value else 0

                    setattr(
                        current_effect,
                        parameter,
                        current_value + new_value,
                    )

        # Add new effect
        else:
            self.effects.append(deepcopy(effect))

        effect.on_apply(
            source,
            self,
        )

        return None

    def remove_effect(
        self,
        keyword: Keyword,
    ) -> Effect:
        """
        Remove an effect from the Entity.

        :param keyword: A keyword.
        :type keyword: Keyword

        :return: The removed effect.
        :rtype: Effect
        """
        effect_to_remove = self.get_effect(keyword)

        if effect_to_remove:
            self.effects.remove(effect_to_remove)

        return effect_to_remove

    def can_act(self) -> bool:
        """
        Returns if the Entity can act.

        :return: If the Entity can act.
        :rtype: bool
        """
        return not any(
            [
                self.get_effect(Keyword.FREEZE),
                self.get_effect(Keyword.SLEEP),
                self.get_effect(Keyword.STUN),
            ]
        )
