"""Edit Menu module."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, List

from src.base.text import normalize_filename
from src.logger.combat import CombatLogger
from src.menus.menu import Menu
from src.systems.file import FileManager
from src.systems.randomizer import Randomizer

if TYPE_CHECKING:
    from src.menus.option import Option
    from src.systems.settings import Settings


class EditMenu(Menu):
    """
    EditMenu class.

    :var settings: Game settings.
    :vartype settings: Settings

    :param message_group: Message group that contains the Menu messages.
    :type message_group: str

    :var logging: If logging is enabled. Default value is True.
    :vartype logging: bool

    :var file_manager: File Manager for importing and exporting options.
    :vartype file_manager: FileManager

    :var randomizer: Randomizer for randomizing options.
    :vartype randomizer: Randomizer
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        settings: Settings,
        message_group: str,
        logging: bool = True,
        file_manager: FileManager = None,
        randomizer: Randomizer = None,
    ):
        self.message_group = message_group

        logger = CombatLogger(enabled=logging, language=settings.language)
        super().__init__(
            logger,
            settings,
        )
        self.logger: CombatLogger

        self.file_manager = file_manager or FileManager()
        self.randomizer = randomizer or Randomizer()

        self.editing: Any = None

    def get_title(self) -> str:
        """
        Returns the Menu's title.

        :return: Menu title.
        :rtype: str
        """
        return self.logger.get_message(
            namespace="menus", message_group=self.message_group, key="title"
        )

    # =========================================================================
    # Options
    # =========================================================================

    def edit_attribute(self, attribute: str, type_cast: Any):
        """
        Edits an attribute of an object.

        :param attribute: Name of the attribute.
        :type attribute: str

        :param type_cast: Type of the attribute for proper casting and
        attribuition (e.g. str, int, float).
        :type type_cast: TypeVar
        """
        self.logger.log(message="")

        message = self.logger.get_message(
            namespace="menus",
            message_group=self.message_group,
            key=f"edit_{attribute}_prompt",
        )

        while True:
            try:
                value = self.logger.input(message=message)
                value = type_cast(value)

                if type_cast is float:
                    value = round(value, 2)

                break
            except Exception:
                continue

        self.editing.__setattr__(attribute, value)

        return

    def input_filename(self, extension: str) -> str:
        """
        Prompts the user to type a filename and returns it, normalized.

        :param extension: Filename extension, including the '.' (e.g. '.dat').
        :type extension: str

        :return: Normalized filename.
        :rtype: str
        """
        message = self.logger.get_message(
            namespace="menus",
            message_group="BASE",
            key="filename_prompt",
        )

        filename = self.logger.input(message=message)
        filename = normalize_filename(filename, extension)

        return filename

    def import_object(self, name: str, extension: str):
        """
        Prompts the user to type a filename and imports an object from a file with that
        filename, substituting the object being edited.

        :param name: Name of the object being imported.
        :type name: str

        :param extension: Filename extension, including the '.' (e.g. '.dat').
        :type extension: str
        """
        filename = self.input_filename(extension)

        loaded = self.file_manager.load_file(filename)

        if loaded:
            message = self.logger.get_message(
                namespace="menus",
                message_group=self.message_group,
                key=f"import_{name}_success",
            )
            self.editing = loaded

        else:
            message = self.logger.get_message(
                namespace="menus",
                message_group=self.message_group,
                key=f"import_{name}_fail",
            )

        self.logger.log(message=message)

        return

    def export_object(self, name: str, extension: str) -> bool:
        """
        Prompts the user to type a filename and exports the object being edited to a
        file with that filename.

        :param obj: Object to be exported.
        :type obj: Any

        :param name: Name of the object being exported.
        :type name: str

        :param extension: Filename extension, including the '.' (e.g. '.dat').
        :type extension: str

        :return: If the object was exported sucessfully.
        :rtype: bool
        """
        filename = self.input_filename(extension)

        saved = self.file_manager.save_file(filename, self.editing)

        if saved:
            message = self.logger.get_message(
                namespace="menus",
                message_group=self.message_group,
                key=f"export_{name}_success",
            )
        else:
            message = self.logger.get_message(
                namespace="menus",
                message_group=self.message_group,
                key=f"export_{name}_fail",
            )

        self.logger.log(message=message)

        return saved

    def select_attribute_option(self, options: List[Option], attribute: str) -> Option:
        """
        Prompts the user to select one option from a list, where each option contains
        an attribute of an object being edited.

        :param options: Options that can be selected by the user.
        :type options: List[Option]

        :param attribute: Name of the attribute.
        :type attribute: str

        :return: Option selected by the user.
        :rtype: Option
        """
        message = self.logger.get_message(
            namespace="menus",
            message_group=self.message_group,
            key=f"select_{attribute}_prompt",
        )

        selected_option: Option = self.select(options, message)

        return selected_option

    # =========================================================================
    # Rendering
    # =========================================================================

    @abstractmethod
    def show_editing_details(self):
        """
        Shows the details of the object being edited.
        """
        raise NotImplementedError

    def open(self, obj: Any):
        """
        Opens the Menu.

        :param obj: Object to be edited.
        :type obj: Any
        """
        self.editing = obj

        while True:
            self.show_title()

            self.show_editing_details()
            self.logger.log(message="")

            self.show_options(self.options)

            message = self.logger.get_message(
                namespace="menus",
                message_group="BASE",
                key="select_option_prompt",
            )
            selected = self.select(self.options, message)

            if self.is_option_valid(selected):
                self.process_option(selected)

            if selected.id in ["EXIT", "RETURN"]:
                break

        return self.editing
