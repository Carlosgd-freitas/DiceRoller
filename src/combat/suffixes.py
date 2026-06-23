"""Suffix Manager module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from src.combat.team import Team


class SuffixManager:
    """
    SuffixManager class.
    """

    def __init__(self):
        self.suffixes = {}

    def count_names(self, teams: List[Team]) -> Dict:
        """
        Counts the names of teams of monsters.

        :var teams: Teams of monsters.
        :vartype teams: List[Team]

        :return: A dictionary where each key is a name of a monster in combat and each
        value is the count of the monsters with this same name.
        :rtype: Dict
        """
        names = {}

        for team in teams:
            for monster in team.members:

                if monster.name not in names:
                    names[monster.name] = 1
                else:
                    names[monster.name] += 1

        return names

    def increase_character(self, character: str) -> Tuple[str, bool]:
        """
        Increases character by one:
        * If the character is not 'Z', returns the next character in the alphabet and
        False as a carry value.
        * If the character is 'Z', returns 'A' and True as a carry value.

        :param character: A single character.
        :type character: str

        :return: A (x, y) tuple where x is the increased character and y is a carry
        value.
        :rtype: Tuple[str, bool]
        """
        if len(character) != 1:
            raise ValueError("character length is not 1.")

        if character == "Z":
            return "A", True

        else:
            return chr(ord(character) + 1), False

    def increase_suffix(self, suffix: str) -> str:
        """
        Increases a suffix by one:
        * The last character in the suffix will be increased by one
        * If any character increase "carries over", than the character before that will
        also be increased by one

        Examples:
        * `increase_suffix("A")` = `"B"`
        * `increase_suffix("Z")` = `"AA"`
        * `increase_suffix("AZ")` = `"BA"`

        :param suffix: A monster suffix.
        :type suffix: str

        :return: The increased suffix.
        :rtype: str
        """
        if not suffix:
            return

        new_suffix = ""

        suffix: List[str] = [char for char in suffix]
        carry = True

        for char in reversed(suffix):
            if carry:
                new_char, carry = self.increase_character(char)
                new_suffix += new_char

            else:
                new_suffix += char

        new_suffix = "".join(reversed(new_suffix))
        if carry:
            new_suffix = "A" + new_suffix

        return new_suffix

    def add_suffixes(self, teams: List[Team]) -> None:
        """
        Add suffixes to monsters to differentiate them in combat.

        :var teams: Teams of monsters.
        :vartype teams: List[Team]
        """
        names = self.count_names(teams)

        for team in teams:
            for monster in team.members:
                if monster.name is None:
                    continue

                # Updating combat suffixes
                if (monster.name not in self.suffixes) and (names[monster.name] > 1):
                    self.suffixes[monster.name] = "A"

                elif names[monster.name] > 1:
                    self.suffixes[monster.name] = self.increase_suffix(
                        self.suffixes[monster.name]
                    )

                # Setting monster suffix
                if (monster.suffix is None) and (monster.name in self.suffixes):
                    monster.suffix = self.suffixes[monster.name]

        return None
