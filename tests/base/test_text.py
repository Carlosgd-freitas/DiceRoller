"""Tests for text module methods."""

from math import inf

from src.base.text import (
    normalize,
    normalize_filename,
    numeric_to_string,
    unaccent,
)
from tests.utils import assert_conditions


def test_numeric_to_string():
    conditions = [
        numeric_to_string(None) is None,
        numeric_to_string("123") == "123",
        numeric_to_string(123) == "123",
        numeric_to_string(123.4) == "123.4",
        numeric_to_string(inf) == "∞",
    ]

    assert_conditions(conditions)


def test_unaccent():
    conditions = [
        unaccent(None) is None,
        unaccent("bola") == "bola",
        unaccent("PATO") == "PATO",
        unaccent("estátua") == "estatua",
        unaccent("ÁRVORE") == "ARVORE",
    ]

    assert_conditions(conditions)


def test_normalize():
    conditions = [
        normalize(None) is None,
        normalize("bola") == "bola",
        normalize("PATO") == "pato",
        normalize("estátua") == "estatua",
        normalize("ÁRVORE") == "arvore",
    ]

    assert_conditions(conditions)


def test_normalize_filename():
    conditions = [
        normalize_filename(None, ".png") is None,
        normalize_filename("pintura", None) is None,
        normalize_filename("cubo", ".txt") == "cubo.txt",
        normalize_filename("cubo.txt", ".txt") == "cubo.txt",
        normalize_filename("ONIBUS_AZUL", ".dat") == "onibus_azul.dat",
        normalize_filename("ÔNIBUS AZUL", ".dat") == "onibus_azul.dat",
    ]

    assert_conditions(conditions)
