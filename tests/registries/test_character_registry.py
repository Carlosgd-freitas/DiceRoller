"""Tests for CharacterRegistry class."""

from __future__ import annotations

from src.registries.character import REGISTRIES, CharacterRegistry
from tests.utils import assert_conditions


def test_character_registry_integrity():
    CharacterRegistry.load()

    conditions = [
        len(REGISTRIES.keys()) > 0,
        REGISTRIES.get("0") is None,
        REGISTRIES.get("WARRIOR") is not None,
        REGISTRIES.get("ROGUE") is not None,
    ]

    assert_conditions(conditions)
