from colorama import init

from src.locales.languages import Language
from src.logger.logger import Logger
from src.menus.main_menu import MainMenu

init()

logger = Logger(language=Language.EN_US)
menu = MainMenu(logger=logger)
menu.open()
