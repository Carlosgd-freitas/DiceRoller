"""Main game file."""

from colorama import init

from src.menus.main_menu import MainMenu
from src.systems.settings import Settings

# Colorama
init()

try:
    # Settings
    settings = Settings()

    if settings.exists():
        settings.load()

    # Main Menu
    menu = MainMenu(settings=settings)
    menu.open()

except Exception as e:
    input(e)
    raise e
