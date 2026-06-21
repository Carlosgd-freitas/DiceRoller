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

try:
    # Settings
    settings = Settings()

    if file_manager.exists(SETTINGS_FILENAME):
        settings_data = file_manager.load(SETTINGS_FILENAME)
        settings.__dict__.update(settings_data.__dict__)

    # Main Menu
    menu = MainMenu(settings=settings)
    menu.open()

except Exception as e:
    traceback.print_exc()
    input()
    raise e
