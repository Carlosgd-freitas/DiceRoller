"""Tests for Randomizer class."""

from __future__ import annotations

from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.systems.randomizer import Randomizer, RandomizerConfig
from tests.utils import assert_conditions


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


def test_get_random_effect(randomizer: Randomizer):
    config = RandomizerConfig(
        value_threshold=(1, 6),
        value_percent_threshold=(0.01, 0.1),
        duration_threshold=(2, 4),
        accuracy_threshold=(0.8, 1),
        target_keywords_threshold=(3, 6),
        effect_type=EffectType.DETERIORATION,
    )

    effect_0 = randomizer.get_random_effect(config)

    conditions = [
        effect_0.value in range(1, 7),
        effect_0.value_percent >= 0.01,
        effect_0.value_percent <= 0.1,
        effect_0.duration in range(2, 5),
        effect_0.accuracy >= 0.8,
        effect_0.accuracy <= 1,
        effect_0.type == EffectType.DETERIORATION,
        len(effect_0.target_keywords) in range(3, 7),
    ]

    config = RandomizerConfig(
        value_threshold=(1, 1),
        value_percent_threshold=(0.02, 0.02),
        duration_threshold=(3, 3),
        accuracy_threshold=(0.4, 0.4),
        target_keywords_threshold=(0, 0),
        effect_type=EffectType.DETERIORATION,
        keyword_whitelist=[Keyword.EXECUTE],
    )

    effect_1 = randomizer.get_random_effect(config)

    conditions.extend(
        [
            effect_1.value == 1,
            effect_1.value_percent == 0.02,
            effect_1.duration == 3,
            effect_1.accuracy == 0.4,
            effect_1.keyword == Keyword.EXECUTE,
            len(effect_1.target_keywords) == 0,
        ]
    )

    assert_conditions(conditions)


def test_get_random_side(randomizer: Randomizer):
    config = RandomizerConfig(
        effect_threshold=(1, 3),
    )

    side_0 = randomizer.get_random_side(config)

    same_type = True
    effect_type = side_0.effects[0].type

    for effect in side_0.effects:
        if effect.type != effect_type:
            same_type = False
            break

    conditions = [
        len(side_0.effects) in range(1, 4),
        same_type is True,
    ]

    config = RandomizerConfig(
        effect_threshold=(1, 1),
        value_threshold=(2, 2),
        value_percent_threshold=(0.3, 0.3),
        duration_threshold=(4, 4),
        accuracy_threshold=(0.05, 0.05),
        target_keywords_threshold=(0, 0),
        effect_type=EffectType.OFFENSIVE,
        keyword_whitelist=[Keyword.ATTACK],
    )

    side_1 = randomizer.get_random_side(config)

    conditions.extend(
        [
            len(side_1.effects) == 1,
            side_1.effects[0].value == 2,
            side_1.effects[0].value_percent == 0.3,
            side_1.effects[0].duration == 4,
            side_1.effects[0].accuracy == 0.05,
            len(side_1.effects[0].target_keywords) == 0,
            side_1.effects[0].keyword == Keyword.ATTACK,
        ]
    )

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
        value_threshold=(3, 3),
        value_percent_threshold=(0.4, 0.4),
        duration_threshold=(5, 5),
        accuracy_threshold=(0.06, 0.06),
        target_keywords_threshold=(0, 0),
        effect_type=EffectType.OFFENSIVE,
    )

    dice_1 = randomizer.get_random_dice(config)

    conditions.extend(
        [
            len(dice_1.sides) == 2,
            all([len(side.effects) == 1 for side in dice_1.sides]),
            all(
                [effect.value == 3 for side in dice_1.sides for effect in side.effects]
            ),
            all(
                [
                    effect.value_percent == 0.4
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.duration == 5
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.accuracy == 0.06
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    len(effect.target_keywords) == 0
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.type == EffectType.OFFENSIVE
                    for side in dice_1.sides
                    for effect in side.effects
                ]
            ),
        ]
    )

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
        monster_0.hp in range(80, 101),
        monster_0.max_hp == monster_0.hp,
        monster_0.mana in range(20, 31),
        monster_0.speed in range(10, 16),
        len(monster_0.dice) in range(2, 5),
    ]

    config = RandomizerConfig(
        hp_threshold=(10, 10),
        mana_threshold=(9, 9),
        speed_threshold=(8, 8),
        dice_threshold=(2, 2),
        side_threshold=(1, 1),
        effect_threshold=(3, 3),
        value_threshold=(4, 4),
        value_percent_threshold=(0.5, 0.5),
        duration_threshold=(6, 6),
        accuracy_threshold=(0.07, 0.07),
        target_keywords_threshold=(0, 0),
        effect_type=EffectType.DEBUFF,
    )

    monster_1 = randomizer.get_random_monster(config)

    conditions.extend(
        [
            monster_1.hp == 10,
            monster_1.max_hp == monster_1.hp,
            monster_1.mana == 9,
            monster_1.speed == 8,
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
                    effect.value == 4
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.value_percent == 0.5
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.duration == 6
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.accuracy == 0.07
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    len(effect.target_keywords) == 0
                    for dice in monster_1.dice
                    for side in dice.sides
                    for effect in side.effects
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
        ]
    )

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
        hp_threshold=(11, 11),
        mana_threshold=(10, 10),
        speed_threshold=(9, 9),
        dice_threshold=(1, 1),
        side_threshold=(3, 3),
        effect_threshold=(4, 4),
        value_threshold=(5, 5),
        value_percent_threshold=(0.6, 0.6),
        duration_threshold=(7, 7),
        accuracy_threshold=(0.08, 0.08),
        target_keywords_threshold=(0, 0),
        effect_type=EffectType.BUFF,
    )

    team_1 = randomizer.get_random_team(config)

    conditions.extend(
        [
            len(team_1.members) == 2,
            all([monster.hp == 11 for monster in team_1.members]),
            all([monster.max_hp == monster.hp for monster in team_1.members]),
            all([monster.mana == 10 for monster in team_1.members]),
            all([monster.speed == 9 for monster in team_1.members]),
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
                    effect.value == 5
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.value_percent == 0.6
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.duration == 7
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.accuracy == 0.08
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    len(effect.target_keywords) == 0
                    for monster in team_1.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
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
        ]
    )

    assert_conditions(conditions)


def test_get_random_combat(randomizer: Randomizer):
    config = RandomizerConfig(
        team_threshold=(2, 3),
    )

    combat_0 = randomizer.get_random_combat(config)

    conditions = [
        len(combat_0["teams"]) in range(2, 4),
    ]

    config = RandomizerConfig(
        team_threshold=(3, 3),
        member_threshold=(1, 1),
        hp_threshold=(12, 12),
        mana_threshold=(11, 11),
        speed_threshold=(10, 10),
        dice_threshold=(2, 2),
        side_threshold=(4, 4),
        effect_threshold=(5, 5),
        value_threshold=(6, 6),
        value_percent_threshold=(0.7, 0.7),
        duration_threshold=(8, 8),
        accuracy_threshold=(0.09, 0.09),
        target_keywords_threshold=(0, 0),
        effect_type=EffectType.BUFF,
    )

    combat_1 = randomizer.get_random_combat(config)

    conditions.extend(
        [
            len(combat_1["teams"]) == 3,
            all([len(team.members) == 1 for team in combat_1["teams"]]),
            all(
                [
                    monster.hp == 12
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
                    monster.mana == 11
                    for team in combat_1["teams"]
                    for monster in team.members
                ]
            ),
            all(
                [
                    monster.speed == 10
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
                    effect.value == 6
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.value_percent == 0.7
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.duration == 8
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    effect.accuracy == 0.09
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
                ]
            ),
            all(
                [
                    len(effect.target_keywords) == 0
                    for team in combat_1["teams"]
                    for monster in team.members
                    for dice in monster.dice
                    for side in dice.sides
                    for effect in side.effects
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
        ]
    )

    assert_conditions(conditions)
