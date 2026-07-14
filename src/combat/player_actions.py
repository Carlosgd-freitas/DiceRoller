"""Combat Player Actions module."""

from __future__ import annotations

from copy import deepcopy
from math import inf
from random import random
from typing import TYPE_CHECKING, Dict, List, Literal, TypedDict, TypeVar

from src.base.color import Color, color_string
from src.base.keywords import Keyword
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
from src.systems.targeting.selectors.random_selector import RandomSelector

T = TypeVar("T")

if TYPE_CHECKING:
    from src.base.team import Team
    from src.systems.settings import Settings


class CombatPlayerActionData(TypedDict):
    """
    Data when applying or activating an Effect.

    :var turn_taken: If the player turn has been taken or if it will continue.
    :vartype turn_taken: bool

    :var wait_for_input: If an input will be requested after the player turn is done.
    :vartype wait_for_input: bool
    """

    turn_taken: bool
    wait_for_input: bool


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

    def process_option(
        self, option: Option, monster: Monster
    ) -> CombatPlayerActionData:
        """
        Processes an option chosen by a player.

        :param option: Menu's option.
        :type option: Option

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :return: Combat player action data.
        :rtype: CombatPlayerActionData
        """
        if option.id == "ROLL_DICE":
            return self.roll_dice(monster)

        elif option.id == "SKILLS":
            return {"turn_taken": True, "wait_for_input": True}

        elif option.id == "CONSUMABLES":
            return {"turn_taken": False, "wait_for_input": True}

        elif option.id == "EQUIPMENT":
            return {"turn_taken": False, "wait_for_input": True}

        elif option.id == "SHOW_DETAILS":
            return self.show_details()

        elif option.id == "SKIP_TURN":
            return self.skip_turn(monster)

    def _select(
        self,
        selectables: List[T],
        message_key: str,
        cancel_key: str = "0",
        blacklist: List[T] = None,
    ) -> T:
        """
        Prompts the user with a message to select an object from a list. If an invalid
        index is selected, the prompt will repeat.

        :param selectables: List of selectable objects.
        :type selectables: List[T]

        :param k: The number of monsters which will be selected and returned.
        :type k: int

        :param message_key: Key of the message that will be prompted.
        :type message_key: str

        :param cancel_key: Keyboard key to cancel the operation. Default value is "0".
        :type cancel_key: str

        :param blacklist: Only objects that aren't in this list can be selected.
        :type blacklist: List[T]

        :return: Selected objects.
        :rtype: List[T]
        """
        selected = None

        while True:
            message = self.logger.get_message(
                namespace="menus",
                message_group="PLAYER_ACTIONS",
                key=message_key,
            )

            index = self.logger.input(message=message)

            if index == cancel_key:
                return None

            try:
                index = int(index)

                if index > 0:
                    selected = selectables[index - 1]

                    if (not blacklist) or (selected not in blacklist):
                        return selected

            except Exception:
                continue

    def _get_targets(
        self,
        side: Side,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        blacklist: List[Monster] = None,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on Side's effects.

        :param side: A Side.
        :type side: Side

        :param source: The source monster which is targeting others.
        :type source: Monster

        :param allies: The source monster's allies.
        :type allies: List[Monster]

        :param enemies: The source monster's enemies.
        :type enemies: List[Monster]

        :param blacklist: Only monters that aren't in this list will be considered.
        :type blacklist: List[Monster]

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        targets = []
        blacklist = [] if blacklist is None else deepcopy(blacklist)

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
            if effect_type in ["BUFF", "CURSE", "DEFENSIVE", "NOTHING", "RESTORATION"]:
                add_self = True
                add_allies = True
            elif effect_type in ["DEBUFF", "OFFENSIVE", "DETERIORATION"]:
                add_enemies = True

        # Determining targets
        if add_self:
            targets.extend(
                filter_monsters(
                    [source],
                    k=inf,
                    life_state=life_state,
                    blacklist=blacklist,
                    consider=[],
                    method="FIRST",
                )
            )

            blacklist.extend(targets)

        if add_allies:
            targets.extend(
                filter_monsters(
                    allies,
                    k=inf,
                    blacklist=blacklist,
                    life_state=life_state,
                    consider=[],
                    method="FIRST",
                )
            )

            blacklist.extend(targets)

        if add_enemies:
            taunting = filter_monsters(
                enemies,
                k=inf,
                blacklist=blacklist,
                keyword_whitelist=[Keyword.TAUNT],
                life_state=life_state,
                method="FIRST",
            )

            if taunting:
                targets.extend(taunting)

            else:
                not_repelling = filter_monsters(
                    enemies,
                    k=inf,
                    blacklist=blacklist,
                    keyword_blacklist=[Keyword.REPEL],
                    life_state=life_state,
                    method="FIRST",
                )

                if not_repelling:
                    targets.extend(not_repelling)

                else:
                    repelling = filter_monsters(
                        enemies,
                        k=inf,
                        blacklist=blacklist,
                        keyword_whitelist=[Keyword.REPEL],
                        life_state=life_state,
                        method="FIRST",
                    )

                    if repelling:
                        targets.extend(repelling)

        return targets

    def _is_automatic(self, side: Side) -> bool:
        """
        Returns if a side needs to be used automatically or if the player can select
        the targets.

        :param side: A Side.
        :type side: Side

        :return: If the side needs to be used automatically.
        :rtype: bool
        """
        effect_summary = side.get_effect_summary()

        used = all(
            [
                effect_type in ["CURSE", "NOTHING"]
                for effect_type in effect_summary.keys()
            ]
        )

        return used

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

        :return: Combat player action data.
        :rtype: CombatPlayerActionData
        """
        sides = self.effect_manager.roll(monster)
        K = 1  # Number of targets

        while len(sides) > 0:
            # Logging sides
            self.logger.log(message="")

            for index, side in enumerate(sides):
                message = self.logger.get_side_details(side, index + 1)
                self.logger.log(message=message)

            message = (
                "\n[0] "
                + self.logger.get_message(
                    namespace="menus",
                    message_group="BASE",
                    key="cancel",
                )
                + "\n"
            )
            self.logger.log(message=message)

            # Player selecting side
            side = self._select(sides, message_key="select_side_prompt")
            self.logger.log(message="")

            # Cancelling action
            if side is None:
                return {"turn_taken": True, "wait_for_input": False}

            # Target selecting
            allies = self.team_manager.get_allies(monster, self.teams)
            enemies = self.team_manager.get_enemies(monster, self.teams)
            enemies = preprocess_enemies(enemies)

            automatic = self._is_automatic(side)
            confused = monster.get_effect(Keyword.CONFUSE)

            main_keyword = side.get_main_keyword()

            # Automatic target selecting
            if automatic:
                selected_targets = self._get_targets(
                    side=side,
                    source=monster,
                    allies=allies,
                    enemies=enemies,
                )[:K]

            # Confuse target selecting
            elif confused and random() < confused.value_percent:
                selector = RandomSelector()

                selected_targets = selector.get_targets_hard(
                    source=monster,
                    allies=allies,
                    enemies=enemies,
                    k=K,
                    main_keyword=main_keyword,
                )

            # Manual target selecting
            else:
                selected_targets = []
                cancel = False

                while len(selected_targets) < K:
                    # Cancelling operation
                    if cancel:
                        break

                    # Getting targets
                    selectable = self._get_targets(
                        side=side,
                        source=monster,
                        allies=allies,
                        enemies=enemies,
                        blacklist=selected_targets,
                    )

                    if not selectable:
                        break

                    # Logging targets
                    self.logger.log_teams(
                        teams=self.teams,
                        whitelist=selectable,
                        life_state=LifeState.ANY,
                        control_type=False,
                        monster_index=1,
                    )

                    message = (
                        "[0] "
                        + self.logger.get_message(
                            namespace="menus",
                            message_group="BASE",
                            key="return",
                        )
                        + "\n"
                    )
                    self.logger.log(message=message)

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

                    # Logging selecting progress
                    if K > 1:
                        self.logger.log(
                            message=f"({len(selected_targets)+1}/{K}) ", end=""
                        )

                    # Player selecting target
                    selected_target = self._select(
                        selectable,
                        message_key="select_target_prompt",
                        blacklist=selected_targets,
                    )

                    if selected_target:
                        self.logger.log(message="")
                        selected_targets.append(selected_target)
                    else:
                        cancel = True

                # Cancelling target selection
                if cancel:
                    continue

            # Executing effects
            if selected_targets:
                for target in selected_targets:
                    for effect in side.effects:
                        self.effect_manager.execute_effect(
                            effect=effect,
                            source=monster,
                            target=target,
                        )

            # No targets to select
            else:
                message = self.logger.get_message(
                    namespace="menus",
                    message_group="PLAYER_ACTIONS",
                    key="side_no_targets",
                )
                self.logger.log(message=message)

            sides.remove(side)

        return {"turn_taken": True, "wait_for_input": True}

    def show_details(self) -> CombatPlayerActionData:
        """
        The steps of this method is as follows:
        1. All alive monsters in combat are logged.
        2. The player selects one of them to have their details logged.

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :return: Combat player action data.
        :rtype: CombatPlayerActionData
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

        message = (
            "[0] "
            + self.logger.get_message(
                namespace="menus",
                message_group="BASE",
                key="cancel",
            )
            + "\n"
        )
        self.logger.log(message=message)

        # Player selecting target
        selected = self._select(targets, message_key="select_target_prompt")

        # Cancelling action
        if selected is None:
            return {"turn_taken": False, "wait_for_input": True}

        # Logging monster details
        self.logger.log(message="")
        self.logger.log_monster_details(
            monster=selected,
            description=False,
            current_hp=True,
        )

        return {"turn_taken": False, "wait_for_input": True}

    def skip_turn(self, monster: Monster) -> CombatPlayerActionData:
        """
        Skips a monster's turn.

        :param monster: Monster being controlled by a player.
        :type monster: Monster

        :return: Combat player action data.
        :rtype: CombatPlayerActionData
        """
        self.logger.log_turn_skip(monster=monster)

        return {"turn_taken": True, "wait_for_input": True}

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
        data: CombatPlayerActionData = {
            "turn_taken": False,
            "wait_for_input": True,
        }

        while not data["turn_taken"]:
            self.show_options(monster)
            selected = self.select_option()

            if self.is_option_valid(selected, monster):
                data = self.process_option(selected, monster)

            if not data["turn_taken"]:
                self.logger.log_turn_start(monster)
                self.logger.log_teams(self.teams)

        if data["wait_for_input"]:
            self.logger.input(message="")

        return
