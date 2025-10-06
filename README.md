# Speak the Meaning of Word

A minimalist Tkinter app that **fetches** and **speaks** the meaning of a word, with synonyms and antonyms, powered by **PyDictionary** and **pyttsx3**.

## Features
- Fast lookup (WordNet + web-backed via PyDictionary)
- Clean GUI with threaded requests (no UI freezes)
- Offline TTS via `pyttsx3`
- Synonyms & antonyms summary

## Installation

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
