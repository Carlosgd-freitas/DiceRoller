"""Tests for AreaRegistry class."""

from __future__ import annotations

from src.registries.area import AreaRegistry
from tests.utils import assert_conditions


def test_area_registry_integrity():
    REGISTRIES = AreaRegistry.load()

    conditions = [
        len(REGISTRIES.keys()) > 0,
        REGISTRIES.get("0") is None,
        REGISTRIES.get("GRASSLANDS") is not None,
    ]

    assert_conditions(conditions)
