#!/usr/bin/env python3
"""Injeta canonical, Open Graph, Twitter Cards e JSON-LD em todas as páginas."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_lib import (  # noqa: E402
    SITE_ROOT,
    article_schema,
    breadcrumb_schema,
    build_seo_block,
    clean_title,
    course_schema,
    inject_ga4,
    inject_into_html,
    is_redirect_page,
    load_blog_index,
    load_config,
    local_business_schema,
    organization_schema,
    page_kind,
    path_to_url,
    rel_site_path,
    speakable_schema,
    truncate,
    website_schema,
)

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', re.I | re.S)

BLOG_PREV = {
    "blog-pagina-2.html": "blog.html",
    "blog-pagina-3.html": "blog-pagina-2.html",
}
BLOG_NEXT = {
    "blog.html": "blog-pagina-2.html",
    "blog-pagina-2.html": "blog-pagina-3.html",
}


def needs_title_fix(title: str) -> bool:
    """Corrige apenas títulos com artefatos de migração ou truncamento."""
    return bool(re.search(r"\(\s*$|—\s*Blog Inforhealth\s*$", title, re.I))


def parse_meta(content: str) -> tuple[str, str]:
    title_m = TITLE_RE.search(content)
    desc_m = DESC_RE.search(content)
    title = title_m.group(1).strip() if title_m else "Inforhealth Educação"
    desc = desc_m.group(1).strip() if desc_m else ""
    return title, desc


def course_slug_from_path(rel: str) -> str | None:
    m = re.match(r"cursos/(.+)\.html$", rel)
    return m.group(1) if m else None


def blog_slug_from_path(rel: str) -> str | None:
    m = re.match(r"blog/artigos/(.+)\.html$", rel)
    return m.group(1) if m else None


def build_page_seo(config: dict, rel: str, content: str, blog_index: dict) -> tuple[str, str | None, str | None]:
    site_url = config["site_url"]
    title, description = parse_meta(content)
    defaults = config.get("page_defaults", {}).get(rel, {})
    if not description and defaults.get("description"):
        description = defaults["description"]
    if defaults.get("title"):
        title = defaults["title"]

    title_clean = clean_title(title)
    canonical = path_to_url(site_url, rel)
    og_image = config["default_og_image"]
    og_type = "website"
    robots = defaults.get("robots")
    jsonld: list[dict] = []
    extra_html = ""

    kind = page_kind(rel)

    if kind == "redirect":
        robots = "noindex, follow"
        return (
            build_seo_block(
                config,
                canonical_url=canonical,
                title=title,
                description=description or title,
                robots=robots,
            ),
            title_clean if needs_title_fix(title) else None,
            description or None,
        )

    if kind == "internal":
        robots = defaults.get("robots", "noindex, nofollow")
        return (
            build_seo_block(
                config,
                canonical_url=canonical,
                title=title,
                description=description or "Design system interno.",
                robots=robots,
            ),
            None,
            description or None,
        )

    if kind == "home":
        jsonld = [
            organization_schema(config),
            local_business_schema(config),
            website_schema(config),
            speakable_schema(config, url=canonical, title=title_clean, description=description or title_clean),
        ]

    elif kind == "blog_article":
        slug = blog_slug_from_path(rel)
        post = blog_index.get(slug or "", {})
        if post.get("image"):
            og_image = post["image"]
        if not description and post.get("excerpt"):
            description = post["excerpt"]
        og_type = "article"
        cats = post.get("categories", [])
        jsonld.append(
            article_schema(
                config,
                title=title_clean,
                description=description,
                url=canonical,
                image=og_image if og_image.startswith("http") else path_to_url(site_url, og_image.lstrip("/")),
                date_published=post.get("date"),
                categories=cats,
            )
        )
        jsonld.append(
            breadcrumb_schema(
                config,
                [
                    ("Início", path_to_url(site_url, "index.html")),
                    ("Blog", path_to_url(site_url, "blog.html")),
                    (truncate(title_clean, 40), canonical),
                ],
            )
        )
        jsonld.append(
            speakable_schema(
                config,
                url=canonical,
                title=title_clean,
                description=description or title_clean,
            )
        )

    elif kind == "curso":
        slug = course_slug_from_path(rel)
        og_image = f"/assets/imagens/cursos/{slug}.png"
        if slug == "seguranca-do-paciente":
            og_image = "/assets/imagens/cursos/scih-seguranca-paciente.png"
        modality = "ao-vivo"
        if "mentoria" in rel or "mentoria" in title.lower():
            modality = "mentoria"
        elif "gravado" in title.lower() or "online" in title.lower():
            modality = "ao-vivo"
        jsonld.append(
            course_schema(
                config,
                title=title_clean,
                description=description,
                url=canonical,
                image=path_to_url(site_url, og_image.lstrip("/")),
                modality=modality,
            )
        )
        jsonld.append(
            breadcrumb_schema(
                config,
                [
                    ("Início", path_to_url(site_url, "index.html")),
                    ("Cursos", path_to_url(site_url, "cursos.html")),
                    (truncate(title_clean, 40), canonical),
                ],
            )
        )
        jsonld.append(
            speakable_schema(
                config,
                url=canonical,
                title=title_clean,
                description=description or title_clean,
            )
        )

    elif kind == "blog_list":
        if rel in BLOG_PREV:
            prev_url = path_to_url(site_url, BLOG_PREV[rel])
            extra_html = f'  <link rel="prev" href="{prev_url}">\n'
        if rel in BLOG_NEXT:
            next_url = path_to_url(site_url, BLOG_NEXT[rel])
            extra_html += f'  <link rel="next" href="{next_url}">\n'

    elif kind in {"cursos", "institutional"} and rel != "index.html":
        jsonld.append(
            breadcrumb_schema(
                config,
                [
                    ("Início", path_to_url(site_url, "index.html")),
                    (title_clean.split("—")[0].strip(), canonical),
                ],
            )
        )

    block = build_seo_block(
        config,
        canonical_url=canonical,
        title=title,
        description=description or title_clean,
        og_type=og_type,
        og_image=og_image,
        robots=robots,
        jsonld=jsonld,
    )
    new_title = title_clean if needs_title_fix(title) else None
    new_desc = (description or None) if not DESC_RE.search(content) else None
    return block + extra_html, new_title, new_desc


def main() -> None:
    config = load_config()
    blog_index = load_blog_index()
    updated = 0
    skipped_redirect = 0

    for html_file in sorted(SITE_ROOT.rglob("*.html")):
        rel = rel_site_path(html_file)
        content = html_file.read_text(encoding="utf-8")

        if is_redirect_page(content) and page_kind(rel) == "redirect":
            # Redirecionamentos legados: apenas noindex + canonical
            block, new_title, new_desc = build_page_seo(config, rel, content, blog_index)
            new_content = inject_into_html(content, block, new_title=new_title, new_description=new_desc)
            html_file.write_text(new_content, encoding="utf-8")
            skipped_redirect += 1
            continue

        block, new_title, new_desc = build_page_seo(config, rel, content, blog_index)
        new_content = inject_into_html(content, block, new_title=new_title, new_description=new_desc)
        new_content = inject_ga4(new_content, config)
        if new_content != content:
            html_file.write_text(new_content, encoding="utf-8")
            updated += 1

    print(f"SEO injetado: {updated} páginas de conteúdo")
    print(f"Redirecionamentos tratados: {skipped_redirect}")


if __name__ == "__main__":
    main()
