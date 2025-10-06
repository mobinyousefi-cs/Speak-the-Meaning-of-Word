#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speak the Meaning of Word
File: dictionary.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Dictionary utilities built on top of PyDictionary with sensible formatting, caching,
and graceful error handling.

Usage:
from speak_meaning.dictionary import lookup_word
defs, syns, ants = lookup_word("algorithm")

Notes:
- PyDictionary relies on WordNet and web sources; responses can vary by connectivity.
- Network calls are wrapped and sanitized; callers should expect None/empty outputs on failures.
=========================================================================================================
"""
from __future__ import annotations

from functools import lru_cache
from typing import Dict, List, Tuple, Optional

try:
    from PyDictionary import PyDictionary  # type: ignore
except Exception:  # pragma: no cover - import-time environment issues
    PyDictionary = None  # type: ignore


class DictionaryClient:
    """Thin wrapper around PyDictionary with formatting helpers."""

    def __init__(self) -> None:
        if PyDictionary is None:
            raise RuntimeError(
                "PyDictionary is not available. Please install it via `pip install PyDictionary`."
            )
        self._client = PyDictionary()

    @staticmethod
    def _normalize_word(word: str) -> str:
        return (word or "").strip().lower()

    @lru_cache(maxsize=512)
    def meanings(self, word: str) -> Dict[str, List[str]]:
        word = self._normalize_word(word)
        if not word:
            return {}
        try:
            meanings = self._client.meaning(word) or {}
            # Ensure values are lists of strings
            return {
                pos: [d for d in defs if isinstance(d, str) and d.strip()]
                for pos, defs in meanings.items()
                if isinstance(defs, list)
            }
        except Exception:
            return {}

    @lru_cache(maxsize=512)
    def synonyms(self, word: str) -> List[str]:
        word = self._normalize_word(word)
        if not word:
            return []
        try:
            syns = self._client.synonym(word) or []
            return sorted({s.strip() for s in syns if isinstance(s, str) and s.strip()})
        except Exception:
            return []

    @lru_cache(maxsize=512)
    def antonyms(self, word: str) -> List[str]:
        word = self._normalize_word(word)
        if not word:
            return []
        try:
            ants = self._client.antonym(word) or []
            return sorted({a.strip() for a in ants if isinstance(a, str) and a.strip()})
        except Exception:
            return []

    def lookup(self, word: str) -> Tuple[Dict[str, List[str]], List[str], List[str]]:
        return self.meanings(word), self.synonyms(word), self.antonyms(word)


def format_meanings(meanings: Dict[str, List[str]]) -> str:
    """Render meanings dict to a human-friendly text block."""
    if not meanings:
        return "No definitions found."
    lines: List[str] = []
    for pos, defs in sorted(meanings.items()):
        lines.append(f"{pos}:")
        for i, d in enumerate(defs[:10], start=1):
            lines.append(f"  {i}. {d}")
        lines.append("")  # spacing between parts of speech
    return "\n".join(lines).strip()


def format_word_summary(
    word: str, meanings: Dict[str, List[str]], syns: List[str], ants: List[str]
) -> str:
    blocks: List[str] = [f"Word: {word}\n"]
    blocks.append("Definitions:\n" + format_meanings(meanings))
    if syns:
        blocks.append("\nSynonyms:\n" + ", ".join(syns[:20]))
    if ants:
        blocks.append("\nAntonyms:\n" + ", ".join(ants[:20]))
    return "\n".join(blocks).strip()


# Public API
def lookup_word(word: str) -> Tuple[Dict[str, List[str]], List[str], List[str]]:
    client = DictionaryClient()
    return client.lookup(word)
