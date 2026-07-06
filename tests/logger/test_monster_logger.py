"""Tests for MonsterLogger class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.monster import Monster
from src.monsters.slime import Slime
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.logger.monster import MonsterLogger


def test_monster_logger_get_monster_name(loggers: Dict):
    monster_logger: MonsterLogger = loggers["monster_logger"]

    monster = Monster()
    name = monster_logger.get_monster_name(monster)

    conditions = [
        name is None,
    ]

    monster.name = "MONSTER"
    name = monster_logger.get_monster_name(monster)

    conditions.extend([name == "MONSTER"])

    slime = Slime()
    slime.suffix = "A"
    name = monster_logger.get_monster_name(slime, suffix=False)

    conditions.extend([name == "Slime"])

    name = monster_logger.get_monster_name(slime, suffix=True)
    conditions.extend([name == "Slime A"])

    assert_conditions(conditions)
