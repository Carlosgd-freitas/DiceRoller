"""Side module."""

from __future__ import annotations

from src.base.keywords import Keyword
from typing import List, Tuple, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from src.base.effect import Effect


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

    def __str__(self) -> str:
        _str = ""
        
        for idx, effect in enumerate(self.effects):
            if idx > 0:
                _str += " + "

            _str += str(effect)

        return _str

    def get_effects(
        self,
        keyword: Keyword = None,
        value: float = None,
        duration: int = None,
        decay: int = None,
        accuracy: float = None
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

        :param accuracy: Filters effects that have the same accuracy parameter.
        :type accuracy: float

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
                ("accuracy", accuracy)
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

    def get_effects_summary(self) -> Dict:
        """
        Gets a summary of the Side's effects based on their types.

        :return: A dictionary where the keys are effect types and the values are lists
        containing the keywords of the effects.
        :rtype: Dict
        """
        types = {}

        for effect in self.effects:
            if effect.type.value not in types:
                types[effect.type.value] = [effect.keyword]
            else:
                types[effect.type.value].append(effect.keyword)
        
        return types
