"""File Logger module."""

from src.base.color import Color, color_string
from src.base.text import normalize_filename
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

    def _get_log_file_start(self, filename: str = None) -> str:
        """."""
        if filename is None:
            message = self.get_message(
                namespace="menus",
                message_group="BASE",
                key="file",
            )
        else:
            message = filename

        return message

    def log_file_found(self, filename: str = None):
        """
        Logs a file that was found.

        :param filename: A filename to be included in the message.
        :type filename: str
        """
        message = self._get_log_file_start(filename)

        message += " " + self.get_message(
            namespace="menus",
            message_group="BASE",
            key="file_found",
            filename=filename,
        )

        message = color_string(f"[!] {message}", foreground_color=Color.WHITE)
        self.log(message=message)

    def log_file_load(self, filename: str = None):
        """
        Logs a file that was loaded.

        :param filename: A filename to be included in the message.
        :type filename: str
        """
        message = self._get_log_file_start(filename)

        message += " " + self.get_message(
            namespace="menus",
            message_group="BASE",
            key="file_load",
            filename=filename,
        )

        message = color_string(f"[!] {message}", foreground_color=Color.GREEN)
        self.log(message=message)

    def log_file_not_found(self, filename: str = None):
        """
        Logs a file that was not found.

        :param filename: A filename to be included in the message.
        :type filename: str
        """
        message = self._get_log_file_start(filename)

        message += " " + self.get_message(
            namespace="menus",
            message_group="BASE",
            key="file_not_found",
            filename=filename,
        )

        message = color_string(f"[!] {message}", foreground_color=Color.RED)
        self.log(message=message)

    def log_file_save(self, filename: str = None):
        """
        Logs a file that was saved.

        :param filename: A filename to be included in the message.
        :type filename: str
        """
        message = self._get_log_file_start(filename)

        message += " " + self.get_message(
            namespace="menus",
            message_group="BASE",
            key="file_save",
            filename=filename,
        )

        message = color_string(f"[!] {message}", foreground_color=Color.GREEN)
        self.log(message=message)

    def input_filename(self, extension: str) -> str:
        """
        Prompts the user to type a filename and returns it.

        :param extension: Filename extension, including the '.' (e.g. '.dat').
        :type extension: str

        :return: Normalized filename, inputted by the user.
        :rtype: str
        """
        message = self.get_message(
            namespace="menus",
            message_group="BASE",
            key="filename_prompt",
        )

        filename = self.input(message=message)
        filename = normalize_filename(filename, extension)

        return filename
