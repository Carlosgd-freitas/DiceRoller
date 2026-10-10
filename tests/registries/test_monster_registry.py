"""Tests for MonsterRegistry class."""

from __future__ import annotations

from src.registries.monster import REGISTRIES, MonsterRegistry
from tests.utils import assert_conditions


def test_monster_registry_integrity():
    MonsterRegistry.load()

    conditions = [
        len(REGISTRIES.keys()) > 0,
        REGISTRIES.get("0") is None,
        REGISTRIES.get("SLIME") is not None,
        REGISTRIES.get("TRAINING_DUMMY") is not None,
    ]

    assert_conditions(conditions)
