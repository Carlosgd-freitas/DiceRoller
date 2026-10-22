"""Character registry module."""

from typing import TYPE_CHECKING, ClassVar

from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.character import Character


class CharacterRegistry(Registry["Character"]):
    """Registry for Character classes."""

    id_name: str = "global_id"
    dir_name: str = "characters"
    registries: ClassVar[dict[str, type[Character]]] = {}
