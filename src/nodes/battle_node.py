"""Battle Node module."""

from typing import List

from src.base.node import Node, NodeType
from src.base.team import Team
from src.combat.manager import CombatData, CombatManager, CombatStatus


class BattleNode(Node):
    """
    Battle Node.

    When entered, starts a combat between teams.
    """

    type = NodeType.BATTLE
    encounter: Team

    def __init__(
        self,
        label: str = "A",
        path_level: int = 1,
        previous_nodes: List[Node] = None,
        next_nodes: List[Node] = None,
    ):
        super().__init__(
            type=self.type,
            label=label,
            path_level=path_level,
            previous_nodes=previous_nodes,
            next_nodes=next_nodes,
        )
        self.encounter: Team = None

    def __str__(self) -> str:
        """String representation of BattleNode."""
        _str = super().__str__()

        if isinstance(self.encounter, Team) and len(self.encounter.members) > 0:
            encounter = ", ".join(
                [str(member.global_id) for member in self.encounter.members]
            )
        else:
            encounter = str(self.encounter)

        _str += f"\nEncounter: {encounter}"

        return _str

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
