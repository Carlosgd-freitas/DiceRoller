"""File Manager module."""

from __future__ import annotations

import os
import pickle
import shutil
from functools import wraps
from inspect import signature
from pathlib import Path
from typing import Any


def treat_path(path: str | Path) -> Path:
    """
    Converts the path to a filesystem path object if it is not already one.

    :param path: Path.
    :type path: str | Path

    :return: Filesystem path object.
    :rtype: Path
    """
    if isinstance(path, str):
        path = Path(path)
    return path


def safe_file_operation(*, default: Any = False):
    """
    Decorator for FileManager methods that:
    * Converts a "path" argument to a Path object, if present.
    * Returns a default value if an exception occurs.
    """

    def decorator(func):
        sig = signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            if "path" in bound.arguments:
                bound.arguments["path"] = treat_path(bound.arguments["path"])

            try:
                return func(*bound.args, **bound.kwargs)
            except Exception:
                return default

        return wrapper

    return decorator


class FileManager:
    """
    FileManager class.
    """

    @safe_file_operation()
    def exists(self, path: str | Path) -> bool:
        """
        Checks if a file or directory exists.

        :param path: File or directory path.
        :type path: str | Path

        :return: If the file or directory exists.
        :rtype: bool
        """
        return path.exists()

    @safe_file_operation()
    def create_directory(self, path: str | Path) -> bool:
        """
        Creates a directory, if it does not exists.

        :param path: Directory path.
        :type path: str | Path

        :return: If the directory was created.
        :rtype: bool
        """
        if not self.exists(path):
            path.mkdir(parents=True, exist_ok=True)
            return True

        return False

    @safe_file_operation()
    def delete(self, path: str | Path) -> bool:
        """
        Deletes a directory, if it exists.

        :param path: Directory path.
        :type path: str | Path

        :return: If the directory was deleted.
        :rtype: bool
        """
        if self.exists(path):
            if path.is_file():
                os.remove(path)
                return True
            elif path.is_dir():
                shutil.rmtree(path)
                return True

        return False

    @safe_file_operation()
    def save_file(self, filename: str, data: Any, mode: str = "wb") -> bool:
        """
        Save data to a file.

        :param filename: Filename.
        :type filename: str

        :param data: Data that will be saved.
        :type data: Any

        :param mode: Opening file mode. Default value is "wb" (write bytes).
        :type mode: str

        :return: If the data was saved in the file sucessfully.
        :rtype: bool
        """
        with open(filename, mode) as f:
            pickle.dump(data, f)
        return True

    @safe_file_operation(default=None)
    def load_file(self, filename: str, mode: str = "rb") -> Any | None:
        """
        Load data from a file.

        :param filename: Filename.
        :type filename: str

        :param mode: Opening file mode. Default value is "rb" (read bytes).
        :type mode: str

        :return: Data from a file.
        :rtype: Any
        """
        if self.exists(filename):
            with open(filename, mode) as f:
                data: Any = pickle.load(f)
                return data

        return
