"""Tests for EffectCompendium class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.effects.attack import AttackEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.compendium.effects import EffectCompendium


def test_effect_compendium_get_item_name(compendiums: Dict):
    compendium: EffectCompendium = compendiums["effect_compendium"]
    effect = AttackEffect()

    name = compendium.get_item_name(effect)

    conditions = [
        name == "ATTACK",
    ]

    assert_conditions(conditions)


def test_effect_compendium_sort_name(compendiums: Dict):
    compendium: EffectCompendium = compendiums["effect_compendium"]

    compendium.sort_menu.sort(
        column_index=1,
        reverse=False,
    )

    sorted = True

    for idx, item in enumerate(compendium.items):
        item: Effect
        item_name = compendium.logger.get_message(
            namespace="effects",
            message_group=item.keyword.name,
            key="name",
        )

        if idx == len(compendium.items) - 2:
            break

        next_item: Effect = compendium.items[idx + 1]
        next_item_name = compendium.logger.get_message(
            namespace="effects",
            message_group=next_item.keyword.name,
            key="name",
        )

        if item_name > next_item_name:
            sorted = False
            break

    conditions = [
        sorted is True,
    ]

    assert_conditions(conditions)


def test_effect_compendium_sort_name_reverse(compendiums: Dict):
    compendium: EffectCompendium = compendiums["effect_compendium"]

    compendium.sort_menu.sort(
        column_index=1,
        reverse=True,
    )

    sorted = True

    for idx, item in enumerate(compendium.items):
        item: Effect
        item_name = compendium.logger.get_message(
            namespace="effects",
            message_group=item.keyword.name,
            key="name",
        )

        if idx == len(compendium.items) - 2:
            break

        next_item: Effect = compendium.items[idx + 1]
        next_item_name = compendium.logger.get_message(
            namespace="effects",
            message_group=next_item.keyword.name,
            key="name",
        )

        if item_name < next_item_name:
            sorted = False
            break

    conditions = [
        sorted is True,
    ]

    assert_conditions(conditions)


def test_effect_compendium_sort_type(compendiums: Dict):
    compendium: EffectCompendium = compendiums["effect_compendium"]

    compendium.sort_menu.sort(
        column_index=2,
        reverse=False,
    )

    sorted = True

    for idx, item in enumerate(compendium.items):
        item: Effect
        item_type = compendium.logger.get_message(
            namespace="effect_types",
            message_group=item.type.name,
            key="name",
        )

        if idx == len(compendium.items) - 2:
            break

        next_item: Effect = compendium.items[idx + 1]
        next_item_type = compendium.logger.get_message(
            namespace="effect_types",
            message_group=next_item.type.name,
            key="name",
        )

        if item_type > next_item_type:
            sorted = False
            break

    conditions = [
        sorted is True,
    ]

    assert_conditions(conditions)


def test_effect_compendium_sort_type_reverse(compendiums: Dict):
    compendium: EffectCompendium = compendiums["effect_compendium"]

    compendium.sort_menu.sort(
        column_index=2,
        reverse=True,
    )

    sorted = True

    for idx, item in enumerate(compendium.items):
        item: Effect
        item_type = compendium.logger.get_message(
            namespace="effect_types",
            message_group=item.type.name,
            key="name",
        )

        if idx == len(compendium.items) - 2:
            break

        next_item: Effect = compendium.items[idx + 1]
        next_item_type = compendium.logger.get_message(
            namespace="effect_types",
            message_group=next_item.type.name,
            key="name",
        )

        if item_type < next_item_type:
            sorted = False
            break

    conditions = [
        sorted is True,
    ]

    assert_conditions(conditions)
