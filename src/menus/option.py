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

    :var isolate: If the Option will be logged before and after a \\n. Default value is
    False.
    :vartype isolate: bool
    """

    def __init__(
        self,
        id: str,
        key: str,
        message: str,
        isolate: bool = False,
    ):
        self.id = id
        self.key = key
        self.message = message
        self.isolate = isolate
