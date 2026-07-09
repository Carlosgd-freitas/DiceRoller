"""Combat Player Actions module."""

from __future__ import annotations

from math import inf
from typing import TYPE_CHECKING, Dict, List, Literal

from src.base.color import Color, color_string
from src.base.life_state import LifeState
from src.base.monster import Monster
from src.base.side import Side
from src.combat.effects import EffectManager
from src.combat.team_manager import TeamManager
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.menus.option import Option
from src.systems.targeting.filters import (
    filter_monsters,
    preprocess_enemies,
)

if TYPE_CHECKING:
    from src.base.team import Team
    from src.systems.settings import Settings


class CombatPlayerActionsMenu(Menu):
    """
    CombatPlayerActionsMenu class.

    :var settings: Game settings.
    :vartype settings: Settings

    :var logging: If logging is enabled. Default value is True.
    :vartype logging: bool
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        settings: Settings,
        logging: bool = True,
        teams: List[Team] = None,
    ):
        # Initialization
        logger = CombatLogger(enabled=logging, language=settings.language)

        super().__init__(
            logger,
            settings,
        )

        self.logger: CombatLogger

        # Effect Management
        self.effect_manager = EffectManager(settings, logging)

        # Team Management
        self.teams = [] if teams is None else teams
        self.team_manager = TeamManager()

    def get_title(self) -> None:
        """
        Returns the Menu title.

        :return: Menu title.
        :rtype: str
        """
        pass

    def get_options(self) -> List[Option]:
        """
        Returns the Menu options.

        :return: Menu options.
        :rtype: List[Option]
        """
        options = [
            Option(
                id="ROLL_DICE",
                key="1",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="roll_dice",
                ),
            ),
            Option(
                id="SKILLS",
                key="2",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="skills",
                ),
            ),
            Option(
                id="CONSUMABLES",
                key="3",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="consumables",
                ),
            ),
            Option(
                id="EQUIPMENT",
                key="4",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="equipment",
                ),
            ),
            Option(
                id="SHOW_DETAILS",
                key="5",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="show_details",
                ),
            ),
            Option(
                id="SKIP_TURN",
                key="0",
                message=self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="skip_turn",
                ),
                isolate_before=True,
                isolate_after=True,
            ),
        ]

        return options

    # =========================================================================
    # Utility
    # =========================================================================

    def change_language(self, language: Language, _messages: Dict = None):
        """
        Changes the Menu language.

        :var language: A Language.
        :vartype language: Language

        :var _messages: Messages loaded from a locale module.
        :vartype _messages: Dict
        """
        self.logger.change_language(language, _messages)
        _messages = self.logger._messages

        # Managers
        self.effect_manager.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Menu logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled

        # Managers
        self.effect_manager.toggle_logging(enabled)

    # =========================================================================
    # Options
    # =========================================================================

    def is_option_valid(self, option: Option, monster: Monster) -> bool:
        """
        Returns if the option can be selected or not.

        :param option: Menu's option.
        :type option: Option

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :return: If the option can be selected.
        :rtype: bool
        """
        if option.id == "ROLL_DICE":
            return len(monster.dice) > 0

        if option.id in [
            "SKILLS",
            "CONSUMABLES",
            "EQUIPMENT",
        ]:
            return False

        return True

    def process_option(self, option: Option, monster: Monster) -> bool:
        """
        Processes an option chosen by a player.

        :param option: Menu's option.
        :type option: Option

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :return: If the player turn has been taken or if it will continue.
        :rtype: bool
        """
        if option.id == "ROLL_DICE":
            return self.roll_dice(monster)

        elif option.id == "SKILLS":
            return True

        elif option.id == "CONSUMABLES":
            return False

        elif option.id == "EQUIPMENT":
            return False

        elif option.id == "SHOW_DETAILS":
            return self.show_details()

        elif option.id == "SKIP_TURN":
            return self.skip_turn(monster)

    # ToDo: k
    def _select(self, valid_indexes: List[int], message_key: str, k: int = 1) -> int:
        """
        Prompts the user with a message, and if:
        * a valid index is selected, is is returned.
        * an invalid index is selected, the prompt will repeat.
        """
        while True:
            target_number = self.logger.input(
                namespace="menus",
                message_group="PLAYER_ACTIONS",
                key=message_key,
            )

            try:
                target_number = int(target_number)

                if target_number in valid_indexes:
                    break

            except Exception:
                continue

        return target_number

    def _get_targets(self, source: Monster, side: Side) -> List[Monster]:
        """
        Returns a list of target monsters based on Side's effects.

        :param side: A Side.
        :type side: Side

        :param source: The source monster which is targeting others.
        :type source: Monster

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        targets = []
        effect_summary = side.get_effect_summary()

        # Determining life state
        add_alive = False
        add_dead = False

        for effect in side.effects:
            if effect.affects() == LifeState.ALIVE:
                add_alive = True
            elif effect.affects() == LifeState.DEAD:
                add_dead = True
            elif effect.affects() == LifeState.ANY:
                add_alive = True
                add_dead = True
                break

        if add_alive and not add_dead:
            life_state = LifeState.ALIVE
        elif not add_alive and add_dead:
            life_state = LifeState.DEAD
        else:
            life_state = LifeState.ANY

        # Determining groups
        add_self = False
        add_allies = False
        add_enemies = False

        for effect_type, _ in effect_summary.items():
            if effect_type in ["BUFF", "CURSE", "DEFENSIVE", "RESTORATION"]:
                add_self = True
                add_allies = True
            elif effect_type in ["DEBUFF", "OFFENSIVE", "DETERIORATION"]:
                add_enemies = True

        # Determining targets
        if add_self:
            if life_state in [LifeState.ALIVE, LifeState.ANY] and source.is_alive():
                targets.append(source)
            elif (
                life_state in [LifeState.DEAD, LifeState.ANY] and not source.is_alive()
            ):
                targets.append(source)

        if add_allies:
            allies = self.team_manager.get_allies(source, self.teams)

            targets.extend(
                filter_monsters(
                    allies,
                    k=inf,
                    blacklist=targets,
                    life_state=life_state,
                    consider=[],
                    method="FIRST",
                )
            )

        if add_enemies:
            enemies = self.team_manager.get_enemies(source, self.teams)
            enemies = preprocess_enemies(enemies)

            targets.extend(
                filter_monsters(
                    enemies,
                    k=inf,
                    blacklist=targets,
                    life_state=life_state,
                    method="FIRST",
                )
            )

        return targets

    def roll_dice(self, monster: Monster) -> Literal[True]:
        """
        The steps of this method is as follows:
        1. All dice of a monster are rolled.
        2. The player selects which side to use.
        3. The player selects which targets the side will be used on, from available
        targets.
        4. Steps 2~3 are repeated until all sides are used.

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :return: If the player turn has been taken or if it will continue.
        :rtype: Literal[True]
        """
        sides = self.effect_manager.roll(monster)

        while len(sides) > 0:
            # Logging sides
            self.logger.log(message="")

            for index, side in enumerate(sides):
                message = self.logger.get_side_details(side, index + 1)
                self.logger.log(message=message)

            # Player selecting side
            valid_indexes = range(1, len(sides) + 1)
            self.logger.log(message="")
            side_number = self._select(
                valid_indexes,
                message_key="select_side_prompt",
            )
            side = sides[side_number - 1]

            # Getting targets
            targets = self._get_targets(
                source=monster,
                side=side,
            )

            # Logging targets
            self.logger.log(message="")
            self.logger.log_teams(
                teams=self.teams,
                whitelist=targets,
                life_state=LifeState.ANY,
                control_type=False,
                monster_index=1,
            )

            # Logging selected side
            message = (
                self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="selected_side",
                )
                + ": "
            )
            message = color_string(message, intensity="BRIGHT")
            message += self.logger.get_side_details(side)
            self.logger.log(message=message)

            # Player selecting target
            valid_indexes = range(1, len(targets) + 1)
            target_number = self._select(
                valid_indexes,
                message_key="select_target_prompt",
            )
            self.logger.log(message="")
            target = targets[target_number - 1]

            # Executing effects
            for effect in side.effects:
                self.effect_manager.execute_effect(
                    effect=effect,
                    source=monster,
                    target=target,
                )

            sides.remove(side)

        return True

    def show_details(self) -> Literal[True]:
        """
        The steps of this method is as follows:
        1. All alive monsters in combat are logged.
        2. The player selects one of them to have their details logged.

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :return: If the player turn has been taken or if it will continue.
        :rtype: Literal[False]
        """
        # Determining targets
        monsters = [monster for team in self.teams for monster in team.members]
        targets = filter_monsters(
            monsters=monsters,
            k=inf,
            life_state=LifeState.ALIVE,
            consider=[],
            method="FIRST",
        )

        # Logging valid targets
        self.logger.log(message="")
        self.logger.log_teams(
            teams=self.teams,
            whitelist=targets,
            control_type=False,
            monster_index=1,
        )

        # Player selecting target
        valid_indexes = range(1, len(targets) + 1)
        target_number = self._select(valid_indexes, message_key="select_target_prompt")
        target = targets[target_number - 1]

        # Logging monster details
        self.logger.log(message="")
        self.logger.log_monster_details(
            monster=target,
            description=False,
            current_hp=True,
        )

        return False

    def skip_turn(self, monster: Monster) -> Literal[True]:
        """
        Skips a monster's turn.

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :return: If the player turn has been taken or if it will continue.
        :rtype: Literal[True]
        """
        self.logger.log_turn_skip(monster=monster)

        return True

    # =========================================================================
    # Rendering
    # =========================================================================

    def show_options(self, monster: Monster):
        """
        Shows the Menu options.

        :param monster: Monster being controlled by a player.
        :type monster: Monster
        """
        for option in self.options:
            message = ""

            if option.isolate_before:
                message += "\n"

            message += f"[{option.key}] {option.message}"

            if option.isolate_after:
                message += "\n"

            if not self.is_option_valid(option, monster):
                message = color_string(message, foreground_color=Color.RED)

            self.logger.log(message=message)

        if not self.options[-1].isolate_after:
            self.logger.log(message="")

        return

    def open(self, monster: Monster, teams: List[Team]):
        """
        Opens the Menu.

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :param teams: A list of teams in combat.
        :type teams: List[Team]
        """
        self.teams = teams
        turn_taken = False

        while not turn_taken:
            self.show_options(monster)
            selected = self.select_option()

            if self.is_option_valid(selected, monster):
                turn_taken = self.process_option(selected, monster)

            if not turn_taken:
                self.logger.log_turn_start(monster)
                self.logger.log_teams(self.teams)

        self.logger.input(message="")

        return
