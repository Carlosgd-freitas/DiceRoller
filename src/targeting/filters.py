"""Filter targets module."""

from __future__ import annotations

from random import choices
from typing import TYPE_CHECKING, Callable, List, Literal

if TYPE_CHECKING:
    from src.base.entity import Entity
    from src.base.keywords import Keyword


def filter(
    entities: List[Entity],
    k: int = 1,
    method: Literal["FIRST", "LAST", "RANDOM"] = "RANDOM",
    sort_function: Callable = None,
    alive: bool = True,
    hurt: bool = False,
    local_id_blacklist: List[str] = None,
    keyword_whitelist: List[Keyword] = None,
    keyword_blacklist: List[Keyword] = None,
) -> List[Entity]:
    """
    Copies and filters a list of entities which meet the criteria.

    :param entities: A list of Entity objects.
    :type entities: List[Entity]

    :param k: The number of entities which will be returned.
    :type k: int

    :param method: The method in which the entities will be picked. Default value is
    "RANDOM".
    :type method: Literal["FIRST", "LAST", "RANDOM"]

    :param sort_function: A function to sort the list of entities.
    :type sort_function: Callable

    :param alive: Whether to consider only alive entities (hp > 0). Default value is
    True.
    :type alive: bool

    :param hurt: Whether to consider only hurt entities (hp < max_hp). Default value is
    False.
    :type hurt: bool

    :param local_id_blacklist: Only entities without any of the specified local_id will
    be returned.
    :type local_id_blacklist: List[str]

    :param keyword_whitelist: Only entities under all effects in this list will be
    returned.
    :type keyword_whitelist: List[Keyword]

    :param keyword_blacklist: Only entities without any effects in this list will be
    returned.
    :type keyword_blacklist: List[Keyword]

    :return: A list of entities which meets the criteria.
    :rtype: List[Entity]
    """
    local_id_blacklist = [] if local_id_blacklist is None else local_id_blacklist
    keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
    keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

    filtered = entities.copy()

    # Sorting
    if sort_function:
        filtered.sort(key=sort_function)

    # Entity attribute conditions
    if alive:
        filtered = [entity for entity in filtered if entity.hp > 0]

    if hurt:
        filtered = [entity for entity in filtered if entity.hp < entity.max_hp]

    # Whitelist and blacklist conditions
    to_remove = []

    for index, entity in enumerate(entities):

        if entity.local_id in local_id_blacklist:
            to_remove.append(index)
            continue

        if not all(entity.get_effect(keyword) for keyword in keyword_whitelist):
            to_remove.append(index)
            continue

        if any(entity.get_effect(keyword) for keyword in keyword_blacklist):
            to_remove.append(index)
            continue

    if to_remove:
        filtered = [
            entity for index, entity in enumerate(entities) if index not in to_remove
        ]

    # Method picking
    if len(filtered) > 0:
        if method == "RANDOM":
            filtered = choices(filtered, k)
        else:
            if method == "LAST":
                filtered.reverse()

            filtered = filtered[:k]

    return filtered
