# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build for Chidon HaTanach — Hapax Finder.

    pyinstaller chidon_hapax.spec

Produces dist/Hapax Finder/ on Windows and dist/Hapax Finder.app on macOS.
--onedir (the default here) rather than --onefile: a single-file executable
unpacks itself to a temporary folder at every launch, which is slower and is
what most antivirus heuristics flag.
"""

import os
import sys
from PyInstaller.utils.hooks import collect_submodules

# macOS only. PyQt6-Qt6 ships separate x86_64 and arm64 wheels rather than a
# universal2 one, so a universal2 build is impossible: PyInstaller cannot fuse
# an app out of single-architecture Qt libraries. Build once per architecture
# instead, on a runner of that architecture. Leave unset to build for whatever
# machine you are on.
TARGET_ARCH = os.environ.get("HAPAX_TARGET_ARCH") or None

APP_NAME = "Hapax Finder"                     # Dock, taskbar and menu bar
BUNDLE_ID = "com.danielmechoulan.hapaxfinder"
VERSION = "1.0.0"                             # .app/.exe want four-part numbers

block_cipher = None

# Everything the program reads at runtime. paths.resource() looks for these
# under chidon_hapax/ inside the bundle, so the destinations must match.
datas = [
    ("chidon_hapax/data/tanach.json.gz", "chidon_hapax/data"),
    ("chidon_hapax/style.qss",           "chidon_hapax"),
    ("chidon_hapax/icons",               "chidon_hapax/icons"),
    ("LICENSE",                          "."),
    ("README.md",                        "."),
]

# Qt ships a great deal we never touch. Dropping it roughly halves the build.
excludes = [
    "PyQt6.QtWebEngineCore", "PyQt6.QtWebEngineWidgets", "PyQt6.QtWebEngine",
    "PyQt6.QtQml", "PyQt6.QtQuick", "PyQt6.QtQuick3D", "PyQt6.QtMultimedia",
    "PyQt6.QtMultimediaWidgets", "PyQt6.QtBluetooth", "PyQt6.QtNetworkAuth",
    "PyQt6.QtPositioning", "PyQt6.QtSensors", "PyQt6.QtSerialPort",
    "PyQt6.QtTest", "PyQt6.QtSql", "PyQt6.QtDesigner", "PyQt6.QtHelp",
    "PyQt6.Qt3DCore", "PyQt6.Qt3DRender", "PyQt6.QtCharts",
    "tkinter", "unittest", "pydoc", "doctest", "test",
    "numpy", "scipy", "pandas", "matplotlib", "PIL",
]

a = Analysis(
    ["run.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=collect_submodules("chidon_hapax"),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                 # UPX compression is itself an antivirus trigger
    console=False,             # no terminal window behind the GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=TARGET_ARCH,    # see the note at the top of this file
    codesign_identity=None,
    entitlements_file=None,
    icon="chidon_hapax/icons/app.ico" if sys.platform == "win32"
         else "chidon_hapax/icons/app.icns",
    version="version_info.txt" if sys.platform == "win32" else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=APP_NAME,
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name=f"{APP_NAME}.app",
        icon="chidon_hapax/icons/app.icns",
        bundle_identifier=BUNDLE_ID,
        version=VERSION,
        info_plist={
            "CFBundleName": APP_NAME,
            "CFBundleDisplayName": APP_NAME,     # what the Dock shows
            "CFBundleShortVersionString": VERSION,
            "CFBundleVersion": VERSION,
            "NSHumanReadableCopyright":
                "Copyright © 2026 Daniel Mechoulan. GPL-3.0-or-later.",
            "NSHighResolutionCapable": True,     # sharp on Retina
            "LSApplicationCategoryType": "public.app-category.education",
            "LSMinimumSystemVersion": "11.0",
        },
    )
