#!/usr/bin/env python3
"""Gera sitemap.xml com todas as URLs públicas indexáveis."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_lib import SITE_ROOT, is_redirect_page, load_config, page_kind, path_to_url, rel_site_path  # noqa: E402


def priority_for(kind: str, config: dict) -> str:
    pmap = config["sitemap"]["priority"]
    return {
        "home": pmap["home"],
        "cursos": pmap["cursos"],
        "curso": pmap["curso"],
        "blog_list": pmap["blog_list"],
        "blog_article": pmap["blog_article"],
    }.get(kind, pmap["institutional"])


def changefreq_for(kind: str, config: dict) -> str:
    cmap = config["sitemap"]["changefreq"]
    return {
        "home": cmap["home"],
        "cursos": cmap["cursos"],
        "curso": cmap["curso"],
        "blog_list": cmap["blog_list"],
        "blog_article": cmap["blog_article"],
    }.get(kind, cmap["institutional"])


def main() -> None:
    config = load_config()
    site_url = config["site_url"]
    today = date.today().isoformat()

    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    count = 0

    for html_file in sorted(SITE_ROOT.rglob("*.html")):
        rel = rel_site_path(html_file)
        content = html_file.read_text(encoding="utf-8", errors="replace")
        kind = page_kind(rel)

        if kind in {"redirect", "internal"}:
            continue
        if is_redirect_page(content):
            continue
        if 'content="noindex' in content:
            continue

        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = path_to_url(site_url, rel)
        ET.SubElement(url, "lastmod").text = today
        ET.SubElement(url, "changefreq").text = changefreq_for(kind, config)
        ET.SubElement(url, "priority").text = priority_for(kind, config)
        count += 1

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    out = SITE_ROOT / "sitemap.xml"
    tree.write(out, encoding="utf-8", xml_declaration=True)
    print(f"sitemap.xml gerado com {count} URLs -> {out}")


if __name__ == "__main__":
    main()
