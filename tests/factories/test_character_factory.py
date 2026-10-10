"""Tests for CharacterFactory class."""

from __future__ import annotations

from src.characters.warrior import Warrior
from src.factories.character import CharacterFactory
from tests.utils import assert_conditions


def test_character_factory_create_simple():
    character = CharacterFactory.create("WARRIOR")

    conditions = [
        isinstance(character, Warrior),
        character.global_id == "WARRIOR",
    ]

    assert_conditions(conditions)


def test_character_factory_create_args():
    character = CharacterFactory.create(
        "WARRIOR",
        local_id="WARRIOR_0",
    )

    conditions = [
        isinstance(character, Warrior),
        character.global_id == "WARRIOR",
        character.local_id == "WARRIOR_0",
    ]

    assert_conditions(conditions)
