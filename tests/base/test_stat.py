"""Tests for Stat class."""

from src.base.stat import Stat
from tests.utils import assert_conditions


def test_stat_add():
    stat_0 = Stat(
        flat=1,
        percent=0.2,
    )

    stat_1 = Stat(
        flat=3,
        percent=0.4,
    )

    stat_0.add(stat_1, "flat")
    stat_0.add(stat_1, "percent")

    conditions = [
        stat_0.flat == 4,
        stat_0.percent == 0.6,
    ]

    assert_conditions(conditions)


def test_stat_subtract():
    stat_0 = Stat(
        flat=10,
        percent=0.9,
    )

    stat_1 = Stat(
        flat=3,
        percent=0.4,
    )

    stat_0.subtract(stat_1, "flat")
    stat_0.subtract(stat_1, "percent")

    conditions = [
        stat_0.flat == 7,
        stat_0.percent == 0.5,
    ]

    assert_conditions(conditions)


def test_stat_lowest():
    stat_0 = Stat(
        flat=1,
        percent=0.2,
    )

    stat_1 = Stat(
        flat=3,
        percent=0.4,
    )

    stat_1.lowest(stat_0, "flat")
    stat_1.lowest(stat_0, "percent")

    conditions = [
        stat_1.flat == 1,
        stat_1.percent == 0.2,
    ]

    assert_conditions(conditions)


def test_stat_highest():
    stat_0 = Stat(
        flat=1,
        percent=0.2,
    )

    stat_1 = Stat(
        flat=3,
        percent=0.4,
    )

    stat_0.highest(stat_1, "flat")
    stat_0.highest(stat_1, "percent")

    conditions = [
        stat_0.flat == 3,
        stat_0.percent == 0.4,
    ]

    assert_conditions(conditions)


def test_stat_eq():
    stat_0 = Stat(
        flat=1,
        percent=0.2,
    )

    stat_1 = Stat(
        flat=1,
        percent=0.2,
    )

    stat_2 = Stat(
        flat=3,
        percent=0.4,
    )

    conditions = [
        (stat_0 == stat_1) is True,
        (stat_0 == stat_2) is False,
    ]

    assert_conditions(conditions)
