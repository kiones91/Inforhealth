#!/usr/bin/env python3
"""Substitui Tailwind CDN por CSS compilado (Core Web Vitals)."""
from __future__ import annotations

import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent.parent / "site"

TAILWIND_CDN = re.compile(
    r'\s*<script src="https://cdn\.tailwindcss\.com"></script>\s*',
    re.I,
)
TAILWIND_CONFIG = re.compile(
    r"\s*<script>\s*tailwind\.config\s*=\s*\{[\s\S]*?\}\s*</script>\s*",
    re.I,
)
TAILWIND_LINK = re.compile(r'\s*<link href="[^"]*css/tailwind\.min\.css" rel="stylesheet"/>\s*', re.I)


def css_prefix(rel: str) -> str:
    depth = len(Path(rel).parts) - 1
    return "../" * depth if depth else ""


def main() -> None:
    updated = 0
    for html in sorted(SITE.rglob("*.html")):
        if "cdn.tailwindcss.com" not in html.read_text(encoding="utf-8", errors="replace"):
            # ainda garante link compilado
            pass
        text = html.read_text(encoding="utf-8", errors="replace")
        prefix = css_prefix(html.relative_to(SITE).as_posix())
        link = f'  <link href="{prefix}css/tailwind.min.css" rel="stylesheet"/>\n'

        new = TAILWIND_CDN.sub("\n", text)
        new = TAILWIND_CONFIG.sub("\n", new)
        new = TAILWIND_LINK.sub("\n", new)

        if "tailwind.min.css" not in new:
            anchor = 'rel="stylesheet"/>'
            ds = f'href="{prefix}css/design-system.css"'
            if ds in new:
                new = new.replace(
                    f'<link href="{prefix}css/design-system.css" rel="stylesheet"/>',
                    link.rstrip() + f'\n  <link href="{prefix}css/design-system.css" rel="stylesheet"/>',
                    1,
                )
            elif anchor in new and "design-system.css" in new:
                new = re.sub(
                    r'(<link href="[^"]*design-system\.css" rel="stylesheet"/>)',
                    link.rstrip() + r"\n  \1",
                    new,
                    count=1,
                )

        if new != text:
            html.write_text(new, encoding="utf-8")
            updated += 1

    print(f"Tailwind compilado aplicado em {updated} paginas")


if __name__ == "__main__":
    main()
