"""Effect registry module."""

from typing import TYPE_CHECKING, ClassVar

from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.effect import Effect


class EffectRegistry(Registry["Effect"]):
    """Registry for Effect classes."""

    id_name: str = "keyword"
    dir_name: str = "effects"
    registries: ClassVar[dict[str, type[Effect]]] = {}
