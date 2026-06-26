"""Option module."""


class Option:
    """
    Option Class.

    :var id: Option identifier.
    :vartype id: str

    :var key: Key that needs to be pressed to select the Option.
    :vartype key: str

    :var message: Message that will be logged when the Option is selected.
    :vartype message: str

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
        isolate_before: bool = None,
        isolate_after: bool = None,
    ):
        self.id = id
        self.key = key
        self.message = message
        self.isolate_before = isolate_before
        self.isolate_after = isolate_after
