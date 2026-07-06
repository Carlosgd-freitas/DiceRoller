"""Entity module."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, List
from uuid import uuid4

from src.base.color import Color, ColorData
from src.base.keywords import Keyword, get_keyword_color
from src.base.text import normalize

if TYPE_CHECKING:
    from src.base.dice import Dice
    from src.base.effect import Effect, EffectData
    from src.base.entity import Entity
    from src.base.side import Side


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
        hp: int = 0,
        max_hp: int = 0,
        speed: int = 0,
        mana: int = 0,
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

    def __str__(self) -> str:
        """String representation of Entity."""
        _str = f"({self.global_id} | {self.local_id})"
        _str = f" {self.name} {self.suffix}"
        _str += f" | HP: {self.hp}/{self.max_hp}"
        _str += f" | Speed: {self.speed}"
        _str += f" | Mana: {self.mana}"

        _str += f"\n>>> Dice ({len(self.dice)}):"
        for one_dice in self.dice:
            _str += f"\n>> {one_dice}\n"

        return _str

    def update_locale_params(self, name: str = None, description: str = None):
        """
        Update parameters that depends on a locale.

        :param name: The entity's name.
        :type name: str

        :param description: The entity's description.
        :type description: str
        .
        """
        if name:
            self.name = name
        if description:
            self.description = description
        return

    def is_alive(self) -> bool:
        """
        Returns if the monster is alive or not.

        :return: If the Monster is alive or not.
        :rtype: bool
        """
        return self.hp > 0

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

    def has_effect(self, keyword: Keyword) -> bool:
        """
        Returns if the entity is currently under the effect.

        :param keyword: A keyword.
        :type keyword: Keyword

        :return: If the entity has the effect.
        :rtype: bool
        """
        for effect in self.effects:
            if effect.keyword == keyword:
                return True
        return False

    def get_effect(self, keyword: Keyword) -> Effect | None:
        """
        Returns an effect from the entity.

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
    ) -> EffectData:
        """
        Add an effect to the Entity, also stacking if the Entity already has an effect
        with that same keyword.

        :param effect: The effect that will be added to the Entity.
        :type effect: Effect

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :return: Data when applying or activating an Effect.
        :rtype: EffectData
        """
        new_effect = deepcopy(effect)
        new_effect.value = new_effect.get_effective_value(source, source)
        current_effect = self.get_effect(effect.keyword)

        # Stack existing effect
        if current_effect:
            current_effect.stack(new_effect)

            effect_data = current_effect.on_apply(
                source,
                self,
            )

        # Add new effect
        else:
            self.effects.append(new_effect)

            effect_data = new_effect.on_apply(
                source,
                self,
            )

        return effect_data

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

    def get_effective_hp(self) -> int:
        """
        Returns the entity' effective hp, taking some effects into account.

        :return: The effective hp.
        :rtype: int
        """
        effective_hp = self.hp

        for keyword in [Keyword.ABSORB, Keyword.BLOCK]:
            effect = self.get_effect(keyword)
            if effect:
                effective_hp += effect.value

        return effective_hp

    def get_effective_speed(self) -> int:
        """
        Returns the entity' effective speed, taking some effects into account.

        :return: The effective speed.
        :rtype: int
        """
        effective_speed = self.speed

        haste = self.get_effect(Keyword.HASTE)
        if haste:
            effective_speed += haste.value

        oil = self.get_effect(Keyword.OIL)
        if oil:
            effective_speed -= oil.value

        slow = self.get_effect(Keyword.SLOW)
        if slow:
            effective_speed -= slow.value

        return effective_speed


def get_attribute_color(attribute: str) -> ColorData:
    """
    Gets an attribute color data.

    :param attribute: An attribute.
    :type attribute: str

    :return: The attribute color data.
    :rtype: ColorData
    """
    attribute = normalize(attribute)

    foreground_color = None
    background_color = None
    intensity = None

    if attribute in ["hp", "max_hp"]:
        foreground_color = Color.RED
    elif attribute in ["speed"]:
        foreground_color = Color.WHITE
        intensity = "BRIGHT"
    elif attribute in ["mana"]:
        return get_keyword_color(Keyword.MANA)

    return {
        "background_color": background_color,
        "foreground_color": foreground_color,
        "intensity": intensity,
    }
