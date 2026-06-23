"""File module."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.base.manager import Manager
from src.logger.file import FileLogger

if TYPE_CHECKING:
    from src.systems.settings import Settings


class FileManager(Manager):
    """
    FileManager class.

    :var settings: Game settings.
    :vartype settings: Settings

    :var logging: If logging is enabled. Default value is True.
    :vartype logging: bool
    """

    def __init__(
        self,
        settings: Settings,
        logging: bool = True,
    ):
        # Initialization
        logger = FileLogger(enabled=logging)

        super().__init__(
            logger,
            settings,
        )

        self.logger: FileLogger

    def exists(self, filename: str) -> bool:
        """
        Checks if a file exists.

        :param filename: Filename.
        :type filename: str

        :return: If the file exists or not.
        :rtype: bool
        """
        file_path = Path(filename)

        return file_path.is_file()

    def save(self, data: Any, filename: str):
        """
        Save data to a file.

        :param data: Data that will be saved.
        :type data: Any

        :param filename: Filename.
        :type filename: str
        """
        with open(filename, "wb") as f:
            pickle.dump(data, f)

        return

    def load(self, filename: str) -> Any | None:
        """
        Load data from a file.

        :param filename: Filename.
        :type filename: str

        :return: Data from a file.
        :rtype: Any
        """
        data = None

        if self.exists(filename):
            with open(filename, "rb") as f:
                data: Any = pickle.load(f)

        return data
