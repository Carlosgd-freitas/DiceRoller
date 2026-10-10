"""Effect registry module."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import TYPE_CHECKING

from src.base.keywords import Keyword
from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.effect import Effect

REGISTRIES: dict[Keyword, type[Effect]] = {}


class EffectRegistry(Registry):
    """
    Effect Registry class.
    """

    @staticmethod
    def register(registry: type[Effect]) -> None:
        """
        Registers a class if it defines its own identifier.

        :param registry: Effect class to be registered.
        :type registry: type[Effect]
        """
        keyword = registry.__dict__.get("keyword")

        if keyword is None:
            return
        elif keyword in REGISTRIES:
            raise ValueError(f"Duplicate effect global ID: {keyword}")

        REGISTRIES[keyword] = registry

    @staticmethod
    def load() -> None:
        """
        Import registries modules.
        """
        effects_dir = Path(__file__).parents[1] / "effects"

        for module in iter_modules([str(effects_dir)]):
            if module.name.startswith("_"):
                continue

            import_module(f"src.effects.{module.name}")
