"""Main game file."""

import traceback

from colorama import init

from src.menus.main_menu import MainMenu
from src.systems.file import FileManager
from src.systems.settings import FILENAME as SETTINGS_FILENAME
from src.systems.settings import Settings

# Colorama
init()

file_manager = FileManager()
settings = Settings()

try:
    loaded_settings = file_manager.load_file(SETTINGS_FILENAME)

    if loaded_settings and isinstance(loaded_settings, Settings):
        settings = loaded_settings

    # Main Menu
    menu = MainMenu(settings=settings)
    menu.open()

except Exception as e:
    traceback.print_exc()
    input()
    raise e
