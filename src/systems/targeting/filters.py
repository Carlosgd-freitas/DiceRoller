"""Filter targets module."""

from __future__ import annotations

from math import inf
from random import sample, shuffle
from typing import Callable, List, Literal

from src.base.keywords import Keyword
from src.base.monster import LifeState, Monster


def filter_monsters(
    monsters: List[Monster],
    k: int = 1,
    sort_functions: List[Callable] = None,
    whitelist: List[Monster] = None,
    blacklist: List[Monster] = None,
    keyword_whitelist: List[Keyword] = None,
    keyword_blacklist: List[Keyword] = None,
    ignore_immune_to: List[Keyword] = None,
    life_state: LifeState = LifeState.ALIVE,
    hurt: bool = False,
    consider: List[Keyword] = None,
    method: Literal["FIRST", "LAST", "RANDOM"] = "RANDOM",
) -> List[Monster]:
    """
    Filters a list of monters which meet the criteria.

    :param monsters: A list of monsters.
    :type monsters: List[Monster]

    :param k: The number of monsters which will be returned.
    :type k: int

    :param sort_functions: A list of sort functions.
    :type sort_functions: List[Callable]

    :param whitelist: Only monters that are in this list will be considered.
    :type whitelist: List[Monster]

    :param blacklist: Only monters that aren't in this list will be considered.
    :type blacklist: List[Monster]

    :param keyword_whitelist: Only monsters under all effects in this list will be
    returned.
    :type keyword_whitelist: List[Keyword]

    :param keyword_blacklist: Only monsters without any effects in this list will be
    returned.
    :type keyword_blacklist: List[Keyword]

    :param ignore_immune_to: Only monsters that aren't immune to any of these keywords
    will be returned.
    :type ignore_immune_to: List[Keyword]

    :param life_state: Whether to consider only alive, dead or any type of monsters.
    Default value is LifeState.ALIVE.
    :type life_state: LifeState

    :param hurt: Whether to consider only hurt monsters (hp < max_hp). Default value is
    False.
    :type hurt: bool

    :param consider: A list of target altering effect keywords to be considered when
    filtering. By default, Repel and Taunt effects are considered.
    :type consider: List[Keyword]

    :param method: The method in which the monsters will be picked. Default value is
    "RANDOM".
    :type method: Literal["FIRST", "LAST", "RANDOM"]

    :return: A list of monsters which meets the criteria.
    :rtype: List[Monster]
    """
    # Adjuting default parameters
    sort_functions = [] if sort_functions is None else sort_functions
    whitelist = [] if whitelist is None else whitelist
    blacklist = [] if blacklist is None else blacklist
    keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
    keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist
    ignore_immune_to = [] if ignore_immune_to is None else ignore_immune_to
    consider = [Keyword.REPEL, Keyword.TAUNT] if consider is None else consider

    filtered = monsters.copy()

    # Sorting
    for sort_function in reversed(sort_functions):
        filtered.sort(key=sort_function)

    # Whitelist and blacklist conditions
    to_remove = []

    for index, monster in enumerate(filtered):
        # Monster
        if whitelist and monster not in whitelist:
            to_remove.append(index)
            continue

        if monster in blacklist:
            to_remove.append(index)
            continue

        # Monster effects
        if not all(monster.get_effect(keyword) for keyword in keyword_whitelist):
            to_remove.append(index)
            continue

        if any(monster.get_effect(keyword) for keyword in keyword_blacklist):
            to_remove.append(index)
            continue

        # Avoid immunity
        immunity = monster.get_effect(Keyword.IMMUNITY)
        if immunity and any(
            keyword in immunity.target_keywords for keyword in ignore_immune_to
        ):
            to_remove.append(index)
            continue

    if to_remove:
        filtered = [
            monster for index, monster in enumerate(filtered) if index not in to_remove
        ]

    # Monster attribute conditions
    if life_state == LifeState.ALIVE:
        filtered = [monster for monster in filtered if monster.is_alive()]
    elif life_state == LifeState.DEAD:
        filtered = [monster for monster in filtered if not monster.is_alive()]

    if hurt:
        filtered = [monster for monster in filtered if monster.hp < monster.max_hp]

    # Repel
    if Keyword.REPEL in consider:
        filtered.sort(key=lambda monster: monster.has_effect(Keyword.REPEL))

    # Taunt
    if Keyword.TAUNT in consider:
        filtered.sort(key=lambda monster: not monster.has_effect(Keyword.TAUNT))

    # Method picking
    if len(filtered) > 0:
        if method == "RANDOM":
            if k != inf:
                filtered = sample(filtered, k=min(k, len(filtered)))
            else:
                shuffle(filtered)

        else:
            if method == "LAST":
                filtered.reverse()

            if k != inf:
                filtered = filtered[:k]

    return filtered
