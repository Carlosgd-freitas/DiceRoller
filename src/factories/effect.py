"""Effect factory module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect_registry import EFFECT_CLASSES, load_effects
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.effect import Effect

load_effects()


class EffectFactory:
    @staticmethod
    def create_effect(
        keyword: Keyword,
        **kwargs,
    ) -> Effect:
        effect_class = EFFECT_CLASSES.get(keyword)

        if effect_class is None:
            raise ValueError(f"No effect registered for keyword: {keyword}")

        return effect_class(**kwargs)
