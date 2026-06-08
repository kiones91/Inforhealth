"""Biblioteca central de SEO — Portal Inforhealth."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_ROOT = REPO_ROOT / "site"
CONFIG_PATH = Path(__file__).resolve().parent / "seo-config.json"

SEO_BEGIN = "<!-- SEO:BEGIN -->"
SEO_END = "<!-- SEO:END -->"
ANALYTICS_BEGIN = "<!-- ANALYTICS:BEGIN -->"
ANALYTICS_END = "<!-- ANALYTICS:END -->"

REDIRECT_RE = re.compile(r'<meta\s+http-equiv=["\']refresh["\']', re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', re.I | re.S)
ROBOTS_RE = re.compile(r'<meta\s+name=["\']robots["\']', re.I)


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def truncate(text: str, max_len: int) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:-") + "…"


def clean_title(raw: str, site_name: str = "Inforhealth") -> str:
    title = re.sub(r"\s+", " ", raw.strip())
    title = re.sub(r"\s*—\s*Blog Inforhealth\s*$", "", title, flags=re.I)
    title = re.sub(r"\s*—\s*Inforhealth Educação\s*$", "", title, flags=re.I)
    title = re.sub(r"\s*\(\s*$", "", title)
    if len(title) > 58 and site_name not in title:
        title = truncate(title, 55) + f" | {site_name}"
    elif len(title) > 60:
        title = truncate(title, 60)
    return title


def path_to_url(site_url: str, rel_path: str) -> str:
    rel = rel_path.replace("\\", "/").lstrip("/")
    if rel == "index.html":
        return site_url.rstrip("/") + "/"
    return site_url.rstrip("/") + "/" + rel


def abs_image(site_url: str, image_path: str | None, config: dict) -> str:
    if not image_path:
        image_path = config["default_og_image"]
    if image_path.startswith("http"):
        return image_path
    return site_url.rstrip("/") + "/" + image_path.lstrip("/")


def strip_seo_block(content: str) -> str:
    return re.sub(
        re.escape(SEO_BEGIN) + r"[\s\S]*?" + re.escape(SEO_END) + r"\n?",
        "",
        content,
        count=1,
    )


def strip_robots_meta(content: str) -> str:
    return ROBOTS_RE.sub("", content)


def jsonld_script(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f'  <script type="application/ld+json">{payload}</script>'


def same_as_links(config: dict) -> list[str]:
    social = config.get("social", {})
    org = config.get("organization", {})
    links = [
        social.get("instagram"),
        social.get("linkedin"),
        social.get("facebook"),
        social.get("youtube"),
        social.get("whatsapp"),
        org.get("google_business_url"),
        org.get("maps_url"),
        "https://inforhealth.com.br",
    ]
    return [u for u in links if u]


def organization_schema(config: dict) -> dict:
    org = config["organization"]
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": ["Organization", "EducationalOrganization"],
        "@id": config["site_url"] + "/#organization",
        "name": org["name"],
        "legalName": org.get("legal_name", org["name"]),
        "url": org["url"],
        "logo": org["logo"],
        "image": org["logo"],
        "email": org["email"],
        "telephone": org["telephone"],
        "foundingDate": org.get("founding_date"),
        "address": {
            "@type": "PostalAddress",
            "addressLocality": org["address_locality"],
            "addressRegion": org["address_region"],
            "addressCountry": org["address_country"],
            "postalCode": org.get("postal_code"),
        },
        "areaServed": {"@type": "Country", "name": "Brasil"},
        "sameAs": same_as_links(config),
    }
    return schema


def local_business_schema(config: dict) -> dict:
    """Schema para Google Maps / Meu Negócio / buscas locais."""
    org = config["organization"]
    social = config.get("social", {})
    return {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "@id": config["site_url"] + "/#localbusiness",
        "name": org["name"],
        "url": org["url"],
        "image": org["logo"],
        "telephone": org["telephone"],
        "email": org["email"],
        "priceRange": org.get("price_range", "$$"),
        "address": {
            "@type": "PostalAddress",
            "addressLocality": org["address_locality"],
            "addressRegion": org["address_region"],
            "addressCountry": org["address_country"],
            "postalCode": org.get("postal_code"),
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": org.get("latitude"),
            "longitude": org.get("longitude"),
        },
        "hasMap": org.get("maps_url"),
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00",
            "closes": "18:00",
        },
        "sameAs": same_as_links(config),
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": org["telephone"],
            "contactType": "customer service",
            "availableLanguage": "Portuguese",
            "url": social.get("whatsapp"),
        },
    }


def website_schema(config: dict) -> dict:
    base = config["site_url"].rstrip("/")
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": base + "/#website",
        "name": config["site_name"],
        "url": base + "/",
        "publisher": {"@id": base + "/#organization"},
        "inLanguage": "pt-BR",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": base + "/cursos.html?q={search_term_string}",
            },
            "query-input": "required name=search_term_string",
        },
    }


def speakable_schema(config: dict, *, url: str, title: str, description: str) -> dict:
    """Ajuda buscas com IA (Google AI Overviews) a identificar trechos citáveis."""
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": url,
        "inLanguage": "pt-BR",
        "isPartOf": {"@id": config["site_url"] + "/#website"},
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".hero-headline", "h1", ".blog-article-body p", ".course-detail-prose p"],
        },
    }


def article_schema(
    config: dict,
    *,
    title: str,
    description: str,
    url: str,
    image: str,
    date_published: str | None,
    categories: list[str],
) -> dict:
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": url,
        "image": image,
        "author": {"@type": "Organization", "name": config["organization"]["name"]},
        "publisher": {
            "@type": "Organization",
            "name": config["organization"]["name"],
            "logo": {"@type": "ImageObject", "url": config["organization"]["logo"]},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "inLanguage": "pt-BR",
    }
    if date_published:
        schema["datePublished"] = date_published
        schema["dateModified"] = date_published
    if categories:
        schema["articleSection"] = categories[0]
        schema["keywords"] = ", ".join(categories)
    return schema


def course_schema(
    config: dict,
    *,
    title: str,
    description: str,
    url: str,
    image: str,
    modality: str,
) -> dict:
    mode_map = {
        "ao-vivo": "Online",
        "gravado": "Online",
        "mentoria": "Blended",
    }
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": title,
        "description": description,
        "url": url,
        "image": image,
        "provider": {
            "@type": "Organization",
            "name": config["organization"]["name"],
            "sameAs": config["site_url"],
        },
        "courseMode": mode_map.get(modality, "Online"),
        "inLanguage": "pt-BR",
        "educationalCredentialAwarded": "Certificado de conclusão",
    }


def breadcrumb_schema(config: dict, items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": item,
            }
            for i, (name, item) in enumerate(items)
        ],
    }


def build_seo_block(
    config: dict,
    *,
    canonical_url: str,
    title: str,
    description: str,
    og_type: str = "website",
    og_image: str | None = None,
    robots: str | None = None,
    jsonld: list[dict] | None = None,
) -> str:
    site_url = config["site_url"]
    image = abs_image(site_url, og_image, config)
    desc = truncate(description, 160)
    title_clean = clean_title(title, "Inforhealth")

    lines = [
        SEO_BEGIN,
        f'  <link rel="canonical" href="{esc(canonical_url)}">',
    ]
    if robots:
        lines.append(f'  <meta name="robots" content="{esc(robots)}">')

    lines.extend(
        [
            f'  <meta property="og:type" content="{esc(og_type)}">',
            f'  <meta property="og:site_name" content="{esc(config["site_name"])}">',
            f'  <meta property="og:locale" content="{esc(config["locale"])}">',
            f'  <meta property="og:title" content="{esc(title_clean)}">',
            f'  <meta property="og:description" content="{esc(desc)}">',
            f'  <meta property="og:url" content="{esc(canonical_url)}">',
            f'  <meta property="og:image" content="{esc(image)}">',
            '  <meta name="twitter:card" content="summary_large_image">',
            f'  <meta name="twitter:title" content="{esc(title_clean)}">',
            f'  <meta name="twitter:description" content="{esc(desc)}">',
            f'  <meta name="twitter:image" content="{esc(image)}">',
        ]
    )

    for block in jsonld or []:
        lines.append(jsonld_script(block))

    lines.append(SEO_END)
    return "\n".join(lines) + "\n"


def build_ga4_block(config: dict) -> str:
    gid = (config.get("ga4_measurement_id") or "").strip()
    if not gid or gid.startswith("G-XXXX"):
        return (
            f"{ANALYTICS_BEGIN}\n"
            "  <!-- GA4: defina ga4_measurement_id em tools/seo/seo-config.json -->\n"
            f"{ANALYTICS_END}\n"
        )
    return (
        f"{ANALYTICS_BEGIN}\n"
        f'  <script async src="https://www.googletagmanager.com/gtag/js?id={esc(gid)}"></script>\n'
        "  <script>\n"
        "    window.dataLayer = window.dataLayer || [];\n"
        "    function gtag(){dataLayer.push(arguments);}\n"
        "    gtag('js', new Date());\n"
        f"    gtag('config', '{esc(gid)}');\n"
        "  </script>\n"
        f"{ANALYTICS_END}\n"
    )


def strip_analytics_block(content: str) -> str:
    return re.sub(
        re.escape(ANALYTICS_BEGIN) + r"[\s\S]*?" + re.escape(ANALYTICS_END) + r"\n?",
        "",
        content,
        count=1,
    )


def inject_ga4(content: str, config: dict) -> str:
    content = strip_analytics_block(content)
    block = build_ga4_block(config)
    if SEO_END in content:
        return content.replace(SEO_END, SEO_END + "\n" + block.rstrip(), 1)
    return content.replace("</head>", block + "</head>", 1)


def inject_into_html(content: str, seo_block: str, *, new_title: str | None = None, new_description: str | None = None) -> str:
    content = strip_seo_block(content)
    content = strip_robots_meta(content)

    if new_title:
        content = TITLE_RE.sub(f"<title>{esc(new_title)}</title>", content, count=1)
    if new_description and DESC_RE.search(content):
        content = DESC_RE.sub(f'<meta name="description" content="{esc(truncate(new_description, 160))}">', content, count=1)
    elif new_description:
        content = content.replace("</title>", f'</title>\n  <meta name="description" content="{esc(truncate(new_description, 160))}">', 1)

    anchor = '<meta name="description"'
    if anchor not in content:
        anchor = "</title>"
    return content.replace(anchor, seo_block + "  " + anchor, 1)


def is_redirect_page(content: str) -> bool:
    return bool(REDIRECT_RE.search(content))


def page_kind(rel: str) -> str:
    if rel == "index.html":
        return "home"
    if rel == "cursos.html":
        return "cursos"
    if rel.startswith("cursos/"):
        return "curso"
    if rel.startswith("blog/artigos/"):
        return "blog_article"
    if rel.startswith("blog-artigo"):
        return "redirect"
    if rel.startswith("blog/"):
        return "redirect"
    if rel.startswith("blog"):
        return "blog_list"
    if rel == "design_system.html":
        return "internal"
    return "institutional"


def rel_site_path(file_path: Path) -> str:
    return file_path.relative_to(SITE_ROOT).as_posix()


def load_blog_index() -> dict[str, dict]:
    path = SITE_ROOT / "js" / "blog-posts.json"
    posts = json.loads(path.read_text(encoding="utf-8"))
    return {p["slug"]: p for p in posts}
