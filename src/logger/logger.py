"""Logger module."""

from importlib import import_module
from typing import Dict, Literal, get_args

from src.base.color import color_string
from src.base.keywords import Keyword, get_keyword_color
from src.locales.languages import Language

Namespace = Literal[
    "base",
    "combat",
    "effects",
]


MessageGroup = Literal[
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
    # On Multiple Namespaces
    "COMPENDIUM",
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
        self._messages = {}
        self.enabled = enabled
        self.change_language(language)

    def change_language(self, language: Language):
        """
        Changes the Logger's language. Loads all messages from a locale module.

        :var language: What language will be logged. Default value is Language.EN_US.
        :vartype language: Language
        """
        self.language = language
        self._messages = {}

        for namespace in get_args(Namespace):
            module = import_module(f"src.locales.{language.value}.{namespace}")
            self._messages[namespace] = {}

            for message_group in get_args(MessageGroup):
                namespace_message_group = getattr(module, message_group, None)
                if namespace_message_group:
                    self._messages[namespace][message_group] = namespace_message_group

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
        namespace: Dict = self._messages.get(namespace)

        if namespace:
            message_group: Dict = namespace.get(message_group)

            if message_group:
                message: str = message_group.get(key)

                if message:
                    message = message.format(**kwargs)
                    return message

        return

    def get_colored_message(
        self,
        namespace: Namespace,
        message_group: MessageGroup,
        keyword: Keyword,
    ) -> str | None:
        """
        Returns a colored message based on a Keyword.

        :param namespace: The namespace.
        :type namespace: Namespace

        :param message_group: The message group.
        :type message_group: MessageGroup

        :param keyword: A keyword that serves as the message key. The returned message
        will have the same colors as this keyword.
        :type keyword: Keyword

        :return: A colored message based on a Keyword.
        :rtype: str
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

        return input("> " + message + ": ")
