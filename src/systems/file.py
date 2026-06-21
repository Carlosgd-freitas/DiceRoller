"""File module."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from src.base.text import normalize


class FileManager:
    """
    File Manager class.
    """

    def normalize_filename(self, filename: str, extension: str) -> str:
        """
        Normalizes a filename.

        :param filename: Filename.
        :type filename: str

        :param extension: Filename extension, including the '.' (e.g. '.dat').
        :type extension: str
        """
        normalized = normalize(filename)

        if not normalized.endswith(extension):
            normalized += extension

        return normalized

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
        """
        data = None

        if self.exists(filename):
            with open(filename, "rb") as f:
                data: Any = pickle.load(f)

        return data
