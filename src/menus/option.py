"""Option module."""

from typing import Any


class Option:
    """
    Option Class.

    :var id: Option identifier.
    :vartype id: str

    :var key: Key that needs to be pressed to select the Option.
    :vartype key: str

    :var message: Message that will be logged when displaying the Option.
    :vartype message: str

    :var obj: Optional bject to be associated to the option.
    :vartype obj: Any

    :var isolate_before: If a \\n will be logged before the Option's message. Default
    value is False.
    :vartype isolate_before: bool

    :var isolate_after: If a \\n will be logged after the Option's message. Default
    value is False.
    :vartype isolate_after: bool
    """

    def __init__(
        self,
        id: str,
        key: str,
        message: str,
        obj: Any = None,
        isolate_before: bool = None,
        isolate_after: bool = None,
    ):
        self.id = id
        self.key = key
        self.message = message
        self.obj = obj
        self.isolate_before = isolate_before
        self.isolate_after = isolate_after
