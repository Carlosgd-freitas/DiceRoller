"""Nothing effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.effect import Effect
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class NothingEffect(Effect):
    """
    Nothing Effect.

    Does nothing.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.NOTHING,
            value,
            duration,
            decay,
            accuracy,
        )

    def on_apply(
        self,
        source: "Entity",
        target: "Entity",
    ) -> None:
        return

    def activate(
        self,
        source: "Entity",
        target: "Entity",
    ) -> None:
        return
