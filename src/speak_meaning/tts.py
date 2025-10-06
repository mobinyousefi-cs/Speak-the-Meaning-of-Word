#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speak the Meaning of Word
File: tts.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Thin wrapper around pyttsx3 for offline text-to-speech with safe defaults.

Usage:
from speak_meaning.tts import speak_text
speak_text("Hello world", rate=180, volume=0.9)

Notes:
- pyttsx3 is offline and uses platform-specific engines (SAPI5 on Windows, NSSpeechSynth on macOS, eSpeak on Linux).
- Speaking is synchronous; call from a thread if you don't want to block the GUI.
=========================================================================================================
"""
from __future__ import annotations

import pyttsx3
from typing import Optional


def _engine() -> pyttsx3.Engine:
    eng = pyttsx3.init()
    # Conservative defaults
    eng.setProperty("rate", 175)
    eng.setProperty("volume", 0.9)
    return eng


def speak_text(text: str, rate: Optional[int] = None, volume: Optional[float] = None) -> None:
    if not text:
        return
    eng = _engine()
    if rate is not None:
        eng.setProperty("rate", rate)
    if volume is not None:
        eng.setProperty("volume", volume)
    eng.say(text)
    eng.runAndWait()
    eng.stop()
