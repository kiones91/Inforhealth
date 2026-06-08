"""Snippet do header com menu mobile (drawer)."""


def mobile_drawer_html() -> str:
    return """  <div id="site-mobile-nav" class="site-mobile-nav" aria-hidden="true">
    <div class="site-mobile-nav-backdrop" data-mobile-nav-close tabindex="-1" aria-hidden="true"></div>
    <aside class="site-mobile-nav-panel" role="dialog" aria-modal="true" aria-label="Menu de navegação">
      <div class="site-mobile-nav-head">
        <span class="site-mobile-nav-label">Navegação</span>
        <button type="button" class="site-mobile-nav-close" aria-label="Fechar menu" data-mobile-nav-close>
          <iconify-icon icon="solar:close-circle-linear" width="26"></iconify-icon>
        </button>
      </div>
      <nav class="site-mobile-nav-links" aria-label="Menu principal"></nav>
      <a href="https://wa.me/5519997773084" class="btn-glass btn-glass-accent btn-glass-md site-mobile-nav-whatsapp">
        <iconify-icon icon="solar:chat-round-dots-linear" width="18"></iconify-icon> Falar no WhatsApp
      </a>
    </aside>
  </div>"""


def nav_actions_html(whatsapp_class: str = "btn-glass btn-glass-accent btn-glass-sm") -> str:
    return f"""      <div class="flex items-center gap-2 shrink-0">
        <button type="button" class="site-nav-toggle lg:hidden" aria-expanded="false" aria-controls="site-mobile-nav" aria-label="Abrir menu">
          <iconify-icon icon="solar:hamburger-menu-linear" width="24"></iconify-icon>
        </button>
        <a class="{whatsapp_class}" href="https://wa.me/5519997773084">
          <iconify-icon icon="solar:phone-linear" width="14"></iconify-icon> WhatsApp
        </a>
      </div>"""


def site_header_nav(
    asset_prefix: str = "",
    active: str | None = None,
    logo_aria_current: bool = False,
    whatsapp_class: str = "btn-glass btn-glass-accent btn-glass-sm",
) -> str:
    links = [
        ("cursos.html", "Cursos", "cursos"),
        ("eventos.html", "Eventos", "eventos"),
        ("in-company.html", "In Company", "in-company"),
        ("blog.html", "Blog", "blog"),
        ("equipe.html", "Equipe", "equipe"),
        ("sobre.html", "Sobre", "sobre"),
        ("contato.html", "Contato", "contato"),
    ]
    nav_items = ""
    for href, label, key in links:
        cls = "text-ih-primary" if key == active else "text-slate-400 hover:text-ih-primary transition-colors"
        current = ' aria-current="page"' if key == active else ""
        nav_items += (
            f'\n        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] {cls}"'
            f' href="{asset_prefix}{href}"{current}>{label}</a>'
        )
    logo_current = ' aria-current="page"' if logo_aria_current else ""
    logo_class = "h-9 w-auto transition-transform group-hover:scale-105"
    return f"""  <header class="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-ih-primary/10">
    <nav class="flex items-center justify-between gap-3 px-6 lg:px-12 py-4">
      <a href="{asset_prefix}index.html" class="flex items-center group shrink-0"{logo_current}>
        <img src="{asset_prefix}../assets/imagens/institucional/logo-inforhealth-2020.png" alt="Inforhealth — Educação e Excelência em Saúde" class="{logo_class}"/>
      </a>
      <div class="site-nav-desktop hidden lg:flex items-center gap-5">{nav_items}
      </div>
{nav_actions_html(whatsapp_class)}
    </nav>
  </header>
{mobile_drawer_html()}"""


def mobile_nav_script_tag(asset_prefix: str = "") -> str:
    return f'<script src="{asset_prefix}js/mobile-nav.js"></script>'
