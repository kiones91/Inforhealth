#!/usr/bin/env python3
"""Injeta menu mobile (hambúrguer + drawer) em todas as páginas HTML do portal."""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent / "site"
SCRIPTS = Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location("nav_snippet", SCRIPTS / "nav-snippet.py")
_nav = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_nav)

SKIP_FILES = {"curso.html", "blog-artigo.html", "blog-artigo-drg.html", "blog-artigo-ona.html", "blog-artigo-seguranca.html"}

DESKTOP_CLASS_RE = re.compile(
    r'(<div class=")(?:site-nav-desktop )?hidden lg:flex items-center gap-5(">)',
)

CORRUPT_DESKTOP_RE = re.compile(
    r'<div class="site-nav-desktop hidden lg:flex items-center gap-5hidden lg:flex items-center gap-5\s*\n',
)

WHATSAPP_GLASS_RE = re.compile(
    r'\n\s*<a class="btn-glass btn-glass-accent btn-glass-sm" href="https://wa\.me/5519997773084">\s*'
    r'<iconify-icon icon="solar:phone-linear" width="14"></iconify-icon> WhatsApp\s*'
    r'</a>\s*\n\s*</nav>\s*\n\s*</header>',
    re.DOTALL,
)

WHATSAPP_LEGACY_RE = re.compile(
    r'\n\s*<a class="inline-flex items-center gap-2 bg-ih-accent hover:bg-ih-accent-dark text-white text-xs font-medium px-4 py-2 rounded-full transition-colors" href="https://wa\.me/5519997773084">\s*'
    r'<iconify-icon icon="solar:phone-linear" width="14"></iconify-icon> WhatsApp\s*'
    r'</a>\s*\n\s*</nav>\s*\n\s*</header>',
    re.DOTALL,
)

OLD_DRAWER_RE = re.compile(
    r'\n\s*<div id="site-mobile-nav" class="site-mobile-nav".*?</div>\s*(?=\n)',
    re.DOTALL,
)

SCRIPT_RE = re.compile(r'\n<script src="[^"]*js/mobile-nav\.js"></script>')


def is_redirect(content: str) -> bool:
    return 'http-equiv="refresh"' in content or "http-equiv='refresh'" in content


def asset_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("blog/artigos/"):
        return "../../"
    if rel.startswith("cursos/"):
        return "../"
    return ""


def _desktop_class_repl(match: re.Match[str]) -> str:
    return f'{match.group(1)}site-nav-desktop hidden lg:flex items-center gap-5{match.group(2)}'


def patch_header(text: str) -> tuple[str, bool]:
    changed = False
    new_text, n = CORRUPT_DESKTOP_RE.subn(
        '<div class="site-nav-desktop hidden lg:flex items-center gap-5">\n',
        text,
    )
    if n:
        text = new_text
        changed = True

    if "site-nav-toggle" in text:
        if 'class="site-nav-desktop hidden lg:flex items-center gap-5">' not in text:
            new_text, n = DESKTOP_CLASS_RE.subn(_desktop_class_repl, text, count=1)
            if n:
                text = new_text
                changed = True
        return text, changed

    text, n = DESKTOP_CLASS_RE.subn(_desktop_class_repl, text, count=1)
    if not n and 'site-nav-desktop hidden lg:flex' not in text:
        return text, False

    actions = _nav.nav_actions_html()
    drawer = _nav.mobile_drawer_html()

    new_text, n = WHATSAPP_GLASS_RE.subn(f"\n{actions}\n    </nav>\n  </header>\n{drawer}", text, count=1)
    if n:
        return new_text, True

    new_text, n = WHATSAPP_LEGACY_RE.subn(
        f"\n{_nav.nav_actions_html('btn-glass btn-glass-accent btn-glass-sm')}\n    </nav>\n  </header>\n{drawer}",
        text,
        count=1,
    )
    if n:
        return new_text, True

    return text, False


def patch_script(path: Path, text: str) -> tuple[str, bool]:
    prefix = asset_prefix(path)
    tag = _nav.mobile_nav_script_tag(prefix)
    text = SCRIPT_RE.sub("", text)
    if tag in text:
        return text, False
    if "</body>" not in text:
        return text, False
    return text.replace("</body>", f"\n{tag}\n</body>", 1), True


def process_file(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return False
    text = path.read_text(encoding="utf-8")
    if is_redirect(text) or "hidden lg:flex items-center gap-5" not in text and "site-nav-toggle" not in text:
        return False

    original = text
    text, _ = patch_header(text)
    text, _ = patch_script(path, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = 0
    for html in sorted(ROOT.rglob("*.html")):
        if process_file(html):
            updated += 1
            print(f"  ok {html.relative_to(ROOT)}")
    print(f"\n{updated} arquivo(s) atualizado(s).")


if __name__ == "__main__":
    main()
