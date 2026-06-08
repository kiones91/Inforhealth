#!/usr/bin/env python3
"""Injeta CTA final + footer premium (index) em todas as páginas do portal."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent / "site"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "closing_footer_snippet",
    Path(__file__).resolve().parent / "closing-footer-snippet.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
closing_zone_footer = _mod.closing_zone_footer

SKIP_FILES = {"index.html", "design_system.html"}
SKIP_DIRS = set()

OLD_FOOTER_RE = re.compile(
    r'\n  <footer class="px-8 lg:px-16 xl:px-24 py-8 border-t border-ih-primary/10 text-center">\s*'
    r'<p class="text-sm text-slate-400">© 2026 Inforhealth Educação e Excelência em Saúde</p>\s*'
    r'</footer>',
    re.DOTALL,
)

# Remove CTA customizado imediatamente antes do footer antigo
LEGACY_CTA_RE = re.compile(
    r'\n  <!-- (?:CTA|CTA banner|═══ CTA ═══).*?</section>\s*(?=\n  <footer class="px-8)',
    re.DOTALL,
)

GENERIC_PRIMARY_CTA_RE = re.compile(
    r'\n  <section class="px-8 lg:px-16 xl:px-24 pb-20">\s*'
    r'<div class="reveal(?: relative overflow-hidden rounded-\[24px\] bg-ih-primary| blog-article-banner).*?</section>\s*'
    r'(?=\n  <footer class="px-8)',
    re.DOTALL,
)

CLOSING_ZONE_RE = re.compile(
    r'\n<!-- CTA \+ FOOTER -->.*?</footer>\s*(?=</main>)',
    re.DOTALL,
)

WHATSAPP_OLD_RE = re.compile(
    r'<a href="https://wa\.me/5519997773084" class="(?:fixed bottom-6 right-6 z-50 flex items-center justify-center w-14 h-14 rounded-full bg-ih-accent text-white shadow-xl hover:scale-110 transition-transform|btn-glass btn-glass-accent btn-glass-fab fixed bottom-6 right-6 z-50 shadow-xl)" aria-label="WhatsApp">\s*'
    r'<iconify-icon icon="solar:chat-round-dots-bold" width="26"></iconify-icon>\s*</a>',
    re.DOTALL,
)

WHATSAPP_NEW = """<a href="https://wa.me/5519997773084" class="btn-glass btn-glass-accent btn-glass-fab fixed bottom-6 right-6 z-50 shadow-xl" aria-label="WhatsApp">
  <iconify-icon icon="solar:chat-round-dots-bold" width="26"></iconify-icon>
</a>"""


def is_redirect(content: str) -> bool:
    return 'http-equiv="refresh"' in content or "http-equiv='refresh'" in content


def asset_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("blog/artigos/"):
        return "../../"
    if rel.startswith("cursos/"):
        return "../"
    return ""


def patch_social_in_footer(path: Path) -> bool:
    """Insere redes sociais em footers premium já existentes."""
    text = path.read_text(encoding="utf-8")
    if "site-footer-social" in text or is_redirect(text):
        return False
    if "site-footer-bottom" not in text:
        return False
    social = _mod.footer_social_html()
    new = re.sub(
        r'(<div class="site-footer-bottom[^"]*">)\s*',
        r"\1\n" + social + "\n",
        text,
        count=1,
    )
    new = new.replace(
        "Capacitação estratégica em gestão, qualidade e compliance.",
        "Capacitação estratégica em gestão, qualidade e compliance · Campinas/SP",
    )
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def inject_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if is_redirect(text):
        return False
    if "closing-zone" in text and "site-footer" in text:
        return False

    prefix = asset_prefix(path)
    block = "\n" + closing_zone_footer(prefix) + "\n"

    # Remove bloco antigo se existir parcialmente
    text = CLOSING_ZONE_RE.sub("", text)
    text = LEGACY_CTA_RE.sub("", text)
    text = GENERIC_PRIMARY_CTA_RE.sub("", text)

    if not OLD_FOOTER_RE.search(text):
        return False

    text = OLD_FOOTER_RE.sub(block, text, count=1)
    text = WHATSAPP_OLD_RE.sub(WHATSAPP_NEW, text)
    path.write_text(text, encoding="utf-8")
    return True


def main():
    updated = []
    social_patched = []
    skipped = []
    for html in sorted(ROOT.rglob("*.html")):
        name = html.name
        if name == "design_system.html":
            skipped.append(html.relative_to(ROOT).as_posix())
            continue
        if inject_file(html):
            updated.append(html.relative_to(ROOT).as_posix())
        elif patch_social_in_footer(html):
            social_patched.append(html.relative_to(ROOT).as_posix())
    print(f"Footers novos: {len(updated)}")
    for p in updated:
        print(" ", p)
    print(f"Redes sociais inseridas: {len(social_patched)}")
    for p in social_patched:
        print(" ", p)
    if skipped:
        print(f"Ignorados: {len(skipped)}")


if __name__ == "__main__":
    main()
