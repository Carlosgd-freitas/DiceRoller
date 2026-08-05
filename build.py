"""Script for building game executables."""

import subprocess

from src.base.constants import VERSION

subprocess.run(
    [
        "pyinstaller",
        "--onedir",
        "--name",
        f"DiceRoller_{VERSION}",
        "main.py",
    ]
)
