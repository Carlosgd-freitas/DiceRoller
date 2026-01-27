"""Side module."""

from typing import List, Tuple
from src.base.effect import Effect
from src.base.keywords import Keyword


class Side:
    """
    Side class.
    
    :var effects: Side's effects, which will be executed in order.
    :vartype effects: List[Effect]

    :var weight: Side's weight when rolling a dice. Default value is 1.
    :vartype weight: float
    """

    def __init__(self, effects: List[Effect], weight: float = 1):
        self.effects = effects
        self.weight = weight

    def get_effects(
        self,
        keyword: Keyword = None,
        value: float = None,
        duration: int = None,
        decay: int = None,
        chance: float = None
    ) -> List[Tuple[int, Effect]]:
        """
        Returns a list of indexes and effects based on a series of filters.

        :param self: Side object.

        :param keyword: Filters effects that have the same keyword parameter.
        :type keyword: Keyword

        :param value: Filters effects that have the same value parameter.
        :type value: float

        :param duration: Filters effects that have the same duration parameter.
        :type duration: int

        :param decay: Filters effects that have the same decay parameter.
        :type decay: int

        :param chance: Filters effects that have the same chance parameter.
        :type chance: float

        :return: List of Tuples, where the first element is the Side 'effects' parameter's
        index, and the second is the effect itself.
        :rtype: List[Tuple[int, Effect]]
        """
        result = []

        for idx, effect in enumerate(self.effects):
            in_filter = False

            for comparison_key, comparison_value in [
                ("keyword", keyword),
                ("value", value),
                ("duration", duration),
                ("decay", decay),
                ("chance", chance)
            ]:
                if comparison_value is not None:
                    if effect.__getattribute__(comparison_key) == comparison_value:
                        in_filter = True
                    else:
                        in_filter = False
                        break

            if in_filter:
                result.append((idx, effect))

        return result
