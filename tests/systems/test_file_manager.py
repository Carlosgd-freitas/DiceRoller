"""Tests for FileManager class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.systems.file import FileManager

FILENAME = "file_manager_tests.dat"
FILEDATA = {
    "test": "file_manager_tests",
}


def test_file_manager_save(managers: Dict):
    file_manager: FileManager = managers["file_manager"]

    try:
        file_manager.save(FILEDATA, FILENAME)
        suceeded = True
    except Exception:
        suceeded = False

    conditions = [
        suceeded is True,
    ]

    assert_conditions(conditions)


def test_file_manager_exists(managers: Dict):
    file_manager: FileManager = managers["file_manager"]

    try:
        file_manager.exists(FILENAME)
        suceeded = True
    except Exception:
        suceeded = False

    conditions = [
        suceeded is True,
    ]

    assert_conditions(conditions)


def test_file_manager_load(managers: Dict):
    file_manager: FileManager = managers["file_manager"]

    try:
        loaded_data = file_manager.load(FILENAME)
        suceeded = True
    except Exception:
        suceeded = False

    conditions = [
        suceeded is True,
        loaded_data == FILEDATA,
    ]

    assert_conditions(conditions)
