"""Filter targets module."""

from __future__ import annotations

from random import sample
from typing import TYPE_CHECKING, Callable, List, Literal

from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


def filter_entities(
    entities: List[Entity],
    k: int = 1,
    method: Literal["FIRST", "LAST", "RANDOM"] = "RANDOM",
    sort_functions: List[Callable] = None,
    life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
    hurt: bool = False,
    consider: List[Keyword] = None,
    exclude: List[str] = None,
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

    :param sort_functions: A list of functions to sort the list of entities.
    :type sort_functions: List[Callable]

    :param life_state: Whether to consider only alive, dead or any type of entities.
    Default value is "ALIVE".
    :type life_state: Literal["ALIVE", "DEAD", "ANY"]

    :param hurt: Whether to consider only hurt entities (hp < max_hp). Default value is
    False.
    :type hurt: bool

    :param consider: A list of target altering effect keywords to be considered when
    filtering. By default, Repel and Taunt effects are considered.
    :type consider: List[Keyword]

    :param exclude: Only entities without any of the specified local_id will
    be returned.
    :type exclude: List[str]

    :param keyword_whitelist: Only entities under all effects in this list will be
    returned.
    :type keyword_whitelist: List[Keyword]

    :param keyword_blacklist: Only entities without any effects in this list will be
    returned.
    :type keyword_blacklist: List[Keyword]

    :return: A list of entities which meets the criteria.
    :rtype: List[Entity]
    """
    sort_functions = [] if sort_functions is None else sort_functions
    consider = [Keyword.REPEL, Keyword.TAUNT] if consider is None else consider
    exclude = [] if exclude is None else exclude
    keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
    keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

    filtered = entities.copy()

    # Sorting
    for sort_function in reversed(sort_functions):
        filtered.sort(key=sort_function)

    # Repel
    if Keyword.REPEL in consider:
        filtered.sort(key=lambda entity: entity.has_effect(Keyword.REPEL))

    # Taunt
    if Keyword.TAUNT in consider:
        filtered.sort(key=lambda entity: not entity.has_effect(Keyword.TAUNT))

    # Entity attribute conditions
    if life_state == "ALIVE":
        filtered = [entity for entity in filtered if entity.is_alive()]
    elif life_state == "DEAD":
        filtered = [entity for entity in filtered if not entity.is_alive()]

    if hurt:
        filtered = [entity for entity in filtered if entity.hp < entity.max_hp]

    # Whitelist and blacklist conditions
    to_remove = []

    for index, entity in enumerate(filtered):

        if entity.local_id in exclude:
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
            entity for index, entity in enumerate(filtered) if index not in to_remove
        ]

    # Method picking
    if len(filtered) > 0:
        if method == "RANDOM":
            filtered = sample(filtered, k=min(k, len(filtered)))
        else:
            if method == "LAST":
                filtered.reverse()

            filtered = filtered[:k]

    return filtered
