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
DIRNAME = "file_manager_tests"


def test_file_manager_create_directory(managers: Dict):
    file_manager: FileManager = managers["file_manager"]

    created_0 = file_manager.create_directory(DIRNAME)
    created_1 = file_manager.create_directory(DIRNAME)

    conditions = [
        created_0 is True,
        created_1 is False,
    ]

    assert_conditions(conditions)


def test_file_manager_save(managers: Dict):
    file_manager: FileManager = managers["file_manager"]

    saved = file_manager.save_file(FILENAME, FILEDATA)

    conditions = [
        saved is True,
    ]

    assert_conditions(conditions)


def test_file_manager_exists(managers: Dict):
    file_manager: FileManager = managers["file_manager"]

    created_0 = file_manager.exists(DIRNAME)
    created_1 = file_manager.exists(DIRNAME + "xyz")
    created_2 = file_manager.exists(FILENAME)
    created_3 = file_manager.exists(FILENAME + "xyz")

    conditions = [
        created_0 is True,
        created_1 is False,
        created_2 is True,
        created_3 is False,
    ]

    assert_conditions(conditions)


def test_file_manager_load(managers: Dict):
    file_manager: FileManager = managers["file_manager"]

    loaded_data_0 = file_manager.load_file(DIRNAME)
    loaded_data_1 = file_manager.load_file(DIRNAME + "xyz")
    loaded_data_2 = file_manager.load_file(FILENAME)
    loaded_data_3 = file_manager.load_file(FILENAME + "xyz")

    conditions = [
        loaded_data_0 is None,
        loaded_data_1 is None,
        loaded_data_2 == FILEDATA,
        loaded_data_3 is None,
    ]

    assert_conditions(conditions)


def test_file_manager_delete(managers: Dict):
    file_manager: FileManager = managers["file_manager"]

    deleted_0 = file_manager.delete(DIRNAME)
    deleted_1 = file_manager.delete(DIRNAME + "xyz")
    deleted_2 = file_manager.delete(FILENAME)
    deleted_3 = file_manager.delete(FILENAME + "xyz")

    conditions = [
        deleted_0 is True,
        deleted_1 is False,
        deleted_2 is True,
        deleted_3 is False,
    ]

    assert_conditions(conditions)
