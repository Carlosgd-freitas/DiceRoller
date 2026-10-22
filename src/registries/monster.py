"""Monster registry module."""

from typing import TYPE_CHECKING, ClassVar

from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.monster import Monster


class MonsterRegistry(Registry["Monster"]):
    """Registry for monster classes."""

    id_name: str = "global_id"
    dir_name: str = "monsters"
    registries: ClassVar[dict[str, type[Monster]]] = {}
