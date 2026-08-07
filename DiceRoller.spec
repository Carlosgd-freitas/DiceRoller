# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

project_dir = Path.cwd()
sys.path.insert(0, str(project_dir))

from src.base.constants import VERSION


hiddenimports = []

locales_dir = project_dir / "src" / "locales"

for language_dir in locales_dir.iterdir():
    if not language_dir.is_dir():
        continue

    for module in language_dir.glob("*.py"):
        if module.stem == "__init__":
            continue

        hiddenimports.append(
            f"src.locales.{language_dir.name}.{module.stem}"
        )


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=f'DiceRoller_{VERSION}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=f'DiceRoller_{VERSION}',
)
