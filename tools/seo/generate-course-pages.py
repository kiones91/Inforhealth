#!/usr/bin/env python3
"""Gera 36 landing pages de curso em site/cursos/{slug}.html para SEO."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SITE = REPO / "site"
CONTENT = REPO / "content"
OUT_DIR = SITE / "cursos"

BADGE = {
    "ao-vivo": ("solar:videocamera-record-linear", "Online Ao Vivo"),
    "gravado": ("solar:play-circle-linear", "Gravado — Assíncrono"),
    "mentoria": ("solar:user-speak-linear", "Mentoria 1:1"),
}

MODALITY_LABEL = {"ao-vivo": "Ao Vivo", "gravado": "Gravado", "mentoria": "Mentoria"}


def parse_course_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", text, re.M)
    modality = re.search(r"\*\*Modalidade:\*\*\s*(.+)", text)
    img = re.search(r"!\[[^\]]*\]\([^)]*imagens/cursos/([^)]+)\)", text)
    resumo = re.search(r"## Resumo\s*\n\s*(.+)", text)
    carga = re.search(r"\*\*Carga horária:\*\*\s*(.+)", text)
    topics = []
    in_prog = False
    for line in text.splitlines():
        if line.startswith("## Programação") or line.startswith("## Tópicos"):
            in_prog = True
            continue
        if in_prog and line.startswith("## "):
            break
        if in_prog and line.strip().startswith("- "):
            topics.append(line.strip()[2:])

    return {
        "title": title.group(1).strip() if title else "Curso Inforhealth",
        "modality": modality.group(1).strip().lower() if modality else "ao-vivo",
        "image": img.group(1) if img else None,
        "resumo": resumo.group(1).strip() if resumo else "",
        "carga": carga.group(1).strip() if carga else None,
        "topics": topics[:6],
    }


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_page(slug: str, short_title: str, meta: dict, modality_key: str) -> str:
    icon, mod_label = BADGE.get(modality_key, BADGE["ao-vivo"])
    img = meta["image"] or ("scih-seguranca-paciente.png" if slug == "seguranca-do-paciente" else f"{slug}.png")
    desc = meta["resumo"] or f"Curso {short_title} — Inforhealth Educação e Excelência em Saúde."
    page_title = f"{short_title} — Inforhealth Educação"
    meta_desc = f"Curso {short_title} ({MODALITY_LABEL.get(modality_key, 'Ao Vivo')}). {desc[:120]}"

    topics_html = ""
    if meta["topics"]:
        items = "\n".join(f"            <li>{esc(t)}</li>" for t in meta["topics"])
        topics_html = f"""        <section>
          <h2>Programação</h2>
          <ul>
{items}
          </ul>
        </section>"""
    else:
        topics_html = """        <section>
          <h2>O que você vai aprender</h2>
          <ul>
            <li>Conteúdo aplicado ao mercado de saúde brasileiro</li>
            <li>Certificado digital de conclusão</li>
            <li>Material de apoio e gravação (quando aplicável)</li>
          </ul>
        </section>"""

    carga_html = ""
    if meta["carga"]:
        carga_html = f"""        <span class="blog-card-dot" aria-hidden="true"></span>
        <span class="inline-flex items-center gap-1.5"><iconify-icon icon="solar:clock-circle-linear" width="14" class="text-ih-accent"></iconify-icon> {esc(meta["carga"])}</span>"""

    return f"""<!DOCTYPE html>
<html class="scroll-smooth" lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(page_title)}</title>
  <meta name="description" content="{esc(meta_desc)}">
  <link rel="icon" href="../../assets/imagens/institucional/favicon.png">
  <script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
  <link href="../css/tailwind.min.css" rel="stylesheet"/>
  <link href="../css/design-system.css" rel="stylesheet"/>
</head>
<body class="min-h-screen bg-stone-200 text-slate-900 antialiased p-3 lg:p-6">

<main class="w-full max-w-[1400px] mx-auto bg-white rounded-[2.5rem] shadow-2xl overflow-hidden relative">

  <header class="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-ih-primary/10">
    <nav class="flex items-center justify-between px-6 lg:px-12 py-4">
      <a href="../index.html" class="flex items-center group">
        <img src="../../assets/imagens/institucional/logo-inforhealth-2020.png" alt="Inforhealth — Educação e Excelência em Saúde" class="h-9 w-auto"/>
      </a>
      <div class="hidden lg:flex items-center gap-5">
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-ih-primary" href="../cursos.html" aria-current="page">Cursos</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="../eventos.html">Eventos</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="../in-company.html">In Company</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="../blog.html">Blog</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="../equipe.html">Equipe</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="../sobre.html">Sobre</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="../contato.html">Contato</a>
      </div>
      <a class="btn-glass btn-glass-accent btn-glass-sm" href="https://wa.me/5519997773084">
        <iconify-icon icon="solar:phone-linear" width="14"></iconify-icon> WhatsApp
      </a>
    </nav>
  </header>

  <section class="relative px-8 lg:px-16 xl:px-24 pt-12 pb-8 overflow-hidden ds-grid-bg">
    <div class="max-w-4xl relative z-10 reveal">
      <nav class="course-breadcrumb" aria-label="Navegação estrutural">
        <a href="../index.html">Início</a>
        <iconify-icon icon="solar:alt-arrow-right-linear" width="12"></iconify-icon>
        <a href="../cursos.html">Cursos</a>
        <iconify-icon icon="solar:alt-arrow-right-linear" width="12"></iconify-icon>
        <span aria-current="page">{esc(short_title)}</span>
      </nav>
      <div class="inline-flex items-center gap-2 border-gradient rounded-full px-4 py-1.5 bg-white/80 w-fit mb-5">
        <iconify-icon icon="{icon}" width="14" class="text-ih-accent"></iconify-icon>
        <span class="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-ih-primary">{mod_label}</span>
      </div>
      <h1 class="font-display text-3xl sm:text-4xl lg:text-[2.75rem] font-bold tracking-tight text-ih-primary leading-tight">{esc(meta["title"])}</h1>
      <p class="text-lg text-slate-600 mt-4 max-w-2xl leading-relaxed">{esc(desc)}</p>
      <div class="flex flex-wrap items-center gap-3 mt-5 font-mono text-[0.65rem] uppercase tracking-wider text-slate-400">
        <span class="inline-flex items-center gap-1.5"><iconify-icon icon="solar:diploma-verified-linear" width="14" class="text-ih-accent"></iconify-icon> Certificado</span>
{carga_html}
      </div>
    </div>
  </section>

  <article class="px-8 lg:px-16 xl:px-24 pb-16">
    <div class="course-detail-layout reveal">
      <div class="course-detail-prose min-w-0">
{topics_html}
        <section class="course-faq">
          <h2>Dúvidas frequentes</h2>
          <details><summary>Tem certificado?</summary><p>Sim. Certificado emitido em conformidade com a LDB e Decreto 5.154/04.</p></details>
          <details><summary>Formas de pagamento</summary><p>Pix, Boleto e Cartão (até 12x).</p></details>
          <details><summary>Como acesso as aulas?</summary><p>Plataforma digital após confirmação do pagamento.</p></details>
        </section>
      </div>
      <aside class="course-enrollment-card border-gradient" aria-label="Inscrição">
        <img src="../../assets/imagens/cursos/{esc(img)}" alt="{esc(short_title)} — curso Inforhealth" loading="lazy">
        <ul class="course-enrollment-features">
          <li><iconify-icon icon="solar:check-circle-linear" width="18"></iconify-icon> {MODALITY_LABEL.get(modality_key, "Ao Vivo")}</li>
          <li><iconify-icon icon="solar:check-circle-linear" width="18"></iconify-icon> Certificado Digital</li>
          <li><iconify-icon icon="solar:check-circle-linear" width="18"></iconify-icon> Suporte pedagógico</li>
        </ul>
        <div class="course-enrollment-actions">
          <a class="btn-glass btn-glass-accent btn-glass-md" href="https://wa.me/5519997773084?text=Olá! Tenho interesse no curso {esc(short_title)}.">
            <iconify-icon icon="solar:chat-round-dots-linear" width="16"></iconify-icon> Inscrever-se
          </a>
          <a class="btn-glass btn-glass-outline btn-glass-md" href="https://wa.me/5519997773084">
            <iconify-icon icon="solar:phone-linear" width="16"></iconify-icon> Tirar dúvidas
          </a>
        </div>
      </aside>
    </div>
    <p class="mt-10"><a href="../cursos.html" class="text-sm font-medium text-ih-accent hover:underline">← Voltar ao catálogo de cursos</a></p>
  </article>

  <footer class="px-8 lg:px-16 xl:px-24 py-8 border-t border-ih-primary/10 text-center">
    <p class="text-sm text-slate-400">© 2026 Inforhealth Educação e Excelência em Saúde</p>
  </footer>
</main>

<a href="https://wa.me/5519997773084" class="btn-glass btn-glass-accent btn-glass-fab fixed bottom-6 right-6 z-50 shadow-xl" aria-label="WhatsApp">
  <iconify-icon icon="solar:chat-round-dots-bold" width="26"></iconify-icon>
</a>
</body>
</html>
"""


def load_course_index():
    """Carrega índice de cursos do markdown."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_cards", REPO / "tools" / "gen-cards.py")
    mod = importlib.util.module_from_spec(spec)
    # Parse index directly to avoid executing gen-cards side effects
    index = CONTENT / "07-indice-cursos.md"
    courses = []
    short = {}
    exec_globals = {"SHORT": {}}
    # Read SHORT from gen-cards without running it
    gen_text = (REPO / "tools" / "gen-cards.py").read_text(encoding="utf-8")
    short_match = re.search(r"SHORT = \{([^}]+(?:\{[^}]*\}[^}]*)*)\}", gen_text, re.S)
    if short_match:
        exec("SHORT = {" + short_match.group(1) + "}", exec_globals)
        short = exec_globals["SHORT"]

    for line in index.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(\S+)\s*\|\s*\[([^\]]+)\]", line)
        if m:
            slug = m.group(3).replace(".md", "").replace("curso-", "")
            courses.append({
                "slug": slug,
                "modality": m.group(2).strip(),
                "file": CONTENT / "cursos" / m.group(3),
                "short": short.get(slug, m.group(1).strip()[:50]),
            })
    return courses


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    courses = load_course_index()
    for c in courses:
        meta = parse_course_md(c["file"]) if c["file"].exists() else {"title": c["short"], "modality": c["modality"], "image": None, "resumo": "", "carga": None, "topics": []}
        html = render_page(c["slug"], c["short"], meta, c["modality"])
        out = OUT_DIR / f"{c['slug']}.html"
        out.write_text(html, encoding="utf-8")
    print(f"{len(courses)} páginas geradas em {OUT_DIR}")


if __name__ == "__main__":
    main()
