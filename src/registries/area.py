"""Area registry module."""

from typing import TYPE_CHECKING, ClassVar

from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.area import Area


class AreaRegistry(Registry["Area"]):
    """Registry for area classes."""

    id_name: str = "id"
    dir_name: str = "areas"
    registries: ClassVar[dict[str, type[Area]]] = {}
