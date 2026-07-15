"""Main game file."""

import traceback

from colorama import init

from src.menus.main_menu import MainMenu
from src.systems.file import FileManager
from src.systems.settings import FILENAME as SETTINGS_FILENAME
from src.systems.settings import Settings

# Colorama
init()

settings = Settings()

# Player settings
try:
    file_manager = FileManager(settings, logging=False)

    if file_manager.exists(SETTINGS_FILENAME):
        settings_data = file_manager.load_file(SETTINGS_FILENAME)
        settings.__dict__.update(settings_data.__dict__)

    # Main Menu
    menu = MainMenu(settings=settings)
    menu.open()

except Exception as e:
    traceback.print_exc()
    input()
    raise e
