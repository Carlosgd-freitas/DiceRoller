"""Tests for EffectRegistry class."""

from __future__ import annotations

from src.base.keywords import Keyword
from src.registries.effect import REGISTRIES, EffectRegistry
from tests.utils import assert_conditions


def test_effect_registry_integrity():
    EffectRegistry.load()

    conditions = [
        len(REGISTRIES.keys()) > 0,
        REGISTRIES.get("0") is None,
        REGISTRIES.get(Keyword.NOTHING) is not None,
        REGISTRIES.get(Keyword.BURN) is not None,
    ]

    assert_conditions(conditions)
