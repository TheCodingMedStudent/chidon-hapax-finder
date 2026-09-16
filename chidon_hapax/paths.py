"""Where things live, running from source or frozen into an .exe / .app.

PyInstaller unpacks the bundled files into a temporary folder it names in
``sys._MEIPASS``; ``__file__`` points somewhere useless there. And that folder
is read-only — as is Program Files and the inside of a signed ``.app`` — so
anything the program *writes* has to go to the user's own data directory
instead.
"""

from __future__ import annotations

import os
import sys


def frozen() -> bool:
    """True when running from a PyInstaller bundle."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def resource(*parts: str) -> str:
    """A file shipped with the program (corpus, stylesheet, icon)."""
    if frozen():
        base = sys._MEIPASS                      # type: ignore[attr-defined]
        return os.path.join(base, "chidon_hapax", *parts)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *parts)


def user_data_dir() -> str:
    """A writable per-user folder, created on demand.

    Windows  %APPDATA%\\ChidonHapaxFinder
    macOS    ~/Library/Application Support/ChidonHapaxFinder
    Linux    ~/.local/share/ChidonHapaxFinder  (or $XDG_DATA_HOME)
    """
    name = "ChidonHapaxFinder"
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = (os.environ.get("XDG_DATA_HOME")
                or os.path.expanduser("~/.local/share"))
    path = os.path.join(base, name)
    os.makedirs(path, exist_ok=True)
    return path


def writable_data(*parts: str) -> str:
    """Somewhere the program may write — a rebuilt corpus, for instance."""
    path = os.path.join(user_data_dir(), *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path
