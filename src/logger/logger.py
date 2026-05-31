"""Logger module."""

from typing import Dict, Literal

from src.base.color import color_string
from src.base.keywords import Keyword, get_keyword_color
from src.logger.languages import en_us, pt_br

LANGUAGES = {
    "EN-US": en_us,
    "PT-BR": pt_br,
}

type LoggingCategory = Literal[
    # Combat
    "ACTIONS",
    "ATTRIBUTES",
    "COMBAT",
    "DAMAGE",
    "EFFECT_ACTIVATION",
    "EFFECT_EXECUTION",
    "EFFECT_REMOVAL",
    "KEYWORDS",
    "STATUS",
]


class Logger:
    """
    Logger class.

    :var enabled: If the Logger will log the messages. Default value is True.
    :vartype enabled: bool

    :var language: What language will be logged. Default value is "EN-US".
    :vartype language: Literal["EN-US", "PT-BR"]
    """

    def __init__(
        self,
        enabled: bool = True,
        language: str = "EN-US",
    ):
        self.enabled = enabled
        self.language = language

    def get_message(
        self,
        category: LoggingCategory,
        key: str,
        **kwargs,
    ) -> str | None:
        """
        Gets a message from a language module.

        :param category: The message category.
        :type category: LoggingCategory

        :param key: The message key.
        :type key: str

        :return: A message.
        :rtype: str
        """
        language_module = LANGUAGES[self.language]
        messages: Dict = getattr(language_module, category)
        message: str = messages.get(key)

        if message:
            message = message.format(**kwargs)

        return message

    def get_colored_message(
        self,
        category: str,
        keyword: Keyword,
    ) -> str | None:
        """
        Returns a colored message based on a Keyword.
        """
        color_data = get_keyword_color(keyword)

        message = color_string(
            self.get_message(
                category=category,
                key=keyword.value.lower(),
            ),
            **color_data,
        )

        return message

    def log(
        self,
        message: str = None,
        category: LoggingCategory = None,
        key: str = None,
        end: str = "\n",
        **kwargs,
    ) -> None:
        """
        Logs a message in the output.

        :param message: If a message is passed as a parameter, it will be logged
        directly.
        :type message: str

        :param category: The message category from a language module.
        :type category: LoggingCategory

        :param key: The message key from a language module.
        :type key: str

        :param end: What will be printed at the end of the message. Default value is
        \\n.
        :type end: str
        """
        if not self.enabled:
            return

        if category and key:
            message: str = self.get_message(category, key, **kwargs)

        print(message, end=end)

        return
