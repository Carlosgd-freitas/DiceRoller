# DiceRoller
A dice rolling roguelike game made in Python.

## Download

You can download the latest pre-built versions from the [Releases](../../releases) page.

### Windows

1. Download the Windows archive:

   `DiceRoller_0.2.0_windows.zip`

2. Extract the ZIP file.

3. Run:

       DiceRoller_0.2.0.exe

**Note:** Please disregard any security warnings, as the game isn't currently code signed.

### Linux

1. Download the Linux archive:
   
   `DiceRoller_0.2.0_linux.tar.gz`

2. Extract it:

       tar -xzf DiceRoller_0.2.0_linux.tar.gz

3. Start the game:

       ./DiceRoller_0.2.0/DiceRoller_0.2.0

**Note:** If needed, use `chmod +x` to give executable permission to the game file.

## Planned Updates
* **v0.3.0:** Roguelike Mode, Playable Classes
* **v0.4.0:** Items (Consumables & Equipment), Shops
* **v0.5.0:** Skills, Events
* **v0.6.0:** Save System, Achievements, Unlocks

## Modding: Getting Started
This project uses **Python 3.14.4**, be sure to use this or another compatible version.
* To install the necessary packages, use: `pip install -r requirements.txt`
* To enable code formatting and linting packages on commit, use: `pre-commit install`
* To build the game executable for the OS in-use, use: `python build.py`
