"""Area module."""

from abc import abstractmethod
from typing import List, TypedDict
from uuid import uuid4

from src.base.graph import Graph, GraphConfig


class EncounterData(TypedDict):
    """
    Encounter data for an Area.

    :var monster_global_id: Global identifier of the monster that can be encountered.
    :vartype monster_global_id: str

    :var weight: Monster encounter weight.
    :vartype weight: float
    """

    monster_global_id: str
    weight: float


class Area:
    """
    Area class.

    :var id: Area unique identifier.
    :vartype id: str

    :var name: Area name.
    :vartype name: str

    :var graph: Graph for player navigation.
    :vartype graph: Graph
    """

    def __init__(
        self,
        id: str = str(uuid4()),
        name: str = None,
        graph: Graph = None,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.graph = graph

    @abstractmethod
    def get_enemies(self) -> List[EncounterData]:
        """
        Returns a list of possible enemy encounters on the area.

        :return: Possible enemy encounters on the area.
        :rtype: List[EncounterData]
        """
        raise NotImplementedError

    @abstractmethod
    def get_bosses(self) -> List[EncounterData]:
        """
        Returns a list of possible boss encounters on the area.

        :return: Possible boss encounters on the area.
        :rtype: List[EncounterData]
        """
        raise NotImplementedError

    def get_graph_config(self) -> GraphConfig:
        """
        Returns the configuration for the Area Graph.

        :return: Area Graph configuration.
        :rtype: GraphConfig
        """
        return GraphConfig()
