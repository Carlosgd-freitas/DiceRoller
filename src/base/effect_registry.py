"""Effect registry module."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import TYPE_CHECKING

from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.effect import Effect


EFFECT_CLASSES: dict[Keyword, type[Effect]] = {}


def register_effect(effect_class: type[Effect]) -> None:
    EFFECT_CLASSES[effect_class.keyword] = effect_class


def load_effects() -> None:
    effects_dir = Path(__file__).parents[1] / "effects"

    for module in iter_modules([str(effects_dir)]):
        if module.name.startswith("_"):
            continue

        import_module(f"src.effects.{module.name}")
