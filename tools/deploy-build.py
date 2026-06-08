#!/usr/bin/env python3
"""Monta pasta dist/ para deploy (Cloudflare Pages, Netlify, etc.)."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
ASSETS = REPO / "assets"
DIST = REPO / "dist"


def win_long(path: Path) -> str:
    s = str(path.resolve())
    if os.name == "nt" and not s.startswith("\\\\?\\"):
        return "\\\\?\\" + s
    return s


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        with open(win_long(src), "rb") as fsrc, open(win_long(dst), "wb") as fdst:
            fdst.write(fsrc.read())
    else:
        shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    for root, _dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        out = dst / rel
        out.mkdir(parents=True, exist_ok=True)
        for name in files:
            copy_file(Path(root) / name, out / name)


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    for item in SITE.iterdir():
        dest = DIST / item.name
        if item.is_dir():
            copy_tree(item, dest)
        else:
            shutil.copy2(item, dest)

    copy_tree(ASSETS, DIST / "assets")
    total = sum(1 for _ in DIST.rglob("*") if _.is_file())
    print(f"Deploy pronto em {DIST} ({total} arquivos)")


if __name__ == "__main__":
    main()
