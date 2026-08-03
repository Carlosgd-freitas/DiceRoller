"""Monster Logger module."""

from __future__ import annotations

from tabulate import tabulate

from src.base.color import Color, color_string
from src.base.keywords import Keyword
from src.base.monster import ControlType, Monster
from src.base.text import numeric_to_string
from src.logger.dice import DiceLogger


class MonsterLogger(DiceLogger):
    """
    MonsterLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def get_monster_name(self, monster: Monster, suffix: bool = True) -> str:
        """
        Gets a monster name.

        :param monster: A monster.
        :type monster: Monster

        :param suffix: If the monster suffix will be included.
        :type suffix: bool

        :return: Monster name.
        :rtype: str
        """
        name = self.get_message(
            namespace="monsters",
            message_group=monster.global_id,
            key="name",
        )

        if name is None:
            name = monster.name

        if suffix and monster.suffix:
            name += " " + monster.suffix

        return name

    def log_monster_details(
        self,
        monster: Monster,
        description: bool = False,
        current_hp: bool = True,
        control_type: bool = False,
    ):
        """
        Logs a Monster details.

        :param monster: A monster.
        :type monster: Monster

        :param description: If the monster description will be logged. Default value
        is False.
        :type description: bool

        :param current_hp: If True, "hp/max_hp" will be logged, and "max_hp" only
        otherwise. Default value is True.
        :type current_hp: bool

        :param control_type: If the monster control type will be logged. Default
        value is False.
        :type control_type: bool
        """
        if not self.enabled:
            return

        # Name + Suffix
        message = self.get_monster_name(monster)

        message = color_string(
            message,
            intensity="BRIGHT",
            underlined=True,
        )
        self.log(message=message + "\n")

        # Description
        if description:
            message = self.get_message(
                namespace="monsters",
                message_group=monster.global_id,
                key="description",
            )

            message = color_string(
                message,
                italic=True,
            )

            if message:
                self.log(message=message + "\n")

        # Atrributes
        attribute_params = self._get_attribute_params()
        attributes = []

        # HP
        row = []

        message = attribute_params["hp"] + ":"
        row.append(message)

        if current_hp:
            message = f"{monster.hp}/{monster.max_hp}"
        else:
            message = f"{monster.max_hp}"
        row.append(message)

        attributes.append(row)

        # Mana
        row = []

        message = attribute_params["mana"] + ":"
        row.append(message)

        message = f"{monster.mana}"
        row.append(message)

        attributes.append(row)

        # Speed
        row = []

        message = attribute_params["speed"] + ":"
        row.append(message)

        speed = monster.get_effective_speed()
        message = numeric_to_string(speed)

        if monster.has_effect(Keyword.HASTE):
            message = color_string(message, foreground_color=Color.SPRING_GREEN)
        elif monster.has_effect(Keyword.SLOW):
            message = color_string(message, foreground_color=Color.TOMATO)

        row.append(message)

        attributes.append(row)

        # Control Type
        if control_type:
            # Blank line
            attributes.append(["", ""])

            row = []

            message = self.get_message(
                namespace="base",
                message_group="LEXICON",
                key="control",
            ).title()

            message = (
                color_string(
                    message,
                    intensity="BRIGHT",
                )
                + ": "
            )

            row.append(message)

            message = self.get_message(
                namespace="combat",
                message_group="COMBAT",
                key=monster.control_type.name.lower(),
            )

            if monster.control_type == ControlType.AI:
                foreground_color = Color.RED

                # IA Level
                message += f" ({monster.difficulty.name})"

            elif monster.control_type == ControlType.PLAYER:
                foreground_color = Color.BLUE

            message = color_string(
                message,
                foreground_color=foreground_color,
                intensity="BRIGHT",
            )

            row.append(message)

            attributes.append(row)

        # Logging attributes
        table = tabulate(
            attributes,
            colalign=("right", "left"),
            tablefmt="plain",
        )

        self.log(message=table)

        # Dice
        if len(monster.dice) > 0:
            for idx, dice in enumerate(monster.dice):
                self.log(message="")

                if idx == 0:
                    message = (
                        self.get_message(
                            namespace="base",
                            message_group="LEXICON",
                            key="dices",
                        ).title()
                        + ":"
                    )

                    message = color_string(
                        message,
                        intensity="BRIGHT",
                    )
                    self.log(message=message)

                header = (
                    self.get_message(
                        namespace="base",
                        message_group="LEXICON",
                        key="dice",
                    ).title()
                    + f" #{idx+1}"
                )

                self.log_dice_details(dice, header=header)

        # Effects
        if len(monster.effects) > 0:
            self.log(message="")

            message = (
                self.get_message(
                    namespace="base",
                    message_group="LEXICON",
                    key="effects",
                ).title()
                + ":"
            )

            message = color_string(
                message,
                intensity="BRIGHT",
            )
            self.log(message=message)

            for effect in monster.effects:
                self.log(message="● ", end="")

                self.log_effect_details(
                    effect=effect,
                    source=monster,
                )
