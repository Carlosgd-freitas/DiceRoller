"""Logger module."""

from importlib import import_module
from typing import Dict, List, Literal, get_args

from src.base.color import Color, color_string
from src.base.keywords import Keyword, get_keyword_color
from src.locales.languages import Language

Namespace = Literal[
    "base",
    "combat",
    "compendium",
    "effect_types",
    "effects",
    "menus",
    "monsters",
    "settings",
]


class Logger:
    """
    Logger class.

    :var enabled: If the Logger will log the messages. Default value is True.
    :vartype enabled: bool

    :var language: What language will be logged. Default value is Language.EN_US.
    :vartype language: Language

    :var max_length: Max length of a logged message. If the length of a message exceed
    this limit, it will be broken into multiple lines. Default value is 200.
    :vartype max_length: int
    """

    def __init__(
        self,
        enabled: bool = True,
        language: Language = Language.EN_US,
        max_length: int = 200,
    ):
        self._messages = {}
        self.enabled = enabled
        self.change_language(language)
        self.max_length = max_length

    def _load_messages(self, language: Language) -> Dict:
        """
        Loads all messages from a locale module.

        :var language: Language of the messages that will be loaded.
        :vartype language: Language
        """
        self.language = language
        _messages = {}

        for namespace in get_args(Namespace):
            module = import_module(f"src.locales.{language.value}.{namespace}")
            _messages[namespace] = {}

            for name, value in vars(module).items():
                if isinstance(value, dict):
                    _messages[namespace][name] = value

        return _messages

    def change_language(self, language: Language, _messages: Dict = None):
        """
        Changes the Logger's language.

        :var language: A Language.
        :vartype language: Language
        """
        self.language = language

        if not _messages:
            _messages = self._load_messages(language)

        self._messages = _messages

    def get_message_group(
        self,
        namespace: Namespace,
        message_group: str,
        **kwargs,
    ) -> Dict | None:
        """
        Gets a message group from a locale's namespace.

        :param namespace: The namespace.
        :type namespace: Namespace

        :param message_group: The message group.
        :type message_group: str

        :param key: The message key.
        :type key: str

        :return: A message.
        :rtype: str
        """
        namespace: Dict = self._messages.get(namespace)

        if namespace:
            message_group: Dict = namespace.get(message_group)

            if message_group:
                return message_group

        return

    def get_message(
        self,
        namespace: Namespace,
        message_group: str,
        key: str,
        **kwargs,
    ) -> str | None:
        """
        Gets a message from a locale's namespace and message group.

        :param namespace: The namespace.
        :type namespace: Namespace

        :param message_group: The message group.
        :type message_group: str

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
        keyword: Keyword,
        message: str = None,
        namespace: Namespace = None,
        message_group: str = None,
        key: str = None,
        **kwargs,
    ) -> str | None:
        """
        Returns a colored message based on a Keyword.

        :param keyword: A keyword which color will be applied to the message.
        :type keyword: Keyword

        :param message: If a message is passed as a parameter, it will be logged
        directly.
        :type message: str

        :param namespace: The namespace.
        :type namespace: Namespace

        :param message_group: The message group.
        :type message_group: str

        :param key: The message key.
        :type key: str

        :return: A colored message based on a Keyword.
        :rtype: str
        """
        color_data = get_keyword_color(keyword)

        if namespace and message_group and key:
            message: str = self.get_message(
                namespace,
                message_group,
                key,
                **kwargs,
            )

        if message:
            message = color_string(
                message,
                **color_data,
            )

        return message

    def pluralize(
        self,
        number: int,
        namespace: Namespace,
        message_group: str,
        key: str,
    ) -> str:
        """
        Gets a message in either singular or plural format.

        :param number: Number that will determined the message. If equal to 1, the
        singular format will be returned, and otherwise, the plural format will.
        :type number: int

        :param namespace: The namespace.
        :type namespace: Namespace

        :param message_group: The message group.
        :type message_group: str

        :param key: The message key.
        :type key: str

        :return: A message in either singular or plural format.
        :rtype: str
        """
        if number == 1:
            return self.get_message(
                namespace=namespace,
                message_group=message_group,
                key=key,
            )
        else:
            return self.get_message(
                namespace=namespace,
                message_group=message_group,
                key=key + "s",
            )

    def break_message(
        message: str,
        max_length: int,
        break_long_words: bool = False,
    ) -> List[str]:
        """
        Break a message into lines whose length is at most max_length. Existing line
        breaks are preserved.

        :var message: The message that will be broken into smaller parts.
        :vartype message: str

        :var max_length: Maximum length of each part of the message.
        :vartype max_length: int

        :var break_long_words: If words longer than max_length will be kept intact or
        also broken into smaller parts. Default value is False.
        :vartype break_long_words: bool

        :return: Message parts.
        :rtype: List[str]
        """
        if max_length <= 0:
            raise ValueError("max_length must be positive")

        result = []

        for paragraph in message.splitlines():
            if not paragraph:
                result.append("")
                continue

            current = ""

            for word in paragraph.split():
                if break_long_words and len(word) > max_length:
                    if current:
                        result.append(current)
                        current = ""

                    for i in range(0, len(word), max_length):
                        result.append(word[i : i + max_length])

                    continue

                if not current:
                    current = word
                elif len(current) + len(word) + 1 <= max_length:
                    current += f" {word}"
                else:
                    result.append(current)
                    current = word

            if current:
                result.append(current)

        return result

    def log(
        self,
        message: str = None,
        namespace: Namespace = None,
        message_group: str = None,
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
        :type message_group: str

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
        message_group: str = None,
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
        :type message_group: str

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

        if message:
            message = "> " + message + ": "

        return input(message)

    def box_message(
        self,
        message: str,
        size: int,
        alignment: Literal["left", "center", "right"] = "center",
        isolate: bool = True,
    ) -> None:
        """
        Logs a message inside a box.

        :param message: A message.
        :type message: str

        :param size: The box size.
        :type size: int

        :param alignment: The message alignment. Default value is "left".
        :type alignment: Literal["left", "center", "right"

        :param isolate: If empty lines will be logged before and after the boxed
        message. Default value is True.
        :type isolate: bool
        """
        if not self.enabled:
            return

        if alignment == "left":
            alignment = "<"
        elif alignment == "center":
            alignment = "^"
        elif alignment == "right":
            alignment = ">"

        center_size = size - 2
        message_size = size - 4

        if isolate:
            self.log(message="")

        self.log(message="╔" + ("═" * center_size) + "╗")
        self.log(message="║ ", end="")
        self.log(message=f"{message:{alignment}{message_size}}", end="")
        self.log(message=" ║\n", end="")
        self.log(message="╚" + ("═" * center_size) + "╝")

        if isolate:
            self.log(message="")

        return

    def log_boolean(
        self,
        message: str,
        value: bool,
        end: str = "\n",
    ) -> None:
        """
        Logs a message that has an associated boolean value. If this value is
        * false, the message will be logged as bright and red.
        * true, the message will be logged as bright and green.

        :param message: A message.
        :type message: str

        :param value: The boolean value.
        :type value: bool

        :param end: What will be printed at the end of the message. Default value is
        \\n.
        :type end: str
        """
        if not value:
            message = color_string(
                message,
                foreground_color=Color.RED,
                intensity="BRIGHT",
            )

        else:
            message = color_string(
                message,
                foreground_color=Color.GREEN,
                intensity="BRIGHT",
            )

        self.log(message=message, end=end)

        return
