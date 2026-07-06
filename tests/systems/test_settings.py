"""Tests for Settings class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.systems.settings import Settings


def test_settings_switch_setting(settings: Settings):
    settings.example = "A"

    settings.switch_setting(
        "example",
        ["A", "B"],
    )

    conditions = [
        settings.example == "B",
    ]

    settings.switch_setting(
        "example",
        ["A", "B"],
    )

    conditions.extend(
        [
            settings.example == "A",
        ]
    )

    assert_conditions(conditions)
