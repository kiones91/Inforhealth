#!/usr/bin/env python3
"""Baixa imagens do WordPress (i0.wp.com) para assets/imagens/blog/ e atualiza referências."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SITE = REPO / "site"
BLOG_IMG = REPO / "assets" / "imagens" / "blog"
JSON_PATH = SITE / "js" / "blog-posts.json"

WP_RE = re.compile(r"https?://i0\.wp\.com/([^?\s\"'<>]+)(?:\?[^\"\s'<>]*)?")
WP_FIND = re.compile(r"https?://i0\.wp\.com/[^\s\"'<>]+")


def wp_url_to_local(url: str) -> tuple[str, str]:
    """Retorna (caminho local relativo a assets/imagens, url original limpa)."""
    m = WP_RE.match(url)
    if not m:
        return "", url
    raw = urllib.parse.unquote(m.group(1))
    # edu.inforhealth.com.br/wp-content/uploads/2023/02/file.png
    parts = raw.split("/wp-content/uploads/", 1)
    if len(parts) == 2:
        rel = "blog/" + parts[1]
    else:
        # fallback por hash
        h = hashlib.md5(url.encode()).hexdigest()[:10]
        ext = Path(raw).suffix or ".jpg"
        rel = f"blog/external/{h}{ext}"
    return rel, url


def origin_from_i0(url: str) -> str:
    """i0.wp.com/edu.inforhealth.com.br/wp-content/... -> https://edu.../wp-content/..."""
    m = WP_RE.match(url)
    if not m:
        return url.split("?")[0]
    return "https://" + urllib.parse.unquote(m.group(1))


def download_candidates(url: str) -> list[str]:
    origin = origin_from_i0(url)
    base = origin.split("?")[0]
    return list(dict.fromkeys([origin, base, url.split("?")[0]]))


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return True
    for candidate in download_candidates(url):
        try:
            req = urllib.request.Request(candidate, headers={"User-Agent": "Inforhealth-SEO-Bot/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            if len(data) < 200:
                continue
            dest.write_bytes(data)
            return True
        except Exception:
            continue
    print(f"  ERRO download: {url[:90]}...")
    return False


def replace_in_text(text: str, mapping: dict[str, str]) -> str:
    for old, new in mapping.items():
        text = text.replace(old, new)
    return text


def main() -> None:
    mapping: dict[str, str] = {}
    urls = set()

    for f in SITE.rglob("*"):
        if f.suffix in {".html", ".json"}:
            content = f.read_text(encoding="utf-8", errors="replace")
            for m in WP_FIND.finditer(content):
                urls.add(m.group(0).rstrip(")"))

    print(f"URLs WordPress encontradas: {len(urls)}")

    ok = 0
    for url in sorted(urls):
        rel, _ = wp_url_to_local(url)
        if not rel:
            continue
        dest = REPO / "assets" / "imagens" / rel
        # Caminho web relativo conforme profundidade será aplicado depois; guardamos padrão
        web_path = f"/assets/imagens/{rel.replace(chr(92), '/')}"
        if download(url, dest):
            mapping[url] = web_path
            ok += 1

    print(f"Imagens baixadas/ok: {ok}/{len(urls)}")

    # Substituir em HTML — caminhos relativos por profundidade
    html_count = 0
    for f in SITE.rglob("*.html"):
        text = f.read_text(encoding="utf-8", errors="replace")
        if "i0.wp.com" not in text:
            continue
        depth = len(f.relative_to(SITE).parts) - 1
        prefix = "../" * (depth + 1)  # site/foo.html -> ../ ; site/blog/artigos/x -> ../../
        local_map: dict[str, str] = {}
        for old, web in mapping.items():
            rel_path = web.lstrip("/assets/imagens/")
            local_map[old] = f"{prefix}assets/imagens/{rel_path}"
            local_map[old.split("?")[0]] = f"{prefix}assets/imagens/{rel_path}"
        new_text = replace_in_text(text, local_map)
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            html_count += 1

    if JSON_PATH.exists():
        data = JSON_PATH.read_text(encoding="utf-8")
        local_map = {}
        for old, web in mapping.items():
            local_map[old] = web
            local_map[old.split("?")[0]] = web
        new_data = replace_in_text(data, local_map)
        if new_data != data:
            JSON_PATH.write_text(new_data, encoding="utf-8")
            print("blog-posts.json atualizado")

    print(f"HTML atualizados: {html_count}")
    remaining = sum(1 for f in SITE.rglob("*.html") if "i0.wp.com" in f.read_text(encoding="utf-8", errors="replace"))
    print(f"Referencias i0.wp.com restantes: {remaining}")


if __name__ == "__main__":
    main()
