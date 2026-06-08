from pathlib import Path
import subprocess

SITE = Path(__file__).resolve().parent.parent / "site"

subprocess.run(['python3', 'gen-cards.py'], check=True, cwd=Path(__file__).resolve().parent)
cards = Path('_course-cards-v2.html').read_text(encoding='utf-8').rstrip()

html = f'''<!DOCTYPE html>
<html class="scroll-smooth" lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cursos — Inforhealth Educação</title>
  <meta name="description" content="Catálogo de cursos ao vivo, gravados e mentorias em gestão, qualidade e saúde suplementar — Inforhealth Educação.">
  <link rel="icon" href="../assets/imagens/institucional/favicon.png">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet"/>
  <link href="css/design-system.css" rel="stylesheet"/>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', 'system-ui', 'sans-serif'],
            display: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
            mono: ['Geist Mono', 'ui-monospace', 'monospace'],
          }},
          colors: {{
            ih: {{
              primary: '#09314d', secondary: '#2f80b5',
              accent: '#16a89a', 'accent-dark': '#118a7e', orange: '#ff8e2b',
              surface: '#ffffff', muted: '#f4f8fa',
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4, h5, h6 {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    iconify-icon {{ display: inline-flex; vertical-align: middle; }}
    .sr-only {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }}
  </style>
</head>
<body class="min-h-screen bg-stone-200 text-slate-900 antialiased selection:bg-ih-accent/30 selection:text-ih-primary p-3 lg:p-6">

<main class="w-full max-w-[1400px] mx-auto bg-white rounded-[2.5rem] shadow-2xl overflow-hidden relative">

  <header class="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-ih-primary/10">
    <nav class="flex items-center justify-between px-6 lg:px-12 py-4">
      <a href="index.html" class="flex items-center group">
        <img src="../assets/imagens/institucional/logo-inforhealth-2020.png" alt="Inforhealth — Educação e Excelência em Saúde" class="h-9 w-auto transition-transform group-hover:scale-105"/>
      </a>
      <div class="hidden lg:flex items-center gap-5">
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-ih-primary" href="cursos.html" aria-current="page">Cursos</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="eventos.html">Eventos</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="in-company.html">In Company</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="blog.html">Blog</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="equipe.html">Equipe</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="sobre.html">Sobre</a>
        <a class="text-[0.7rem] font-semibold uppercase tracking-[0.15em] text-slate-400 hover:text-ih-primary transition-colors" href="contato.html">Contato</a>
      </div>
      <a class="btn-glass btn-glass-accent btn-glass-sm" href="https://wa.me/5519997773084">
        <iconify-icon icon="solar:phone-linear" width="14"></iconify-icon> WhatsApp
      </a>
    </nav>
  </header>

  <!-- Hero -->
  <section class="relative px-8 lg:px-16 xl:px-24 pt-16 pb-12 overflow-hidden ds-grid-bg">
    <div class="beam-h top-16" style="animation-delay:0s;"></div>
    <div class="beam-v left-1/4 top-0" style="animation-delay:2s;"></div>
    <div class="orb w-72 h-72 bg-ih-accent/15 -top-20 -left-20"></div>
    <div class="orb w-96 h-96 bg-ih-primary/10 -top-10 right-0" style="animation-delay:-3s;"></div>
    <div class="relative z-10 max-w-3xl reveal">
      <div class="inline-flex items-center gap-2 border-gradient rounded-full px-4 py-1.5 bg-white/80 backdrop-blur-sm w-fit mb-6">
        <span class="flex h-2 w-2 relative">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-ih-accent opacity-60"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-ih-accent"></span>
        </span>
        <span class="text-[0.65rem] font-semibold uppercase tracking-[0.25em] text-slate-500">Catálogo permanente</span>
      </div>
      <h1 class="font-display font-bold tracking-tighter leading-[0.9] text-5xl lg:text-7xl mb-4">
        <span class="block text-transparent-gradient text-glow">Nossos Cursos</span>
      </h1>
      <p class="text-lg text-slate-600 leading-relaxed max-w-xl">
        Turmas ao vivo, gravados e mentorias com docentes referência no mercado. Para congressos e workshops pontuais, veja <a href="eventos.html" class="text-ih-accent font-medium hover:underline">Eventos</a>.
      </p>
    </div>
  </section>

  <!-- Catálogo -->
  <section class="catalog-section">
    <div class="catalog-trust reveal">
      <span><iconify-icon icon="solar:book-bookmark-linear" width="16"></iconify-icon> <strong>36</strong> programas de capacitação</span>
      <span><iconify-icon icon="solar:users-group-rounded-linear" width="16"></iconify-icon> <strong>6.000+</strong> profissionais formados</span>
      <span><iconify-icon icon="solar:diploma-verified-linear" width="16"></iconify-icon> Certificado <strong>LDB</strong> reconhecido</span>
      <span><iconify-icon icon="solar:shield-check-linear" width="16"></iconify-icon> Docentes <strong>avaliadores ONA</strong></span>
    </div>

    <div class="catalog-toolbar reveal">
      <div class="catalog-search-wrap">
        <iconify-icon icon="solar:magnifer-linear" width="18" class="catalog-search-icon"></iconify-icon>
        <input type="search" placeholder="Buscar por nome, área ou tema…" aria-label="Buscar curso" id="course-search-input" autocomplete="off">
      </div>
      <div class="catalog-pills" role="group" aria-label="Filtrar por modalidade">
        <button type="button" class="catalog-pill is-active" data-modality="all"><iconify-icon icon="solar:widget-5-linear" width="14"></iconify-icon> Todos</button>
        <button type="button" class="catalog-pill" data-modality="ao-vivo"><iconify-icon icon="solar:videocamera-record-linear" width="14"></iconify-icon> Ao Vivo</button>
        <button type="button" class="catalog-pill" data-modality="gravado"><iconify-icon icon="solar:play-circle-linear" width="14"></iconify-icon> Gravado</button>
        <button type="button" class="catalog-pill" data-modality="mentoria"><iconify-icon icon="solar:user-speak-linear" width="14"></iconify-icon> Mentoria</button>
      </div>
    </div>

    <div class="catalog-layout reveal">
      <aside class="catalog-filters" aria-label="Filtrar cursos por área">
        <div class="catalog-filters-header">
          <h2>Refinar</h2>
          <button type="button" class="catalog-filters-clear" id="clear-filters">Limpar</button>
        </div>
        <fieldset class="catalog-filter-group border-0 p-0 m-0">
          <legend>Área de atuação</legend>
          <label class="catalog-filter-option"><input type="checkbox" data-filter-group="area" data-filter="qualidade"> Qualidade e ONA <span class="catalog-filter-count" data-count-for="qualidade">0</span></label>
          <label class="catalog-filter-option"><input type="checkbox" data-filter-group="area" data-filter="suplementar"> Saúde Suplementar <span class="catalog-filter-count" data-count-for="suplementar">0</span></label>
          <label class="catalog-filter-option"><input type="checkbox" data-filter-group="area" data-filter="gestao"> Gestão Hospitalar <span class="catalog-filter-count" data-count-for="gestao">0</span></label>
          <label class="catalog-filter-option"><input type="checkbox" data-filter-group="area" data-filter="faturamento"> Faturamento <span class="catalog-filter-count" data-count-for="faturamento">0</span></label>
          <label class="catalog-filter-option"><input type="checkbox" data-filter-group="area" data-filter="governanca"> Governança <span class="catalog-filter-count" data-count-for="governanca">0</span></label>
        </fieldset>
        <div class="mt-5 pt-4 border-t border-ih-primary/10">
          <a href="in-company.html" class="flex items-center gap-2 text-sm font-semibold text-ih-accent hover:underline">
            <iconify-icon icon="solar:buildings-2-linear" width="16"></iconify-icon> Programas In Company
          </a>
        </div>
      </aside>

      <div class="flex-1 min-w-0">
        <div class="catalog-results-header">
          <p class="catalog-results-count" id="course-count" aria-live="polite">Mostrando <strong>36</strong> cursos</p>
          <div class="catalog-sort">
            <iconify-icon icon="solar:sort-linear" width="14"></iconify-icon>
            <label for="course-sort" class="sr-only">Ordenar cursos</label>
            <select id="course-sort" aria-label="Ordenar cursos">
              <option value="default">Relevância</option>
              <option value="az">A → Z</option>
              <option value="featured">Destaques primeiro</option>
            </select>
          </div>
        </div>

        <div class="course-grid" id="course-grid">

{cards}

        </div>

        <div class="catalog-empty" id="catalog-empty" role="status">
          <iconify-icon icon="solar:magnifer-linear"></iconify-icon>
          <h3>Nenhum curso encontrado</h3>
          <p>Tente outro termo de busca ou remova alguns filtros para ver mais opções.</p>
          <button type="button" id="empty-reset">Ver todos os cursos</button>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="px-8 lg:px-16 xl:px-24 pb-20">
    <div class="reveal blog-article-banner border-gradient">
      <div class="orb w-72 h-72 bg-ih-accent/30 -top-20 -left-10"></div>
      <div class="orb w-80 h-80 bg-ih-orange/15 -bottom-24 -right-10" style="animation-delay:-2s;"></div>
      <div class="relative z-10">
        <h2 class="font-display text-2xl lg:text-3xl font-bold tracking-tight">Não encontrou o curso ideal?</h2>
        <p class="text-white/70 mt-3 max-w-xl mx-auto text-sm lg:text-base">Montamos programas In Company sob medida para hospitais, operadoras e consultorias.</p>
        <div class="flex flex-wrap gap-4 justify-center mt-8">
          <div class="btn-glow-wrap">
            <a href="in-company.html" class="relative z-10 inline-flex items-center gap-2 bg-ih-accent hover:bg-ih-accent-dark text-white text-sm font-medium px-6 py-3 rounded-full transition-all hover:scale-[1.02]">
              <iconify-icon icon="solar:buildings-2-linear" width="18"></iconify-icon> Solicitar In Company
            </a>
            <span class="btn-glow"></span>
          </div>
          <a href="https://wa.me/5519997773084" class="inline-flex items-center gap-2 bg-white/10 backdrop-blur border border-white/30 text-white text-sm font-medium px-6 py-3 rounded-full hover:bg-white/20 transition-colors">
            <iconify-icon icon="solar:phone-linear" width="18"></iconify-icon> Falar no WhatsApp
          </a>
        </div>
      </div>
    </div>
  </section>

  <footer class="px-8 lg:px-16 xl:px-24 py-8 border-t border-ih-primary/10 text-center">
    <p class="text-sm text-slate-400">© 2026 Inforhealth Educação e Excelência em Saúde</p>
  </footer>

</main>

<a href="https://wa.me/5519997773084" class="btn-glass btn-glass-accent btn-glass-fab fixed bottom-6 right-6 z-50 shadow-xl" aria-label="WhatsApp">
  <iconify-icon icon="solar:chat-round-dots-bold" width="26"></iconify-icon>
</a>

<script src="js/catalog.js"></script>
</body>
</html>
'''

(SITE / 'cursos.html').write_text(html, encoding='utf-8')
print('site/cursos.html rebuilt')
