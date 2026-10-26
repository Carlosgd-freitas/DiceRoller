"""Roguelike Engine module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.base.area import Area
    from src.base.node import Node
    from src.base.team import Team
    from src.systems.settings import Settings


class RoguelikeEngine:
    """
    RoguelikeEngine class.

    :var player_team: Player team.
    :vartype player_team: Team

    :var area: Game area.
    :vartype area: Area

    :var settings: Game settings.
    :vartype settings: Settings
    """

    def __init__(
        self,
        player_team: Team,
        area: Area,
        settings: Settings,
        current_node: Node = Node,
    ):
        self.player_team = player_team
        self.area = area
        self.settings = settings
        self.current_node = current_node

    def start_area(self):
        """
        .
        """
        return
