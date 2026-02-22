"""Targets processor module."""

from random import choices
from src.base.side import Side
from src.base.monster import Monster
from src.base.keywords import Keyword
from typing import List, Callable, Literal
from src.base.difficulties import Difficulty


def filter_monsters(
    monsters: List[Monster],
    k: int = 1,
    method: Literal["FIRST", "LAST", "RANDOM"] = "RANDOM",
    sort_function: Callable = None,
    alive: bool = False,
    hurt: bool = False
) -> List[Monster]:
    """
    Returns the first k monsters which meet the criteria among a list of monsters.
    
    :param monsters: A list of Monster objects.
    :type monsters: List[Monster]

    :param k: The number of Monster objects which will be returned.
    :type k: int

    :param method: The method in which the monsters will be picked. Default value is
    "RANDOM".
    :type method: Literal["FIRST", "LAST", "RANDOM"]

    :param sort_function: A function to sort the list of monsters.
    :type sort_function: Callable
    
    :param alive: Whether to consider only alive monsters (hp > 0). Default value is
    False.
    :type alive: bool

    :param hurt: Whether to consider only hurt monsters (hp < max_hp). Default value is
    False.
    :type hurt: bool

    :return: A list of Monster objects which meets the criteria.
    :rtype: List[Monster]
    """
    filtered = monsters.copy()

    if sort_function:
        reverse = False if method == "FIRST" else True
        filtered.sort(
            key=sort_function,
            reverse=reverse
        )

    if alive:
        filtered = [
            monster for monster in filtered
            if monster.hp > 0
        ]

    if hurt:
        filtered = [
            monster for monster in filtered
            if monster.hp < monster.max_hp
        ]

    if len(filtered) > 0:
        if method == "RANDOM":
            filtered = choices(filtered, k)
        else:
            filtered = filtered[:k]

    return filtered


def get_targets(
    current_monster: Monster,
    side: Side,
    k: int = 1,
    current_team: List[Monster] = None,
    enemies: List[Monster] = None,
) -> List[Monster]:
    """
    Returns a list of Monster objects based on the Side keywords.

    :param current_monster: A Monster object, which rolled the Side.
    :type current_monster: List[Monster]

    :param side: A Side object, responsible for the targets that will be chosen.
    :type side: Side

    :param k: The number of Monster objects which will be returned.
    :type k: int

    :param current_team: A list of Monster objects representing the current monster's team.
    :type current_team: List[Monster]

    :param enemies: A list of Monster objects representing the current monsters enemies.
    :type enemies: List[Monster]

    :return: A list of Monster objects which are the targets for the Side processing.
    :rtype: List[Monster]
    """
    difficulty = current_monster.difficulty
    current_team = [] if current_team is None else list(current_team)
    enemies = [] if enemies is None else list(enemies)

    # The targets are chosen based on the Side's first keyword
    effect = side.effects[0]

    if effect.keyword == Keyword.ATTACK:
        if difficulty == Difficulty.EASY:
            return filter_monsters(
                enemies,
                k=k,
                method="LAST",
                sort_function=(lambda x: x.hp),
                alive=True,
            )
        elif difficulty == Difficulty.NORMAL:
            return filter_monsters(
                enemies,
                k=k,
                method="RANDOM",
                alive=True,
            )
        elif difficulty == Difficulty.HARD:
            return filter_monsters(
                enemies,
                k=k,
                method="FIRST",
                sort_function=(lambda x: x.hp),
                alive=True,
            )

    elif effect.keyword in [Keyword.CURSE, Keyword.MANA]:
        return [current_monster]

    elif effect.keyword == Keyword.HEAL:
        if difficulty == Difficulty.EASY:
            return filter_monsters(
                current_team,
                k=k,
                method="LAST",
                sort_function=(lambda x: x.hp),
                hurt=True,
            )
        elif difficulty == Difficulty.NORMAL:
            return filter_monsters(
                current_team,
                k=k,
                method="RANDOM",
                hurt=True,
            )
        elif difficulty == Difficulty.HARD:
            return filter_monsters(
                current_team,
                k=k,
                method="FIRST",
                sort_function=(lambda x: x.hp),
                hurt=True,
            )

    return []
