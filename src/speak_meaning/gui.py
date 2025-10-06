#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speak the Meaning of Word
File: gui.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Tkinter-based GUI for entering a word, fetching its definitions/synonyms/antonyms,
and speaking the result using pyttsx3. Uses a background thread to avoid blocking the UI.

Usage:
from speak_meaning.gui import run_app
run_app()

Notes:
- Network lookups are executed off the main thread; UI updates are marshalled onto Tk's mainloop.
- Minimal aesthetic with built-in Tk; keep dependencies lean.
=========================================================================================================
"""
from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from .dictionary import lookup_word, format_word_summary
from .tts import speak_text


class SpeakMeaningApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=12)
        self.master.title("Speak the Meaning of Word")
        self.master.geometry("720x520")
        self.master.minsize(640, 420)

        # State
        self._result_q: "queue.Queue[str]" = queue.Queue()
        self._lookup_thread: threading.Thread | None = None

        # Widgets
        self._build_widgets()
        self.pack(fill="both", expand=True)

        # Key bindings
        self.entry_word.bind("<Return>", lambda _e: self.on_search())

    def _build_widgets(self) -> None:
        # Top row: input + buttons
        row = ttk.Frame(self)
        row.pack(fill="x", pady=(0, 8))

        ttk.Label(row, text="Word:", width=8).pack(side="left")
        self.entry_word = ttk.Entry(row)
        self.entry_word.pack(side="left", fill="x", expand=True, padx=(4, 8))
        self.entry_word.focus_set()

        self.btn_search = ttk.Button(row, text="Define", command=self.on_search)
        self.btn_search.pack(side="left", padx=2)

        self.btn_speak = ttk.Button(row, text="Speak", command=self.on_speak, state="disabled")
        self.btn_speak.pack(side="left", padx=2)

        self.btn_clear = ttk.Button(row, text="Clear", command=self.on_clear)
        self.btn_clear.pack(side="left", padx=2)

        self.btn_exit = ttk.Button(row, text="Exit", command=self.master.destroy)
        self.btn_exit.pack(side="left", padx=2)

        # Text area with scrollbar
        frame_text = ttk.Frame(self)
        frame_text.pack(fill="both", expand=True)

        self.text = tk.Text(frame_text, wrap="word", undo=False)
        scroll = ttk.Scrollbar(frame_text, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)

        self.text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Status bar
        self.status = ttk.Label(self, text="Ready", anchor="w")
        self.status.pack(fill="x", pady=(6, 0))

    # UI helpers
    def _set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.btn_search.configure(state=state)
        self.btn_clear.configure(state=state)
        self.btn_exit.configure(state=state)
        self.entry_word.configure(state=state)
        self.status.configure(text="Looking up..." if busy else "Ready")
        self.master.configure(cursor="watch" if busy else "")

    def on_search(self) -> None:
        word = self.entry_word.get().strip()
        if not word:
            messagebox.showinfo("Info", "Please enter a word.")
            return

        if self._lookup_thread and self._lookup_thread.is_alive():
            return  # Avoid double-firing

        self._set_busy(True)
        self.text.delete("1.0", "end")
        self.btn_speak.configure(state="disabled")

        def worker() -> None:
            try:
                meanings, syns, ants = lookup_word(word)
                summary = format_word_summary(word, meanings, syns, ants)
            except Exception as e:  # Safety net
                summary = f"An error occurred while looking up the word:\n{e}"
            self._result_q.put(summary)

        self._lookup_thread = threading.Thread(target=worker, daemon=True)
        self._lookup_thread.start()
        self.after(75, self._poll_results)

    def _poll_results(self) -> None:
        try:
            summary = self._result_q.get_nowait()
        except queue.Empty:
            self.after(75, self._poll_results)
            return

        self.text.insert("1.0", summary + "\n")
        # Enable speak if we have something meaningful
        content = summary.strip().lower()
        can_speak = content and "error occurred" not in content
        self.btn_speak.configure(state="normal" if can_speak else "disabled")
        self._set_busy(False)

    def on_speak(self) -> None:
        content = self.text.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Info", "Nothing to speak.")
            return

        # Speak asynchronously to avoid blocking UI
        threading.Thread(target=speak_text, args=(content,), daemon=True).start()

    def on_clear(self) -> None:
        self.text.delete("1.0", "end")
        self.entry_word.delete(0, "end")
        self.btn_speak.configure(state="disabled")
        self.status.configure(text="Ready")


def run_app() -> None:
    root = tk.Tk()
    # Native look
    try:
        root.call("tk", "scaling", 1.2)
    except Exception:
        pass
    app = SpeakMeaningApp(root)
    app.mainloop()
