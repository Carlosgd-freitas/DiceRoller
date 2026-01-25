"""
Colored impression of strings.
Needs a previously executed colorama.init() to work.
"""

from enum import Enum
from typing import Tuple, Literal


class ANSICode(Enum):
    "ANSI codes for various text components."
    FOREGROUND = "\033[38;2;"
    BACKGROUND = "\033[48;2;"

    # Intensity
    BRIGHT = "\033[1m"
    DIM = "\033[2m"
    SLOW_BLINK = "\033[5m"
    RAPID_BLINK = "\033[6m"

    # Styles
    ITALIC = "\033[3m"
    UNDERLINED = "\033[4m"
    INVERT = "\033[7m"
    CONCEAL = "\033[8m"
    STRIKETHROUGH = "\033[9m"

    RESET = "\033[0m"


class Color(Enum):
    "A color represented with its' RGB values in a 3-integer tuple format."
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    GRAY = (128, 128, 128)
    SILVER = (74, 78, 80)
    DARK_GRAY = (64, 64, 64)
    BURGUNDY = (128, 0, 32)
    RED_CLAY = (194, 69, 45)
    TOMATO = (255, 99, 71)
    PEACH_PINK = (255, 154, 138)
    SALMON = (250, 127, 114)
    MANGO = (255, 191, 52)
    ORANGE = (250, 143, 1)
    METALLIC_ORANGE = (218, 104, 15)
    BRONZE_YELLOW = (111, 112, 17)
    GOLD = (212, 175, 55)
    VOLT = (206, 255, 0)
    LEMON = (255, 244, 79)
    PEARL = (234, 224, 200)
    BEIGE = (208, 176, 132)
    DURIAN = (176, 121, 57)
    BRONZE = (136, 84, 11)
    COFFEE = (159, 78, 55)
    BROWN = (87, 44, 2)
    BISTRE = (61, 43, 31)
    EMERALD_GREEN = (4, 99, 7)
    OLIVE = (107, 142, 35)
    PEAR = (209, 226, 49)
    GRASS_GREEN = (124, 252, 0)
    CELADON = (172, 225, 175)
    SPRING_GREEN = (0, 255, 127)
    TURQUOISE = (64, 224, 208)
    JADE = (0, 168, 107)
    TEAL = (0, 128, 128)
    AERO = (124, 185, 232)
    SKY_BLUE = (0, 187, 255)
    METALLIC_BLUE = (50, 82, 123)
    DARK_NAVY = (2, 7, 93)
    LILAC = (204, 153, 255)
    VIOLET = (127, 0, 255)
    INDIGO = (91, 0, 161)
    PURPLE = (147, 18, 172)
    JAM = (165, 11, 94)
    HOT_PINK = (252, 3, 152)
    RUBY = (224, 17, 95)
    PINK = (255, 153, 204)


def get_color_code(color: Tuple[int, int, int] | Color) -> str:
    "Returns a RGB-based code from a code."

    if isinstance(color, tuple) and len(color) == 3:
        return f"{color[0]};{color[1]};{color[2]}m"
    elif isinstance(color, Color):
        return f"{color.value[0]};{color.value[1]};{color.value[2]}m"
    else:
        raise ValueError("'color' parameter must be either a Tuple of 3 integers or of Color class")


def color_string(
    string: str,
    foreground_color: Tuple[int, int, int] | Color = (255, 255, 255),
    background_color: Tuple[int, int, int] | Color = (12, 12, 12),
    intensity: Literal["BRIGHT", "DIM", "SLOW_BLINK", "RAPID_BLINK"] = "BRIGHT",
    italic: bool = False,
    underlined: bool = False,
    inverted: bool = False,
    concealed: bool = False,
    strikethrough: bool = False,
) -> str:
    """
    Colors and returns a string.

    Parameters:
    * string: string that will be colored. If this parameter is not a string, a cast to string will
    be attemped so the coloring can be applied.

    Optional Parameter:
    * foreground_color: color that will be used on the string itself. Default value is (255, 255, 255), 
        which is the terminal's default white.
    * background_color: color that will be used on the background. Default value is (12, 12, 12), 
        which is the terminal's default black.
    * intensity: intensity of the string itself, which can be 'BRIGHT', 'DIM', 'SLOW_BLINK' or
        'RAPID_BLINK'. Default value is 'BRIGHT'.
    * italic: if the text will be in italic or not. Default value is False.
    * underlined: if the text will be underlined or not. Default value is False.
    * inverted: if the text will be inverted or not. Default value is False.
    * concealed: if the text will be concealed or not. Default value is False.
    * strikethrough: if the text will be strikethrough or not. Default value is False.
    """
    try:
        string = str(string)
    except:
        raise Exception("'string' parameter is neither a string or can be casted to string")

    parts = []

    # Text intensity
    if intensity == "BRIGHT":
        parts.append(ANSICode.BRIGHT.value)
    elif intensity == "DIM":
        parts.append(ANSICode.DIM.value)
    elif intensity == "SLOW_BLINK":
        parts.append(ANSICode.SLOW_BLINK.value)
    elif intensity == "RAPID_BLINK":
        parts.append(ANSICode.RAPID_BLINK.value)

    # Text style
    if italic:
        parts.append(ANSICode.ITALIC.value)
    if underlined:
        parts.append(ANSICode.UNDERLINED.value)
    if inverted:
        parts.append(ANSICode.INVERT.value)
    if concealed:
        parts.append(ANSICode.CONCEAL.value)
    if strikethrough:
        parts.append(ANSICode.STRIKETHROUGH.value)

    # Text colors
    parts.append(ANSICode.FOREGROUND.value + get_color_code(foreground_color))
    parts.append(ANSICode.BACKGROUND.value + get_color_code(background_color))

    return "".join(parts) + string + ANSICode.RESET.value
