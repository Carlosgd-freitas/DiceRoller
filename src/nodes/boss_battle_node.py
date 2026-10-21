"""Boss Battle Node module."""

from typing import List

from src.base.node import Node, NodeType
from src.combat.manager import CombatData, CombatManager, CombatStatus


class BossBattleNode(Node):
    """
    Boss Battle Node.

    When entered, starts a combat between teams.
    """

    type = NodeType.BOSS_BATTLE

    def __init__(
        self,
        label: str,
        path_level: int,
        previous_nodes: List[Node] = None,
        next_nodes: List[Node] = None,
    ):
        super().__init__(
            label=label,
            type=self.type,
            path_level=path_level,
            previous_nodes=previous_nodes,
            next_nodes=next_nodes,
        )

    def enter(
        self, combat_manager: CombatManager, combat_data: CombatData
    ) -> CombatStatus:
        """
        Game behavior when a player enters the Node.

        :var combat_manager: Manager for running a combat.
        :vartype combat_manager: CombatManager

        :var combat_data: Data for running a combat.
        :vartype combat_data: CombatData

        :return: The final combat status.
        :rtype: CombatStatus
        """
        combat_manager.set_combat_data(combat_data)
        combat_status = combat_manager.run()
        return combat_status
