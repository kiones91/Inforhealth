#!/usr/bin/env python3
"""Gera páginas do blog a partir do site original Inforhealth."""
import re, json, subprocess, html as htmlmod
from pathlib import Path

BASE = "https://edu.inforhealth.com.br"
BLOG_PAGES = [
    f"{BASE}/blog_inforhealth-educacao-excelencia-saude/",
    f"{BASE}/blog_inforhealth-educacao-excelencia-saude/page/2/",
    f"{BASE}/blog_inforhealth-educacao-excelencia-saude/page/3/",
    f"{BASE}/blog_inforhealth-educacao-excelencia-saude/page/4/",
]
SKIP = {"equipe", "curso-in-company", "capacitacao", "wp-json"}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ROOT = REPO_ROOT / "site"
JSON_PATH = ROOT / "js/blog-posts.json"
BLOG_DIR = ROOT / "blog" / "artigos"
ARTICLE_HREF = "blog/artigos"
PORTAL_PREFIX = "../../"
WHATSAPP = "https://wa.me/5519997773084"

# Slugs de curso/página no site antigo → rota local no portal novo
LOCAL_ROUTE_MAP = {
    "curso-in-company": "in-company.html",
    "treinamentos-para-instituicoes-de-saude": "in-company.html",
    "administracao-hospitalar-3-congresso": "eventos.html",
    "gestao-de-pessoas-em-saude-lideranca-performance": "curso.html",
    "curso-governanca-regulatoria-ans": "curso.html",
    "curso-ao-vivo-governanca-clinica-e-vbhc-na-medicina-baseada-em-evidencias": "curso.html",
    "curso-ao-vivo-gestao-de-riscos-principios-e-diretrizes-da-iso-31000": "curso.html",
    "curso-ao-vivo-mapeamento-e-gestao-por-processos": "curso.html",
    "curso-auditoria-clinica": "curso.html",
    "curso-formacao-de-auditores-internos-de-gestao-da-qualidade-em-saude": "curso.html",
    "curso-online-drg-diagnosis-related-groups": "curso.html",
    "curso-online-seguranca-do-paciente": "curso.html",
    "formacao-em-medicina-hospitalista": "curso.html",
    "formacao-servico-de-controle-de-infeccao-hospitalar": "curso.html",
    "guia_drg_pratica": "ebook.html",
}

CATEGORY_STYLE = {
    "gestão em saúde": ("primary", "solar:document-text-linear"),
    "gestao em saude": ("primary", "solar:document-text-linear"),
    "qualidade": ("accent", "solar:medal-ribbon-linear"),
    "seguranca do paciente": ("seguranca", "solar:shield-check-linear"),
    "segurança do paciente": ("seguranca", "solar:shield-check-linear"),
    "faturamento": ("secondary", "solar:chart-2-linear"),
    "cursos saúde suplementar": ("primary", "solar:document-text-linear"),
    "sem categoria": ("secondary", "solar:notebook-linear"),
}


def fetch(url):
    r = subprocess.run(["curl", "-sL", "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", errors="replace")


def strip_junk(content):
    for marker in [
        "<h3>Compartilhe isso:",
        "<div class='sharedaddy",
        '<nav aria-label="Post navigation"',
        "<h2> Posts relacionados</h2>",
        "jetpack-likes-widget",
        "Curtir isso:",
    ]:
        idx = content.find(marker)
        if idx != -1:
            content = content[:idx]
    content = re.sub(r"\sdata-element[_a-z-]+=\"[^\"]*\"", "", content)
    content = re.sub(r"\sdata-widget[_a-z-]+=\"[^\"]*\"", "", content)
    content = re.sub(r"<section[^>]*>", "<section>", content)
    content = re.sub(r"<div[^>]*>", "<div>", content)
    content = re.sub(r"(<div>\s*</div>\s*)+$", "", content)
    content = re.sub(r"</section></div>(<div>\s*</div>)+", "</section>", content)
    return content


def clean_html_content(raw):
    content = ""
    m = re.search(r'<div class="entry-content[^"]*"[^>]*>(.*)', raw, re.S | re.I)
    if m:
        content = m.group(1)
    else:
        m2 = re.search(r'data-elementor-type="wp-post"[^>]*>(.*)', raw, re.S | re.I)
        if m2:
            content = m2.group(1)
    content = strip_junk(content)
    end = re.search(r"</article>", content)
    if end:
        content = content[: end.start()]
    content = re.sub(r"<script[\s\S]*?</script>", "", content, flags=re.I)
    content = re.sub(r"<style[\s\S]*?</style>", "", content, flags=re.I)
    content = re.sub(
        r'<img([^>]*?)data-src="([^"]+)"([^>]*)>',
        r'<img\1src="\2"\3 loading="lazy">',
        content,
    )
    content = re.sub(r'data-lazyloaded="1"\s*', "", content)
    content = re.sub(r'src="data:image/svg\+xml[^"]*"', "", content)
    content = re.sub(r"\sdata-[a-z-]+=\"[^\"]*\"", "", content)
    content = re.sub(r'\sclass="[^"]*"', "", content)
    content = re.sub(r'\sstyle="[^"]*"', "", content)
    content = re.sub(r'\sid="[^"]*"', "", content)
    content = re.sub(r"<span>\s*</span>", "", content)
    content = re.sub(r"(<div>\s*</div>\s*)+$", "", content)
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = strip_junk(content)
    return content.strip()


def get_meta(raw, list_title=""):
    title_m = re.search(r'<meta property="og:title" content="([^"]*)"', raw)
    if not title_m:
        title_m = re.search(r"<title>([^<|]+)", raw)
    title = htmlmod.unescape(title_m.group(1).strip()) if title_m else list_title
    title = re.sub(r"\s*[\-|–].*$", "", title).strip()
    date_m = re.search(r'<time[^>]+datetime="(\d{4}-\d{2}-\d{2})"', raw)
    if not date_m:
        date_m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', raw)
    date = date_m.group(1) if date_m else "2024-01-01"
    cats = re.findall(r'rel="category tag">([^<]+)</a>', raw)
    cats = list(dict.fromkeys([htmlmod.unescape(c.strip()) for c in cats]))[:3]
    excerpt_m = re.search(r'<meta name="description" content="([^"]*)"', raw)
    if not excerpt_m:
        excerpt_m = re.search(r'<meta property="og:description" content="([^"]*)"', raw)
    excerpt = htmlmod.unescape(excerpt_m.group(1)) if excerpt_m else ""
    img_m = re.search(r'<meta property="og:image" content="([^"]*)"', raw)
    image = img_m.group(1) if img_m else ""
    return title, date, cats, excerpt, image


def format_date_pt(iso):
    months = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    ]
    y, m, d = iso.split("-")
    return f"{int(d)} de {months[int(m) - 1]} de {y}"


def cat_style(cats):
    key = (cats[0] if cats else "Gestão em Saúde").lower()
    for k, v in CATEGORY_STYLE.items():
        if k in key:
            return v
    return ("primary", "solar:document-text-linear")


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def _local_path(page):
    return f"{PORTAL_PREFIX}{page}"


def _slug_from_url(url):
    from urllib.parse import urlparse, unquote

    path = unquote(urlparse(url).path).strip("/")
    if not path:
        return ""
    return path.split("/")[-1].split("#")[0].split("?")[0]


def rewrite_portal_links(content, article_slugs=None):
    """Reescreve URLs do site antigo para a estrutura local do portal novo."""
    article_slugs = article_slugs or set()

    content = re.sub(
        r"https?://wa\.me/551935971445[^\"'>\s]*",
        WHATSAPP,
        content,
        flags=re.I,
    )
    content = content.replace('href="#baixar"', f'href="{_local_path("ebook.html")}"')

    def local_for_slug(slug):
        if not slug:
            return _local_path("index.html")
        if slug in article_slugs:
            return f"{slug}.html"
        if slug in LOCAL_ROUTE_MAP:
            return _local_path(LOCAL_ROUTE_MAP[slug])
        if slug.startswith("curso") or slug.startswith("formacao"):
            return _local_path("curso.html")
        if slug.startswith("cursos"):
            return _local_path("cursos.html")
        if "in-company" in slug or "treinamento" in slug:
            return _local_path("in-company.html")
        if "congresso" in slug or "evento" in slug:
            return _local_path("eventos.html")
        if "contato" in slug:
            return _local_path("contato.html")
        return _local_path("cursos.html")

    def rewrite_href(match):
        href = match.group(1)
        if re.search(r"\.pdf(?:\?|$|#)", href, re.I) or "/wp-content/uploads/" in href:
            return f'href="{_local_path("ebook.html")}"'
        if "consultoria.inforhealth.com.br" in href:
            return f'href="{_local_path("in-company.html")}"'
        if re.match(r"https?://(?:www\.)?inforhealth\.com\.br", href, re.I):
            return f'href="{_local_path("index.html")}"'
        if "edu.inforhealth.com.br" not in href:
            return match.group(0)
        slug = _slug_from_url(href)
        if slug.endswith(".pdf"):
            return f'href="{_local_path("ebook.html")}"'
        if "?share=" in href or href.endswith("?share=facebook") or href.endswith("?share=x"):
            slug = _slug_from_url(href.split("?")[0])
        return f'href="{local_for_slug(slug)}"'

    content = re.sub(r'href="([^"]+)"', rewrite_href, content)
    return content


def tag_content_links(content):
    """Marca banners (img) e botões de texto para estilos corretos no CSS."""

    def add_class(tag, class_name):
        if class_name in tag:
            return tag
        if 'class="' in tag:
            return tag.replace('class="', f'class="{class_name} ', 1)
        return tag.replace("<a", f'<a class="{class_name}"', 1)

    def banner_link(match):
        return add_class(match.group(1), "blog-banner-link") + match.group(2)

    def inline_cta(match):
        return add_class(match.group(1), "blog-inline-cta") + match.group(2)

    content = re.sub(
        r'(<a\b[^>]*?)(\s*>\s*<img\b)',
        banner_link,
        content,
        flags=re.I,
    )
    content = re.sub(
        r'(<a\b[^>]*?)(\s*>\s*<span>\s*<span>)',
        inline_cta,
        content,
        flags=re.I,
    )
    content = re.sub(
        r'(<a\b(?![^>]*\bblog-inline-cta\b)[^>]*?)(\s*>\s*(?:BAIXAR|CONFERIR|Baixe|🔗)[^<]{0,120}</a>)',
        inline_cta,
        content,
        flags=re.I,
    )
    return content


def prepare_article_content(content, article_slugs):
    content = strip_junk(content or "")
    content = rewrite_portal_links(content, article_slugs)
    return tag_content_links(content)


TAILWIND_CONFIG = """
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'system-ui', 'sans-serif'],
            display: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
            mono: ['Geist Mono', 'ui-monospace', 'monospace'],
          },
          colors: {
            ih: {
              primary: '#09314d', secondary: '#2f80b5',
              accent: '#16a89a', 'accent-dark': '#118a7e', orange: '#ff8e2b',
              surface: '#ffffff', muted: '#f4f8fa',
            }
          }
        }
      }
    }
  </script>"""


def ds_head(title, description, asset_prefix=""):
    css = f"{asset_prefix}css/design-system.css"
    favicon = f"{asset_prefix}../assets/imagens/institucional/favicon.png"
    return f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
  <meta name="description" content="{{description}}">
  <link rel="icon" href="{{favicon}}">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js" defer></script>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500&display=swap" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'"/>
  <link href="{{css}}" rel="stylesheet"/>
{TAILWIND_CONFIG}
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4, h5, h6 {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    iconify-icon {{ display: inline-flex; vertical-align: middle; }}
  </style>"""


def ds_nav(asset_prefix="", active="blog"):
    import importlib.util
    from pathlib import Path as _Path
    _spec = importlib.util.spec_from_file_location(
        "nav_snippet",
        _Path(__file__).resolve().parent / "nav-snippet.py",
    )
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    return _mod.site_header_nav(asset_prefix=asset_prefix, active=active)


def ds_closing_footer(asset_prefix=""):
    import importlib.util
    from pathlib import Path as _Path
    _spec = importlib.util.spec_from_file_location(
        "closing_footer_snippet",
        _Path(__file__).resolve().parent / "closing-footer-snippet.py",
    )
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    return "  " + _mod.closing_zone_footer(asset_prefix).replace("\n", "\n  ").strip()


def ds_whatsapp():
    return """<a href="https://wa.me/5519997773084" class="btn-glass btn-glass-accent btn-glass-fab fixed bottom-6 right-6 z-50 shadow-xl" aria-label="WhatsApp">
  <iconify-icon icon="solar:chat-round-dots-bold" width="26"></iconify-icon>
</a>"""


def ds_mobile_nav(asset_prefix=""):
    import importlib.util
    from pathlib import Path as _Path
    _spec = importlib.util.spec_from_file_location(
        "nav_snippet",
        _Path(__file__).resolve().parent / "nav-snippet.py",
    )
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    return _mod.mobile_nav_script_tag(asset_prefix)


def ds_scripts(extra=""):
    return f"""<script>
document.addEventListener('DOMContentLoaded', () => {{
  const aosObs = new IntersectionObserver((entries) => {{
    entries.forEach((e) => {{ if (e.isIntersecting) {{ e.target.classList.add('animate'); aosObs.unobserve(e.target); }} }});
  }}, {{ threshold: 0.1 }});
  document.querySelectorAll('.animate-on-scroll').forEach((el) => aosObs.observe(el));
  const revObs = new IntersectionObserver((entries) => {{
    entries.forEach((e) => {{ if (e.isIntersecting) e.target.classList.add('active'); }});
  }}, {{ threshold: 0.08 }});
  document.querySelectorAll('.reveal').forEach((el) => revObs.observe(el));
  {extra}
}});
</script>"""


def related_cards(articles, current_slug):
    idx = next((i for i, x in enumerate(articles) if x["slug"] == current_slug), 0)
    others = []
    for offset in [1, 2, -1, -2, 3, 4]:
        j = idx + offset
        if 0 <= j < len(articles) and articles[j]["slug"] != current_slug:
            others.append(articles[j])
        if len(others) >= 2:
            break
    if len(others) < 2:
        others = [x for x in articles if x["slug"] != current_slug][:2]
    html = ""
    for r in others[:2]:
        cc, ci = cat_style(r["categories"])
        html += f"""          <article class="blog-card group">
            <a href="{esc(r['slug'])}.html" class="blog-card-link">
              <div class="blog-card-cover blog-card-cover--{cc}" style="aspect-ratio:16/7;">
                <div class="blog-card-cover-bg"></div>
                <iconify-icon icon="{ci}" class="blog-card-cover-icon" style="font-size:2rem;"></iconify-icon>
              </div>
              <div class="blog-card-body" style="padding:0.85rem 1rem 1rem;">
                <h3 style="font-size:0.9rem;">{esc(r['title'][:70])}</h3>
              </div>
            </a>
          </article>"""
    if not html:
        return ""
    return f"""
      <section class="mt-16 pt-10 border-t border-ih-primary/10 reveal">
        <h2 class="font-display text-xl font-semibold text-ih-primary mb-6">Artigos relacionados</h2>
        <div class="blog-related-grid">{html}
        </div>
      </section>"""


def render_article(a, articles=None):
    cover_class, cat_icon = cat_style(a["categories"])
    cat_label = esc(a["categories"][0])
    breadcrumb = a["title"][:50] + ("…" if len(a["title"]) > 50 else "")

    if a.get("image"):
        cover = (
            f'<div class="blog-article-cover"><img src="{esc(a["image"])}" '
            f'alt="{esc(a["title"])}" loading="eager"/></div>'
        )
    else:
        cover = (
            f'<div class="blog-article-cover blog-article-cover--gradient '
            f'blog-card-cover--{cover_class}">'
            f'<iconify-icon icon="{cat_icon}"></iconify-icon></div>'
        )

    plain = re.sub(r"<[^>]+>", " ", a.get("content", ""))
    if len(plain.strip()) < 80:
        body = (
            f'<p class="text-lg text-slate-600 leading-relaxed">{esc(a["excerpt"])}</p>'
            f'<p>Conteúdo completo disponível no '
            f'<a href="{esc(a["url"])}" target="_blank" rel="noopener">'
            f"blog original da Inforhealth</a>.</p>"
        )
    else:
        slugs = {x["slug"] for x in (articles or [])}
        body = prepare_article_content(a["content"], slugs)

    related = related_cards(articles or [], a["slug"]) if articles else ""

    return f"""<!DOCTYPE html>
<html class="scroll-smooth" lang="pt-BR">
<head>
{ds_head(esc(a['title'][:70]) + ' — Blog Inforhealth', esc(a['excerpt'][:160]), '../../')}
</head>
<body class="min-h-screen bg-stone-200 text-slate-900 antialiased selection:bg-ih-accent/30 selection:text-ih-primary p-3 lg:p-6">

<main class="w-full max-w-[1400px] mx-auto bg-white rounded-[2.5rem] shadow-2xl overflow-hidden relative">

{ds_nav('../../', 'blog')}

  <!-- Hero artigo -->
  <section class="blog-article-hero relative px-8 lg:px-16 xl:px-24 pt-12 pb-8 overflow-hidden ds-grid-bg">
    <div class="beam-h top-12" style="animation-delay:0s;"></div>
    <div class="orb w-64 h-64 bg-ih-accent/12 -top-16 -right-16"></div>
    <div class="orb w-48 h-48 bg-ih-primary/8 bottom-0 left-1/4" style="animation-delay:-2s;"></div>
    <div class="blog-article-wrap relative z-10 reveal">
      <nav class="blog-breadcrumb" aria-label="Navegação">
        <a href="../../index.html">Início</a>
        <iconify-icon icon="solar:alt-arrow-right-linear" width="12"></iconify-icon>
        <a href="../../blog.html">Blog</a>
        <iconify-icon icon="solar:alt-arrow-right-linear" width="12"></iconify-icon>
        <span aria-current="page">{esc(breadcrumb)}</span>
      </nav>
      <header class="blog-article-header">
        <div class="inline-flex items-center gap-2 border-gradient rounded-full px-4 py-1.5 bg-white/80 backdrop-blur-sm w-fit mb-5">
          <iconify-icon icon="{cat_icon}" width="14" class="text-ih-accent"></iconify-icon>
          <span class="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-ih-primary">{cat_label}</span>
        </div>
        <h1 class="font-display text-3xl sm:text-4xl lg:text-[2.75rem] font-bold tracking-tight text-ih-primary leading-tight">{esc(a['title'])}</h1>
        <div class="blog-article-meta flex flex-wrap items-center gap-3 mt-4">
          <time datetime="{a['date']}">{format_date_pt(a['date'])}</time>
          <span class="blog-card-dot" aria-hidden="true"></span>
          <span>{a['reading_min']} min de leitura</span>
        </div>
      </header>
    </div>
  </section>

  <article class="px-8 lg:px-16 xl:px-24 pb-16 lg:pb-20">
    <div class="blog-article-wrap reveal">
      {cover}
      <div class="blog-article-prose">
        <div class="blog-article-body">{body}</div>
      </div>

      <aside class="blog-article-cta">
        <p class="text-sm font-semibold text-ih-primary mb-1">Quer se aprofundar neste tema?</p>
        <p class="text-sm text-slate-600 mb-4">Conheça os cursos e soluções In Company da Inforhealth Educação.</p>
        <div class="flex flex-wrap gap-3">
          <a href="../../cursos.html" class="btn-glass btn-glass-outline btn-glass-md">Ver cursos <iconify-icon icon="solar:arrow-right-linear" width="16"></iconify-icon></a>
          <a href="https://wa.me/5519997773084" class="btn-glass btn-glass-accent btn-glass-md">WhatsApp <iconify-icon icon="solar:phone-linear" width="16"></iconify-icon></a>
        </div>
      </aside>
      {related}
    </div>
  </article>

{ds_closing_footer("../../")}

</main>

{ds_whatsapp()}
{ds_mobile_nav("../../")}
{ds_scripts()}
</body>
</html>"""


def card_html(a, index):
    cover_class, cat_icon = cat_style(a["categories"])
    tag = a["categories"][0]
    short_date = format_date_pt(a["date"]).split(" de ")[1] + " " + a["date"][:4] if a["date"] else ""
    # simpler: month year from iso
    months_short = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    y, m, d = a["date"].split("-")
    date_label = f"{int(d)} {months_short[int(m)-1]} {y}"
    return f"""          <article class="blog-card blog-card--{cover_class} group" data-categories="{esc(','.join(a['categories']).lower())}">
            <a href="{ARTICLE_HREF}/{esc(a['slug'])}.html" class="blog-card-link">
              <div class="blog-card-cover blog-card-cover--{cover_class}">
                <div class="blog-card-cover-bg"></div>
                <iconify-icon icon="{cat_icon}" class="blog-card-cover-icon"></iconify-icon>
                <span class="blog-card-tag">{esc(tag)}</span>
              </div>
              <div class="blog-card-body">
                <div class="blog-card-meta">
                  <time datetime="{a['date']}">{date_label}</time>
                  <span class="blog-card-dot" aria-hidden="true"></span>
                  <span>{a['reading_min']} min de leitura</span>
                </div>
                <h3>{esc(a['title'])}</h3>
                <p class="blog-card-excerpt">{esc(a['excerpt'][:160])}</p>
                <span class="blog-card-cta">Ler artigo <iconify-icon icon="solar:arrow-right-linear" width="14"></iconify-icon></span>
              </div>
            </a>
          </article>"""


def render_blog_listing(articles, page=1, per_page=12):
    total = len(articles)
    pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    chunk = articles[start : start + per_page]
    cards = "\n".join(card_html(a, i) for i, a in enumerate(chunk))

    pagination = ""
    if pages > 1:
        links = []
        for p in range(1, pages + 1):
            href = "blog.html" if p == 1 else f"blog-pagina-{p}.html"
            active_cls = "is-active" if p == page else ""
            links.append(f'<a class="{active_cls} px-2 py-1" href="{href}">{p}</a>')
        pagination = f"""
        <nav class="blog-pagination flex items-center justify-center gap-2 mt-12 pt-8 border-t border-ih-primary/10 reveal" aria-label="Paginação">
          <span class="text-xs text-slate-400 mr-2 font-mono uppercase tracking-wider">{total} artigos</span>
          {''.join(links)}
        </nav>"""

    page_title = f"Blog — Página {page} — Inforhealth Educação" if page > 1 else "Blog — Inforhealth Educação"
    listing_path = ROOT / ("blog.html" if page == 1 else f"blog-pagina-{page}.html")
    html = f"""<!DOCTYPE html>
<html class="scroll-smooth" lang="pt-BR">
<head>
{ds_head(page_title, "Artigos sobre regulação, qualidade e gestão em saúde — canal editorial da Inforhealth Educação.", "")}
</head>
<body class="min-h-screen bg-stone-200 text-slate-900 antialiased selection:bg-ih-accent/30 selection:text-ih-primary p-3 lg:p-6">

<main class="w-full max-w-[1400px] mx-auto bg-white rounded-[2.5rem] shadow-2xl overflow-hidden relative">

{ds_nav("", "blog")}

  <!-- Hero -->
  <section class="blog-list-hero relative px-8 lg:px-16 xl:px-24 pt-16 pb-12 overflow-hidden ds-grid-bg">
    <div class="beam-h top-16" style="animation-delay:0s;"></div>
    <div class="beam-v left-1/3 top-0" style="animation-delay:2.5s;"></div>
    <div class="orb w-72 h-72 bg-ih-accent/15 -top-20 -left-20"></div>
    <div class="orb w-96 h-96 bg-ih-primary/10 -top-10 right-0" style="animation-delay:-3s;"></div>
    <div class="relative z-10 max-w-3xl animate-on-scroll">
      <div class="inline-flex items-center gap-2 border-gradient rounded-full px-4 py-1.5 bg-white/80 backdrop-blur-sm w-fit mb-6">
        <span class="flex h-2 w-2 relative">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-ih-accent opacity-60"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-ih-accent"></span>
        </span>
        <span class="text-[0.65rem] font-semibold uppercase tracking-[0.25em] text-slate-500">Canal editorial</span>
      </div>
      <h1 class="font-display font-bold tracking-tighter leading-[0.9] text-5xl lg:text-7xl mb-4">
        <span class="block text-transparent-gradient text-glow">Fique por dentro</span>
      </h1>
      <p class="text-lg text-slate-600 leading-relaxed max-w-xl">
        Análises de especialistas em regulação, qualidade e gestão — conteúdo gratuito para quem lidera na saúde suplementar e hospitalar.
      </p>
    </div>
  </section>

  <section class="px-8 lg:px-16 xl:px-24 pb-12">
    <div class="reveal flex flex-col lg:flex-row gap-8 lg:gap-12">
      <aside class="blog-filters lg:w-56 shrink-0 h-fit lg:sticky lg:top-24 border-gradient" aria-label="Filtrar artigos">
        <fieldset class="border-0 p-0 m-0 relative z-10">
          <legend>Categorias</legend>
          <label><input type="checkbox" checked data-filter="all"> Todos</label>
          <label><input type="checkbox" data-filter="qualidade"> Qualidade e ONA</label>
          <label><input type="checkbox" data-filter="suplementar"> Saúde Suplementar</label>
          <label><input type="checkbox" data-filter="gestão"> Gestão Hospitalar</label>
          <label><input type="checkbox" data-filter="faturamento"> Faturamento e DRG</label>
          <label><input type="checkbox" data-filter="segurança"> Segurança do Paciente</label>
        </fieldset>
      </aside>
      <div class="flex-1 min-w-0">
        <p class="text-sm text-slate-500 mb-6 font-mono uppercase tracking-wider">{total} artigos publicados</p>
        <div class="blog-grid" id="blog-grid">
{cards}
        </div>
{pagination}
      </div>
    </div>
  </section>

{ds_closing_footer("")}

</main>

{ds_whatsapp()}
{ds_mobile_nav("")}
{ds_scripts()}
</body>
</html>"""
    listing_path.write_text(html, encoding="utf-8")
    print("Wrote", listing_path.name)


def write_blog_readme(articles):
    """Gera índice legível em blog/README.md."""
    lines = [
        "# Blog — artigos do portal",
        "",
        "Estrutura organizada do canal editorial Inforhealth.",
        "",
        "## Pastas",
        "",
        "| Caminho | Conteúdo |",
        "|---------|----------|",
        "| `../blog.html` | Listagem principal (página 1) |",
        "| `../blog-pagina-2.html` · `../blog-pagina-3.html` | Paginação |",
        "| `artigos/` | **36 páginas de artigo** (1 arquivo por slug) |",
        "| `../js/blog-posts.json` | Metadados + conteúdo (fonte para regenerar) |",
        "| `../../tools/scripts/generate-blog.py` | Script gerador |",
        "",
        "## URL de um artigo",
        "",
        "```",
        "blog/artigos/{slug}.html",
        "```",
        "",
        "Exemplo: `blog/artigos/governanca-regulatoria-novo-modelo-ans-2026.html`",
        "",
        "## Redirecionamentos legados",
        "",
        "| URL antiga | Destino |",
        "|------------|---------|",
        "| `blog-artigo.html` | artigo ANS 2026 |",
        "| `blog-artigo-drg.html` | artigo DRG |",
        "| `blog-artigo-ona.html` | artigo Manual ONA |",
        "| `blog-artigo-seguranca.html` | artigo Segurança do paciente |",
        "| `blog/{slug}.html` | `blog/artigos/{slug}.html` |",
        "",
        "## Regenerar páginas",
        "",
        "```bash",
        "cd tools/scripts",
        "python generate-blog.py --from-json",
        "```",
        "",
        f"## Índice ({len(articles)} artigos)",
        "",
    ]
    for a in articles:
        cat = a["categories"][0] if a.get("categories") else "—"
        lines.append(
            f"- [{a['title']}](artigos/{a['slug']}.html) — {cat} · {a.get('date', '')}"
        )
    readme = ROOT / "blog" / "README.md"
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote blog/README.md")


def main():
    import sys
    from_json = "--from-json" in sys.argv

    if from_json and JSON_PATH.exists():
        articles = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        print(f"Regenerating from {JSON_PATH} ({len(articles)} articles)")
    else:
        articles = []
        seen = set()
        for page in BLOG_PAGES:
            raw = fetch(page)
            for m in re.finditer(
                r'<h2[^>]*>\s*<a href="(https://edu\.inforhealth\.com\.br/([^"/]+)/)"[^>]*>([^<]+)</a>',
                raw,
            ):
                slug = m.group(2)
                if slug in SKIP or slug in seen:
                    continue
                seen.add(slug)
                articles.append(
                    {
                        "slug": slug,
                        "url": m.group(1),
                        "list_title": htmlmod.unescape(m.group(3).strip()),
                    }
                )

        print(f"Fetching {len(articles)} articles...")
        for i, a in enumerate(articles):
            raw = fetch(a["url"])
            title, date, cats, excerpt, image = get_meta(raw, a["list_title"])
            content = clean_html_content(raw)
            plain = re.sub(r"<[^>]+>", " ", content)
            a["title"] = a["list_title"] or title
            a["date"] = date
            a["categories"] = cats or ["Gestão em Saúde"]
            a["excerpt"] = (excerpt or a["list_title"])[:220]
            a["content"] = content
            a["image"] = image
            a["reading_min"] = max(3, min(12, len(plain.split()) // 200 or 3))
            if (i + 1) % 6 == 0:
                print(f"  {i + 1}/{len(articles)}")

        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")

    # Reescreve links e marca CTAs ao regenerar do JSON
    slug_set = {a["slug"] for a in articles}
    if from_json:
        for a in articles:
            if a.get("content"):
                a["content"] = prepare_article_content(a["content"], slug_set)
        JSON_PATH.write_text(
            json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    for a in articles:
        (BLOG_DIR / f"{a['slug']}.html").write_text(render_article(a, articles), encoding="utf-8")

    # Redirecionamentos: URLs antigas blog/{slug}.html → artigos/{slug}.html
    legacy_blog = ROOT / "blog"
    for a in articles:
        legacy_path = legacy_blog / f"{a['slug']}.html"
        if legacy_path.parent.resolve() != BLOG_DIR.resolve():
            target = f"artigos/{a['slug']}.html"
            redirect = (
                f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
                f'<meta http-equiv="refresh" content="0;url={target}">'
                f'<link rel="canonical" href="{target}"><title>Redirecionando…</title></head>'
                f'<body><p><a href="{target}">Ir para o artigo</a></p></body></html>'
            )
            legacy_path.write_text(redirect, encoding="utf-8")

    per_page = 12
    pages = (len(articles) + per_page - 1) // per_page
    for p in range(1, pages + 1):
        render_blog_listing(articles, p, per_page)

    # Redirecionamentos: URLs legadas na raiz do esqueleto
    slug_map = {
        "blog-artigo.html": "governanca-regulatoria-novo-modelo-ans-2026",
        "blog-artigo-drg.html": "drg-e-o-mercado-futuro-na-saude",
        "blog-artigo-ona.html": "o-papel-do-manual-ona-para-hospitais",
        "blog-artigo-seguranca.html": "seguranca-paciente-excelencia-cuidado",
    }
    for old, new_slug in slug_map.items():
        target = f"{ARTICLE_HREF}/{new_slug}.html"
        redirect = (
            f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
            f'<meta http-equiv="refresh" content="0;url={target}">'
            f'<link rel="canonical" href="{target}"><title>Redirecionando…</title></head>'
            f'<body><p><a href="{target}">Ir para o artigo</a></p></body></html>'
        )
        (ROOT / old).write_text(redirect, encoding="utf-8")

    write_blog_readme(articles)

    print(f"Done: {len(articles)} articles, {pages} listing pages")
    print("SEO: execute `python tools/seo/run-seo.py` para atualizar meta tags e sitemap.")


if __name__ == "__main__":
    main()
