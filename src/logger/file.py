"""File Logger module."""

from src.logger.logger import Logger


class FileLogger(Logger):
    """
    FileLogger class.
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
