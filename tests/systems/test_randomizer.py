"""Tests for Randomizer class."""

from __future__ import annotations

from math import inf, isclose

from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.combat.manager import OrderStrategy
from src.systems.randomizer import Randomizer, RandomizerConfig
from tests.utils import assert_conditions


def test_random_int(randomizer: Randomizer):
    value_0 = randomizer.random_int([1, 6], cap=[-999, 999])
    value_1 = randomizer.random_int([-inf, 6], cap=[-999, 999])
    value_2 = randomizer.random_int([1, inf], cap=[-999, 999])

    conditions = [
        value_0 in range(1, 7),
        value_1 in range(-999, 7),
        value_2 in range(1, 999),
    ]

    assert_conditions(conditions)


def test_random_float(randomizer: Randomizer):
    value_0 = randomizer.random_float([0.1, 1])
    value_1 = randomizer.random_float([-inf, 1])
    value_2 = randomizer.random_float([0.1, inf])

    conditions = [
        value_0 >= 0.1,
        value_0 <= 1,
        value_1 == -inf,
        value_2 == inf,
    ]

    assert_conditions(conditions)


def test_get_random_keyword(randomizer: Randomizer):
    config = RandomizerConfig(
        keyword_whitelist=[Keyword.BLOCK],
    )

    keyword_0 = randomizer.get_random_keyword(config)

    conditions = [
        keyword_0 == Keyword.BLOCK,
    ]

    config = RandomizerConfig(
        keyword_blacklist=[Keyword.DOOM],
    )

    keyword_1 = randomizer.get_random_keyword(config)

    conditions.extend(
        [
            keyword_1 != Keyword.DOOM,
        ]
    )

    assert_conditions(conditions)


def test_get_random_stat(randomizer: Randomizer):
    config = RandomizerConfig(
        flat_threshold=(1, 10),
        percent_threshold=(0.1, 0.2),
    )

    stat_0 = randomizer.get_random_stat(config)

    conditions = [
        stat_0.flat in range(1, 20),
        stat_0.percent >= 0.1,
        stat_0.percent <= 0.2,
    ]

    assert_conditions(conditions)


def test_get_random_effect(randomizer: Randomizer):
    config = RandomizerConfig(
        value_flat_threshold=(1, 6),
        value_percent_threshold=(0.01, 0.1),
        accuracy_threshold=(0.8, 1),
        effect_type=EffectType.OFFENSIVE,
    )

    effect_0 = randomizer.get_random_effect(config)

    conditions = [
        effect_0.type == EffectType.OFFENSIVE,
        effect_0.value.flat in range(1, 7),
        effect_0.value.percent >= 0.01,
        effect_0.value.percent <= 0.1,
        effect_0.duration is None,
        effect_0.delta is None,
        effect_0.accuracy >= 0.8,
        effect_0.accuracy <= 1,
    ]

    config = RandomizerConfig(
        value_flat_threshold=(2, 2),
        value_percent_threshold=(0.02, 0.02),
        min_value_flat_threshold=(1, 1),
        min_value_percent_threshold=(0.01, 0.01),
        max_value_flat_threshold=(3, 3),
        max_value_percent_threshold=(0.03, 0.03),
        duration_threshold=(4, 4),
        delta_flat_threshold=(5, 5),
        delta_percent_threshold=(0.05, 0.05),
        accuracy_threshold=(0.6, 0.6),
        target_keywords_threshold=(7, 7),
        keyword_whitelist=[Keyword.BURN],
    )

    effect_1 = randomizer.get_random_effect(config)

    conditions.extend(
        [
            effect_1.keyword == Keyword.BURN,
            effect_1.value.flat == 2,
            isclose(effect_1.value.percent, 0.02),
            effect_1.min_value.flat == 1,
            isclose(effect_1.min_value.percent, 0.01),
            effect_1.max_value.flat == 3,
            isclose(effect_1.max_value.percent, 0.03),
            effect_1.duration == 4,
            effect_1.delta.flat == 5,
            isclose(effect_1.delta.percent, 0.05),
            isclose(effect_1.accuracy, 0.6),
            effect_1.target_keywords is None,
        ]
    )

    config = RandomizerConfig(
        duration_threshold=(3, 4),
        accuracy_threshold=(0.9, 1),
        target_keywords_threshold=(1, 3),
        keyword_whitelist=[Keyword.IMMUNITY],
    )

    effect_2 = randomizer.get_random_effect(config)

    conditions.extend(
        [
            effect_2.keyword == Keyword.IMMUNITY,
            effect_2.value is None,
            effect_2.min_value is None,
            effect_2.max_value is None,
            effect_2.duration in range(3, 5),
            effect_2.delta is None,
            effect_2.accuracy >= 0.9,
            effect_2.accuracy <= 1,
            len(effect_2.target_keywords) in range(1, 4),
        ]
    )

    assert_conditions(conditions)


def test_get_random_side(randomizer: Randomizer):
    config = RandomizerConfig(
        effect_threshold=(1, 3),
    )

    side = randomizer.get_random_side(config)

    same_type = True
    effect_type = side.effects[0].type

    for effect in side.effects:
        if effect.type != effect_type:
            same_type = False
            break

    conditions = [
        len(side.effects) in range(1, 4),
        same_type is True,
    ]

    assert_conditions(conditions)


def test_get_random_dice(randomizer: Randomizer):
    config = RandomizerConfig(
        side_threshold=(8, 10),
    )

    dice_0 = randomizer.get_random_dice(config)

    conditions = [
        len(dice_0.sides) in range(8, 11),
    ]

    config = RandomizerConfig(
        side_threshold=(2, 2),
        effect_threshold=(1, 1),
        value_flat_threshold=(4, 4),
        value_percent_threshold=(0.04, 0.04),
        min_value_flat_threshold=(3, 3),
        min_value_percent_threshold=(0.03, 0.03),
        max_value_flat_threshold=(5, 5),
        max_value_percent_threshold=(0.05, 0.05),
        duration_threshold=(6, 6),
        delta_flat_threshold=(7, 7),
        delta_percent_threshold=(0.07, 0.07),
        accuracy_threshold=(0.8, 0.8),
        target_keywords_threshold=(9, 9),
        keyword_whitelist=[Keyword.BURN],
    )

    dice_1 = randomizer.get_random_dice(config)

    conditions.extend(
        [
            len(dice_1.sides) == 2,
            all([len(side.effects) == 1 for side in dice_1.sides]),
            all(
                [
                    effect.keyword == Keyword.BURN
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.value.flat == 4
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    isclose(effect.value.percent, 0.04)
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.min_value.flat == 3
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    isclose(effect.min_value.percent, 0.03)
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.max_value.flat == 5
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    isclose(effect.max_value.percent, 0.05)
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.duration == 6
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.delta.flat == 7
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    isclose(effect.delta.percent, 0.07)
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    isclose(effect.accuracy, 0.8)
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.target_keywords is None
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
        ]
    )

    assert_conditions(conditions)


def test_get_random_monster_name(randomizer: Randomizer):
    name = randomizer.get_random_monster_name()

    conditions = [
        isinstance(name, str),
    ]

    assert_conditions(conditions)


def test_get_random_monster(randomizer: Randomizer):
    config = RandomizerConfig(
        hp_threshold=(80, 100),
        mana_threshold=(20, 30),
        speed_threshold=(10, 15),
        dice_threshold=(2, 4),
    )

    monster_0 = randomizer.get_random_monster(config)

    conditions = [
        isinstance(monster_0.name, str),
        monster_0.hp in range(80, 101),
        monster_0.max_hp == monster_0.hp,
        monster_0.mana in range(20, 31),
        monster_0.speed in range(10, 16),
        len(monster_0.dice) in range(2, 5),
    ]

    config = RandomizerConfig(
        hp_threshold=(11, 11),
        mana_threshold=(12, 12),
        speed_threshold=(13, 13),
        dice_threshold=(2, 2),
        side_threshold=(1, 1),
        effect_threshold=(3, 3),
        effect_type=EffectType.DEBUFF,
        value_flat_threshold=(5, 5),
        value_percent_threshold=(0.05, 0.05),
        min_value_flat_threshold=(4, 4),
        min_value_percent_threshold=(0.04, 0.04),
        max_value_flat_threshold=(6, 6),
        max_value_percent_threshold=(0.06, 0.06),
        duration_threshold=(7, 7),
        delta_flat_threshold=(8, 8),
        delta_percent_threshold=(0.08, 0.08),
        accuracy_threshold=(0.9, 0.9),
        target_keywords_threshold=(10, 10),
    )

    monster_1 = randomizer.get_random_monster(config)

    conditions.extend(
        [
            monster_1.hp == 11,
            monster_1.max_hp == monster_1.hp,
            monster_1.mana == 12,
            monster_1.speed == 13,
            len(monster_1.dice) == 2,
            all([len(dice.sides) == 1 for dice in monster_1.dice]),
            all(
                [
                    len(side.effects) == 3
                    for dice in monster_1.dice
                    for side in dice.sides
                ]
            ),
            all(
                [
                    effect.type == EffectType.DEBUFF
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.value is None
                        or effect.value.flat is None
                        or effect.value.flat == 5
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.value is None
                        or effect.value.percent is None
                        or isclose(effect.value.percent, 0.05)
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.min_value is None
                        or effect.min_value.flat is None
                        or effect.min_value.flat == 4
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.min_value is None
                        or effect.min_value.percent is None
                        or isclose(effect.min_value.percent, 0.04)
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.max_value is None
                        or effect.max_value.flat is None
                        or effect.max_value.flat == 6
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.max_value is None
                        or effect.max_value.percent is None
                        or isclose(effect.max_value.percent, 0.06)
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.duration == 7
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.delta is None
                        or effect.delta.flat is None
                        or effect.delta.flat == 8
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.delta is None
                        or effect.delta.percent is None
                        or isclose(effect.delta.percent, 0.08)
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    isclose(effect.accuracy, 0.9)
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.target_keywords is None
                        or len(effect.target_keywords) <= 10
                    )
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
        ]
    )

    assert_conditions(conditions)


def test_get_random_team_name(randomizer: Randomizer):
    name = randomizer.get_random_team_name()

    conditions = [
        isinstance(name, str),
    ]

    assert_conditions(conditions)


def test_get_random_team(randomizer: Randomizer):
    config = RandomizerConfig(
        member_threshold=(2, 4),
    )

    team_0 = randomizer.get_random_team(config)

    conditions = [
        len(team_0.members) in range(2, 5),
    ]

    config = RandomizerConfig(
        member_threshold=(2, 2),
        hp_threshold=(12, 12),
        mana_threshold=(13, 13),
        speed_threshold=(14, 14),
        dice_threshold=(1, 1),
        side_threshold=(3, 3),
        effect_threshold=(4, 4),
        effect_type=EffectType.BUFF,
        value_flat_threshold=(6, 6),
        value_percent_threshold=(0.06, 0.06),
        min_value_flat_threshold=(5, 5),
        min_value_percent_threshold=(0.05, 0.05),
        max_value_flat_threshold=(7, 7),
        max_value_percent_threshold=(0.07, 0.07),
        duration_threshold=(8, 8),
        delta_flat_threshold=(9, 9),
        delta_percent_threshold=(0.09, 0.09),
        accuracy_threshold=(0.1, 0.1),
        target_keywords_threshold=(11, 11),
    )

    team_1 = randomizer.get_random_team(config)

    conditions.extend(
        [
            len(team_1.members) == 2,
            all([monster.hp == 12 for monster in team_1.members]),
            all([monster.max_hp == monster.hp for monster in team_1.members]),
            all([monster.mana == 13 for monster in team_1.members]),
            all([monster.speed == 14 for monster in team_1.members]),
            all([len(monster.dice) == 1 for monster in team_1.members]),
            all(
                [
                    len(dice.sides) == 3
                    for monster in team_1.members
                    for dice in monster.dice
                ]
            ),
            all(
                [
                    len(side.effects) == 4
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                ]
            ),
            all(
                [
                    effect.type == EffectType.BUFF
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.value is None
                        or effect.value.flat is None
                        or effect.value.flat == 6
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.value is None
                        or effect.value.percent is None
                        or isclose(effect.value.percent, 0.06)
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.min_value is None
                        or effect.min_value.flat is None
                        or effect.min_value.flat == 5
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.min_value is None
                        or effect.min_value.percent is None
                        or isclose(effect.min_value.percent, 0.05)
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.max_value is None
                        or effect.max_value.flat is None
                        or effect.max_value.flat == 7
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.max_value is None
                        or effect.max_value.percent is None
                        or isclose(effect.max_value.percent, 0.07)
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.duration == 8
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.delta is None
                        or effect.delta.flat is None
                        or effect.delta.flat == 9
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.delta is None
                        or effect.delta.percent is None
                        or isclose(effect.delta.percent, 0.09)
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    isclose(effect.accuracy, 0.1)
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.target_keywords is None
                        or len(effect.target_keywords) <= 11
                    )
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
        ]
    )

    assert_conditions(conditions)


def test_get_random_combat(randomizer: Randomizer):
    config = RandomizerConfig(
        team_threshold=(2, 3),
    )

    combat_0 = randomizer.get_random_combat(config)

    conditions = [
        isinstance(combat_0["order_strategy"], OrderStrategy),
        len(combat_0["teams"]) in range(2, 4),
    ]

    config = RandomizerConfig(
        team_threshold=(3, 3),
        member_threshold=(1, 1),
        hp_threshold=(13, 13),
        mana_threshold=(14, 14),
        speed_threshold=(15, 15),
        dice_threshold=(2, 2),
        side_threshold=(4, 4),
        effect_threshold=(5, 5),
        effect_type=EffectType.BUFF,
        value_flat_threshold=(7, 7),
        value_percent_threshold=(0.07, 0.07),
        min_value_flat_threshold=(6, 6),
        min_value_percent_threshold=(0.06, 0.06),
        max_value_flat_threshold=(8, 8),
        max_value_percent_threshold=(0.08, 0.08),
        duration_threshold=(9, 9),
        delta_flat_threshold=(10, 10),
        delta_percent_threshold=(0.1, 0.1),
        accuracy_threshold=(0.11, 0.11),
        target_keywords_threshold=(12, 12),
    )

    combat_1 = randomizer.get_random_combat(config)

    conditions.extend(
        [
            len(combat_1["teams"]) == 3,
            all([len(team.members) == 1 for team in combat_1["teams"]]),
            all(
                [
                    monster.hp == 13
                    for team in combat_1["teams"]
                    for monster in team.members
                ]
            ),
            all(
                [
                    monster.max_hp == monster.hp
                    for team in combat_1["teams"]
                    for monster in team.members
                ]
            ),
            all(
                [
                    monster.mana == 14
                    for team in combat_1["teams"]
                    for monster in team.members
                ]
            ),
            all(
                [
                    monster.speed == 15
                    for team in combat_1["teams"]
                    for monster in team.members
                ]
            ),
            all(
                [
                    len(monster.dice) == 2
                    for team in combat_1["teams"]
                    for monster in team.members
                ]
            ),
            all(
                [
                    len(dice.sides) == 4
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                ]
            ),
            all(
                [
                    len(side.effects) == 5
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                ]
            ),
            all(
                [
                    effect.type == EffectType.BUFF
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.value is None
                        or effect.value.flat is None
                        or effect.value.flat == 7
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.value is None
                        or effect.value.percent is None
                        or isclose(effect.value.percent, 0.07)
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.min_value is None
                        or effect.min_value.flat is None
                        or effect.min_value.flat == 6
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.min_value is None
                        or effect.min_value.percent is None
                        or isclose(effect.min_value.percent, 0.06)
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.max_value is None
                        or effect.max_value.flat is None
                        or effect.max_value.flat == 8
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.max_value is None
                        or effect.max_value.percent is None
                        or isclose(effect.max_value.percent, 0.08)
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.duration == 9
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.delta is None
                        or effect.delta.flat is None
                        or effect.delta.flat == 10
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.delta is None
                        or effect.delta.percent is None
                        or isclose(effect.delta.percent, 0.1)
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    isclose(effect.accuracy, 0.11)
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    (
                        effect.target_keywords is None
                        or len(effect.target_keywords) <= 12
                    )
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
        ]
    )

    assert_conditions(conditions)
