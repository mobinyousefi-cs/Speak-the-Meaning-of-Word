#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic unit tests for dictionary formatting helpers.
Network calls are avoided by stubbing DictionaryClient methods.
"""
import builtins
import types

import pytest

from speak_meaning import __version__
from speak_meaning.dictionary import format_meanings, format_word_summary


def test_version_semver_like():
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)


def test_format_meanings_empty():
    assert format_meanings({}) == "No definitions found."


def test_format_meanings_blocks():
    meanings = {
        "Noun": ["a thing", "another meaning"],
        "Verb": ["to do something"],
    }
    text = format_meanings(meanings)
    assert "Noun:" in text and "Verb:" in text
    assert "1. a thing" in text


def test_format_word_summary_contains_sections():
    m = {"Noun": ["first meaning"]}
    syns = ["term1", "term2"]
    ants = ["opposite"]
    out = format_word_summary("test", m, syns, ants)
    assert "Word: test" in out
    assert "Definitions:" in out
    assert "Synonyms:" in out
    assert "Antonyms:" in out
