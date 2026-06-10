#!/usr/bin/env python3
"""Aplica otimizações de Core Web Vitals (PageSpeed) em todas as páginas HTML do portal."""
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

# Regex para recursos bloqueadores
ICONIFY_RE = re.compile(
    r'<script\s+src="https://code\.iconify\.design/iconify-icon/2.1.0/iconify-icon\.min\.js"\s*></script>',
    re.I
)
FONTS_RE = re.compile(
    r'<link\s+href="https://fonts\.googleapis\.com/css2\?([^"]*?display=swap)"\s+rel="stylesheet"/>',
    re.I
)

# Regex para reflow forçado (Layout Thrashing)
LAYOUT_THRASH_RE = re.compile(
    r"const\s+r\s*=\s*el\.getBoundingClientRect\(\);\s*if\s*\(r\.top\s*<\s*innerHeight\s*&&\s*r\.bottom\s*>\s*0\)\s*el\.classList\.add\('animate'\);\s*else\s*aosObs\.observe\(el\);",
    re.DOTALL
)

# Regex para logotipo do cabeçalho sem dimensões
LOGO_RE = re.compile(
    r'<img\s+([^>]*?)src="([^"]*?logo-inforhealth-2020\.(?:webp|png))"([^>]*?)>',
    re.I
)


def css_prefix(rel: str) -> str:
    depth = len(Path(rel).parts) - 1
    return "../" * depth if depth else ""


def is_redirect(content: str) -> bool:
    return 'http-equiv="refresh"' in content or "http-equiv='refresh'" in content


def minify_css(content: str) -> str:
    # Remove comentários
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    # Remove espaços em branco desnecessários
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'\s*([:;{},])\s*', r'\1', content)
    return content.strip()


def inject_logo_dimensions(match):
    attrs_before = match.group(1)
    src_val = match.group(2)
    attrs_after = match.group(3)
    
    all_attrs = attrs_before + attrs_after
    if "width=" in all_attrs or "height=" in all_attrs:
        return match.group(0) # Já possui dimensões
        
    attrs_after_clean = attrs_after.rstrip().rstrip("/")
    return f'<img {attrs_before}src="{src_val}"{attrs_after_clean} width="120" height="38"/>'


def main() -> None:
    # 1. Minificar o design-system.css
    ds_css_path = SITE / "css" / "design-system.css"
    ds_min_path = SITE / "css" / "design-system.min.css"
    
    if ds_css_path.exists():
        css_content = ds_css_path.read_text(encoding="utf-8")
        min_css = minify_css(css_content)
        ds_min_path.write_text(min_css, encoding="utf-8")
        print(f"CSS minificado criado em {ds_min_path.name} ({len(css_content)/1024:.1f}KB -> {len(min_css)/1024:.1f}KB)")
    else:
        print("Aviso: site/css/design-system.css não encontrado para minificação.")

    # 2. Processar páginas HTML
    updated = 0
    for html in sorted(SITE.rglob("*.html")):
        text = html.read_text(encoding="utf-8", errors="replace")
        
        if is_redirect(text):
            continue
            
        new = text
        prefix = css_prefix(html.relative_to(SITE).as_posix())
        
        # Otimização 1: Substituição de Tailwind CDN (original)
        if "cdn.tailwindcss.com" in new:
            link = f'  <link href="{prefix}css/tailwind.min.css" rel="stylesheet"/>\n'
            new = TAILWIND_CDN.sub("\n", new)
            new = TAILWIND_CONFIG.sub("\n", new)
            new = TAILWIND_LINK.sub("\n", new)
            
            if "tailwind.min.css" not in new:
                ds = f'href="{prefix}css/design-system.css"'
                ds_min = f'href="{prefix}css/design-system.min.css"'
                
                if ds in new:
                    new = new.replace(
                        f'<link href="{prefix}css/design-system.css" rel="stylesheet"/>',
                        link.rstrip() + f'\n  <link href="{prefix}css/design-system.css" rel="stylesheet"/>',
                        1,
                    )
                elif ds_min in new:
                    new = new.replace(
                        f'<link href="{prefix}css/design-system.min.css" rel="stylesheet"/>',
                        link.rstrip() + f'\n  <link href="{prefix}css/design-system.min.css" rel="stylesheet"/>',
                        1,
                    )
        
        # Otimização 2: Substituir design-system.css por design-system.min.css
        new = new.replace("css/design-system.css", "css/design-system.min.css")

        # Otimização 3: Defer no script do Iconify
        new = ICONIFY_RE.sub(
            r'<script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js" defer></script>',
            new
        )

        # Otimização 4: Google Fonts de forma assíncrona (non-blocking)
        font_repl = (
            r'<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?\1" />\n'
            r'  <link href="https://fonts.googleapis.com/css2?\1" rel="stylesheet" media="print" onload="this.media=\'all\'" />'
        )
        new = FONTS_RE.sub(font_repl, new)

        # Otimização 5: Correção de Layout Thrashing no Intersection Observer
        new = LAYOUT_THRASH_RE.sub("aosObs.observe(el);", new)

        # Otimização 6: Dimensões explícitas no logotipo
        new = LOGO_RE.sub(inject_logo_dimensions, new)

        if new != text:
            html.write_text(new, encoding="utf-8")
            updated += 1

    print(f"Otimizações de performance aplicadas em {updated} páginas HTML.")


if __name__ == "__main__":
    main()
