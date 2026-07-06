"""Attribute Logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.color import color_string
from src.base.entity import get_attribute_color
from src.logger.logger import Logger

if TYPE_CHECKING:
    pass


class AttributeLogger(Logger):
    """
    AttributeLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _get_attribute_params(self) -> Dict:
        """
        Returns common attribute parameters for logging.

        :return: Parameters for logging.
        :rtype: Dict
        """
        params = {}

        for attribute in [
            "hp",
            "mana",
            "max_hp",
            "speed",
        ]:
            message = self.get_message(
                namespace="base", message_group="ATTRIBUTES", key=attribute
            )

            color_data = get_attribute_color(attribute)

            message = color_string(message, **color_data)

            params[attribute] = message

        return params
