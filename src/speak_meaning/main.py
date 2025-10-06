#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speak the Meaning of Word
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Application entry point. Launches the Tkinter GUI that fetches and speaks
the meaning of a user-provided word.

Usage:
python -m speak_meaning
# or
speak-meaning

Notes:
- Ensure dependencies are installed from requirements.txt or pyproject.toml.
=========================================================================================================
"""
from __future__ import annotations

from .gui import run_app


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
