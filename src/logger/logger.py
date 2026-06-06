"""Logger module."""

from importlib import import_module
from typing import Dict, Literal

from src.base.color import color_string
from src.base.keywords import Keyword, get_keyword_color
from src.locales.languages import Language

type Namespace = Literal[
    "base",
    "combat",
    "effects",
]


type MessageGroup = Literal[
    # Base
    "ATTRIBUTES",
    "WORDS",
    # Combat
    "COMBAT",
    # Effects
    "ACTIONS",
    "ACTIVATION",
    "DAMAGE",
    "DESCRIPTION",
    "EXECUTION",
    "EXECUTION_FAIL",
    "FAILS",
    "KEYWORDS",
    "REMOVAL",
    "STATUS",
    "TYPES",
]


class Logger:
    """
    Logger class.

    :var enabled: If the Logger will log the messages. Default value is True.
    :vartype enabled: bool

    :var language: What language will be logged. Default value is Language.EN_US.
    :vartype language: Language
    """

    def __init__(
        self,
        enabled: bool = True,
        language: Language = Language.EN_US,
    ):
        self.enabled = enabled
        self.change_language(language)

    def change_language(self, language: Language):
        """
        .
        """
        self.language = language
        # self.language_module = import_module(f"src.locales.{language.value}")

    def get_message(
        self,
        namespace: Namespace,
        message_group: MessageGroup,
        key: str,
        **kwargs,
    ) -> str | None:
        """
        Gets a message from a locale's namespace.

        :param namespace: The namespace.
        :type namespace: Namespace

        :param message_group: The message group.
        :type message_group: MessageGroup

        :param key: The message key.
        :type key: str

        :return: A message.
        :rtype: str
        """
        module = import_module(f"src.locales.{self.language.value}.{namespace}")
        messages: Dict = getattr(module, message_group)
        message: str = messages.get(key)

        if message:
            message = message.format(**kwargs)

        return message

    def get_colored_message(
        self,
        namespace: Namespace,
        message_group: MessageGroup,
        keyword: Keyword,
    ) -> str | None:
        """
        Returns a colored message based on a Keyword.
        """
        color_data = get_keyword_color(keyword)

        message = color_string(
            self.get_message(
                namespace=namespace,
                message_group=message_group,
                key=keyword.value.lower(),
            ),
            **color_data,
        )

        return message

    def log(
        self,
        message: str = None,
        namespace: Namespace = None,
        message_group: MessageGroup = None,
        key: str = None,
        end: str = "\n",
        **kwargs,
    ) -> None:
        """
        Logs a message in the output.

        :param message: If a message is passed as a parameter, it will be logged
        directly.
        :type message: str

        :param namespace: The namespace.
        :type namespace: Namespace

        :param message_group: The message group.
        :type message_group: MessageGroup

        :param key: The message key.
        :type key: str

        :param end: What will be printed at the end of the message. Default value is
        \\n.
        :type end: str
        """
        if not self.enabled:
            return

        if namespace and message_group and key:
            message: str = self.get_message(
                namespace,
                message_group,
                key,
                **kwargs,
            )

        print(message, end=end)

        return

    def input(
        self,
        message: str = None,
        namespace: Namespace = None,
        message_group: MessageGroup = None,
        key: str = None,
        **kwargs,
    ) -> str:
        """
        Gets an input with a message.

        :param message: If a message is passed as a parameter, it will be logged
        directly before awaiting for input.
        :type message: str

        :param namespace: The namespace.
        :type namespace: Namespace

        :param message_group: The message group.
        :type message_group: MessageGroup

        :param key: The message key.
        :type key: str

        :return: The user's input.
        :rtype: str
        """
        if not self.enabled:
            return

        if namespace and message_group and key:
            message: str = self.get_message(
                namespace,
                message_group,
                key,
                **kwargs,
            )

        return input(message)
