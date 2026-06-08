#!/usr/bin/env python3
"""Remove CTAs antigos que ficaram antes do bloco closing-zone."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent / "site"

LEGACY_COMMENT_CTA = re.compile(
    r'\n  <!-- (?:═══ CTA ═══|CTA|CTA banner).*?</section>\s*'
    r'(?=\n(?:  <!-- Footer -->\s*)?<!-- CTA \+ FOOTER -->)',
    re.DOTALL,
)

GENERIC_BEFORE_CLOSING = re.compile(
    r'\n  <section class="px-8 lg:px-16 xl:px-24 pb-20">.*?</section>\s*'
    r'(?=\n(?:  <!-- Footer -->\s*)?<!-- CTA \+ FOOTER -->)',
    re.DOTALL,
)

FOOTER_COMMENT = re.compile(r'\n  <!-- Footer -->\s*(?=<!-- CTA \+ FOOTER -->)')


def clean(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "closing-zone" not in text:
        return False
    orig = text
    text = LEGACY_COMMENT_CTA.sub("", text)
    text = GENERIC_BEFORE_CLOSING.sub("", text)
    text = FOOTER_COMMENT.sub("\n", text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for html in sorted(ROOT.rglob("*.html")):
        if clean(html):
            n += 1
            print(html.relative_to(ROOT).as_posix())
    print(f"Limpos: {n}")


if __name__ == "__main__":
    main()
