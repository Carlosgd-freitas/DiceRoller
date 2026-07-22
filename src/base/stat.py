"""Stat module."""

from __future__ import annotations


class Stat:
    """
    Stat class.

    This class acts as a helper for the Effect class.

    :var flat: A value in flat format (e.g. 1, 10).
    :vartype flat: float | None

    :var percent: A value in percentage format (e.g. 0.01 means 1%).
    :vartype percent: float | None
    """

    def __init__(
        self,
        flat: float | None = None,
        percent: float | None = None,
    ):
        self.flat = flat
        self.percent = percent

    def __str__(self) -> str:
        """String representation of Stat."""
        values = []

        if self.flat is not None:
            values.append(str(self.flat))
        if self.percent is not None:
            values.append(str(self.percent * 100) + "%")

        _str = "; ".join(values)

        return _str

    def add(self, stat: Stat, attribute: str):
        """
        Adds a value of another Stat to itself.

        :param stat: A Stat.
        :type stat: Stat

        :param attribute: Stat attribute name.
        :type attribute: str
        """
        self_attribute = getattr(self, attribute)
        stat_attribute = getattr(stat, attribute)

        if self_attribute is not None and stat_attribute is not None:
            new_value = self_attribute + stat_attribute
            setattr(self, attribute, new_value)

        elif stat_attribute is not None:
            setattr(self, attribute, stat_attribute)

    def subtract(self, stat: Stat, attribute: str):
        """
        Subtracts a value of another Stat from itself.

        :param stat: A Stat.
        :type stat: Stat

        :param attribute: Stat attribute name.
        :type attribute: str
        """
        self_attribute = getattr(self, attribute)
        stat_attribute = getattr(stat, attribute)

        if self_attribute is not None and stat_attribute is not None:
            new_value = self_attribute - stat_attribute
            setattr(self, attribute, new_value)

        elif stat_attribute is not None:
            setattr(self, attribute, stat_attribute)

    def lowest(self, stat: Stat, attribute: str):
        """
        Sets a value to the lowest value between itself and another Stat.

        :param stat: A Stat.
        :type stat: Stat

        :param attribute: Stat attribute name.
        :type attribute: str
        """
        self_attribute = getattr(self, attribute)
        stat_attribute = getattr(stat, attribute)

        if self_attribute is not None and stat_attribute is not None:
            new_value = (
                self_attribute if self_attribute < stat_attribute else stat_attribute
            )
            setattr(self, attribute, new_value)

        elif stat_attribute is not None:
            setattr(self, attribute, stat_attribute)

    def highest(self, stat: Stat, attribute: str):
        """
        Sets a value to the highest value between itself and another Stat.

        :param stat: A Stat.
        :type stat: Stat

        :param attribute: Stat attribute name.
        :type attribute: str
        """
        self_attribute = getattr(self, attribute)
        stat_attribute = getattr(stat, attribute)

        if self_attribute is not None and stat_attribute is not None:
            new_value = (
                self_attribute if self_attribute > stat_attribute else stat_attribute
            )
            setattr(self, attribute, new_value)

        elif stat_attribute is not None:
            setattr(self, attribute, stat_attribute)

    def __eq__(self, other: object) -> bool:
        """
        Compares two objects and returns if they are equivalent.

        :param other: Object for comparison.
        :type other: object

        :return: If the objects are equivalent.
        :rtype: bool
        """
        return (
            isinstance(other, Stat)
            and self.flat == other.flat
            and self.percent == other.percent
        )
