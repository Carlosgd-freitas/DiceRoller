"""Script for building game executables."""

import subprocess

subprocess.run(
    ["pyinstaller", "DiceRoller.spec"],
    check=True,
)
