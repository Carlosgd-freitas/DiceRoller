"""Item module."""

from enum import Enum
from base.entity import Entity


class ItemType(Enum):
    """Type of an Item."""

    ACCESSORY = "ACCESSORY"
    ARMOR = "ARMOR"
    CONSUMABLE = "CONSUMABLE"
    WEAPON = "WEAPON"


class Item(Entity):
    """
    Item class.

    :var type: Item's type.
    :vartype type: ItemType
    """

    def __init__(
        self,
        type: ItemType = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.type: ItemType = type
