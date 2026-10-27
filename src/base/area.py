"""Area module."""

from abc import abstractmethod
from math import ceil
from random import choices
from typing import List, Literal, TypedDict
from uuid import uuid4

from src.base.difficulties import Difficulty
from src.base.graph import Graph, GraphConfig
from src.base.node import Node, NodeType
from src.base.team import Team
from src.factories.monster import MonsterFactory
from src.registries.area import AreaRegistry


class EncounterEntryData(TypedDict):
    """
    Encounter entry data for an Area.

    :var monster_global_id: Global identifier of the monster that can be encountered.
    :vartype monster_global_id: str

    :var weight: Monster encounter weight.
    :vartype weight: float

    :var weight: Role of the monster in the encounter.
    :vartype weight: float
    """

    monster_global_id: str
    weight: float
    role: Literal["DAMAGE", "SUPPORT"]


class Area:
    """
    Area class.

    :var id: Area unique identifier.
    :vartype id: str

    :var name: Area name.
    :vartype name: str

    :var difficulty: Game difficulty. Default value is Difficulty.NORMAL.
    :vartype difficulty: Difficulty

    :var graph: Graph for player navigation.
    :vartype graph: Graph

    :var current_node: Current graph node the player is in.
    :vartype current_node: Node
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        AreaRegistry.register(cls)

    def __init__(
        self,
        id: str = str(uuid4()),
        name: str = None,
        difficulty: Difficulty = Difficulty.NORMAL,
        graph: Graph = None,
        current_node: Node = None,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.difficulty = difficulty
        self.current_node = current_node

        # Graph
        if graph is None:
            config = self.get_graph_config()
            graph = Graph()
            graph.generate(config)

            self.setup_graph(graph)

        self.graph = graph

    def get_graph_config(self) -> GraphConfig:
        """
        Returns the configuration for the Area Graph.

        :return: Area Graph configuration.
        :rtype: GraphConfig
        """
        return GraphConfig()

    @abstractmethod
    def get_enemies(self) -> List[EncounterEntryData]:
        """
        Returns a list of possible enemies on the area.

        :return: Possible enemies on the area.
        :rtype: List[EncounterEntryData]
        """
        raise NotImplementedError

    @abstractmethod
    def get_bosses(self) -> List[EncounterEntryData]:
        """
        Returns a list of possible bosses on the area.

        :return: Possible bosses on the area.
        :rtype: List[EncounterEntryData]
        """
        raise NotImplementedError

    def get_encounter(
        self,
        encounter_entries: List[EncounterEntryData],
        k: int = None,
        path_level: int = None,
        ratio: int = 2,
        allow_support_only: bool = False,
    ) -> Team:
        """
        Returns a Team for combat encounters is battle-type Nodes.

        :var encounter_entries: The possible entries that can compose the encounter.
        :vartype encounter_entries: List[EncounterEntryData]

        :var k: The number of the enemies that will participate in the encounter. If
        not passed, this will be infered by the `path_level` param.
        :vartype k: int

        :var path_level: The path level of the Area Node in which the combat encounter
        will take place.
        :vartype path_level: int

        :var ratio: Number of path levels that will have the same amount of monsters (e.g. 2 means that one
        more monster will be added to the encounter after each 2 leves, or at each 3rd level). Default value is 2.
        :vartype ratio: int

        :var allow_support_only: If encounters composed only of monsters with support
        roles are allowed to be generated. Default value is False.
        :vartype allow_support_only: bool

        :return: The enemy team that will participate in combat.
        :rtype: Team
        """
        chosen_entries: List[EncounterEntryData] = []

        if not allow_support_only:
            non_support_entries = [
                encounter_entry
                for encounter_entry in encounter_entries
                if encounter_entry["role"] != "SUPPORT"
            ]

            chosen_entries = choices(
                non_support_entries,
                weights=[
                    encounter_entry["weight"] for encounter_entry in non_support_entries
                ],
                k=1,
            )

        if k is None:
            if path_level is not None:
                k = ceil(path_level / ratio)
            else:
                raise ValueError("Either k or path_level param must be passed.")

        if len(chosen_entries) < k:
            chosen_entries.extend(
                choices(
                    encounter_entries,
                    weights=[
                        encounter_entry["weight"]
                        for encounter_entry in encounter_entries
                    ],
                    k=k - len(chosen_entries),
                )
            )

        members = [
            MonsterFactory.create(
                encounter_entry["monster_global_id"],
                difficulty=self.difficulty,
            )
            for encounter_entry in chosen_entries
        ]

        return Team(members=members)

    def setup_node(self, node: Node) -> None:
        """
        Sets up a Node with information from the Area.

        :var node: A Node.
        :vartype node: Node
        """
        if node.type == NodeType.BATTLE:
            encounter_entries = self.get_enemies()
            encounter = self.get_encounter(
                encounter_entries, path_level=node.path_level
            )
            node.encounter = encounter

        elif node.type == NodeType.BOSS_BATTLE:
            encounter_entries = self.get_bosses()
            encounter = self.get_encounter(encounter_entries, k=1)
            node.encounter = encounter

        return

    def setup_graph(self, graph: Graph) -> None:
        """
        Sets up a Graph with information from the Area.

        :var graph: A Graph.
        :vartype graph: Graph
        """
        for _, node in graph.nodes.items():
            self.setup_node(node)

        return
