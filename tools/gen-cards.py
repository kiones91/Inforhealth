import re, os

INDEX = '../content/07-indice-cursos.md'
CURSOS_DIR = '../content/cursos'

AREA_MAP = {
    'gestao-rede-credenciada': 'suplementar', 'auditoria-clinica': 'qualidade',
    'formacao-auditores-ona-2026': 'qualidade', 'gestao-eficiente-em-saude': 'gestao',
    'governanca-360-saude-suplementar': 'governanca', 'plano-terapeutico-na-pratica': 'governanca',
    'gestao-estrategica-corpo-clinico': 'governanca', 'gestao-ciclo-receitas-hospitalares': 'faturamento',
    'mentoria-auditoria-qualidade': 'qualidade', 'custos-assistenciais-operadoras': 'suplementar',
    'drg-conceito-aplicacao': 'faturamento', 'gestao-tecnologias-infraestrutura': 'gestao',
    'recursos-glosas-saude-suplementar': 'suplementar', 'gestao-indicadores-em-saude': 'gestao',
    'gestao-pessoas-em-saude': 'gestao', 'governanca-regulatoria-ans-2026-2028': 'governanca',
    'auditoria-contas-medicas': 'faturamento', 'regulamentacao-planos-saude-ans': 'suplementar',
    'gestao-contratos-negociacao': 'suplementar', 'governanca-clinica': 'governanca',
    'mentoria-auditor-interno-qualidade': 'qualidade', 'marketing-em-saude': 'gestao',
    'workshop-telemedicina': 'gestao', 'planejamento-gestao-estrategica': 'gestao',
    'governanca-compliance-acreditacao': 'suplementar', 'formacao-gestao-contratos-negociacao': 'suplementar',
    'gestao-suprimentos-hospitalares': 'gestao', 'gestao-faturamento-em-saude': 'faturamento',
    'gestao-orcamentaria-financeira': 'gestao', 'gestao-projetos-metodologias-ageis': 'gestao',
    'seguranca-do-paciente': 'qualidade', 'gestao-assistencia-odontologica': 'gestao',
    'ferramentas-gestao-qualidade': 'qualidade', 'scih-seguranca-paciente': 'qualidade',
    'jornada-do-paciente': 'gestao', 'lideranca-profissionais-saude': 'gestao',
}

AREA_LABEL = {
    'qualidade': 'Qualidade e ONA', 'suplementar': 'Saúde Suplementar',
    'gestao': 'Gestão Hospitalar', 'faturamento': 'Faturamento', 'governanca': 'Governança',
}

SHORT = {
    'gestao-rede-credenciada': 'Gestão de Rede Credenciada', 'auditoria-clinica': 'Auditoria Clínica',
    'formacao-auditores-ona-2026': 'Formação Auditores ONA 2026', 'gestao-eficiente-em-saude': 'Gestão Eficiente em Saúde',
    'governanca-360-saude-suplementar': 'Governança 360° Saúde Suplementar', 'plano-terapeutico-na-pratica': 'Plano Terapêutico na Prática',
    'gestao-estrategica-corpo-clinico': 'Gestão Estratégica do Corpo Clínico', 'gestao-ciclo-receitas-hospitalares': 'Ciclo de Receitas Hospitalares',
    'mentoria-auditoria-qualidade': 'Mentoria Auditoria Interna', 'custos-assistenciais-operadoras': 'Custos Assistenciais para Operadoras',
    'drg-conceito-aplicacao': 'DRG do Conceito à Aplicação', 'gestao-tecnologias-infraestrutura': 'Gestão de Tecnologias em Saúde',
    'recursos-glosas-saude-suplementar': 'Recursos de Glosas', 'gestao-indicadores-em-saude': 'Gestão de Indicadores em Saúde',
    'gestao-pessoas-em-saude': 'Gestão de Pessoas em Saúde', 'governanca-regulatoria-ans-2026-2028': 'Governança Regulatória ANS 2026–2028',
    'auditoria-contas-medicas': 'Auditoria de Contas Médicas', 'regulamentacao-planos-saude-ans': 'Regulamentação ANS e Planos de Saúde',
    'gestao-contratos-negociacao': 'Gestão de Contratos e Negociação', 'governanca-clinica': 'Governança Clínica na Prática',
    'mentoria-auditor-interno-qualidade': 'Mentoria Auditor Interno', 'marketing-em-saude': 'Marketing em Saúde',
    'workshop-telemedicina': 'Workshop Telemedicina', 'planejamento-gestao-estrategica': 'Planejamento e Gestão Estratégica',
    'governanca-compliance-acreditacao': 'Governança, Compliance e Acreditação', 'formacao-gestao-contratos-negociacao': 'Formação em Contratos e Negociação',
    'gestao-suprimentos-hospitalares': 'Gestão de Suprimentos Hospitalares', 'gestao-faturamento-em-saude': 'Gestão de Faturamento em Saúde',
    'gestao-orcamentaria-financeira': 'Gestão Orçamentária e Financeira', 'gestao-projetos-metodologias-ageis': 'Gestão de Projetos Ágeis',
    'seguranca-do-paciente': 'Segurança do Paciente', 'gestao-assistencia-odontologica': 'Gestão da Assistência Odontológica',
    'ferramentas-gestao-qualidade': 'Ferramentas de Gestão da Qualidade', 'scih-seguranca-paciente': 'SCIH e Segurança do Paciente',
    'jornada-do-paciente': 'Jornada do Paciente', 'lideranca-profissionais-saude': 'Liderança para Profissionais de Saúde',
}

FEATURED = {'auditoria-clinica', 'drg-conceito-aplicacao', 'formacao-auditores-ona-2026', 'governanca-regulatoria-ans-2026-2028'}
BADGE = {'ao-vivo': ('course-badge--live', 'Ao Vivo'), 'gravado': ('course-badge--rec', 'Gravado'), 'mentoria': ('course-badge--mentoria', 'Mentoria')}

FALLBACK = {
    'qualidade': 'Capacitação em qualidade assistencial, acreditação e auditoria.',
    'suplementar': 'Especialização para operadoras e saúde suplementar.',
    'gestao': 'Gestão estratégica e operacional para líderes em saúde.',
    'faturamento': 'Faturamento, DRG e eficiência financeira hospitalar.',
    'governanca': 'Governança clínica e regulatória na prática.',
}

def excerpt(text, max_len=88):
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(' ', 1)[0] + '…'

courses = []
with open(INDEX, encoding='utf-8') as f:
    for line in f:
        m = re.match(r'\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\S+)\s*\|\s*\[([^\]]+)\]', line)
        if m:
            slug = m.group(4).replace('.md', '').replace('curso-', '')
            courses.append({'slug': slug, 'modalidade': m.group(3).strip(), 'file': f'{CURSOS_DIR}/{m.group(4)}'})

cards = []
for i, c in enumerate(courses):
    slug = c['slug']
    path = c['file']
    img = 'scih-seguranca-paciente.webp' if slug == 'seguranca-do-paciente' else None
    carga = None
    resumo = ''
    if os.path.exists(path):
        text = open(path, encoding='utf-8').read()
        im = re.search(r'!\[[^\]]*\]\(\.\./imagens/cursos/([^)]+)\)', text)
        if im:
            img = im.group(1)
        ch = re.search(r'\*\*Carga horária:\*\*\s*(.+)', text)
        if ch:
            carga = ch.group(1).strip()
        rm = re.search(r'## Resumo\s*\n\s*(.+)', text)
        if rm:
            resumo = excerpt(rm.group(1))

    area = AREA_MAP[slug]
    area_label = AREA_LABEL[area]
    badge_cls, badge_txt = BADGE[c['modalidade']]
    title = SHORT[slug]
    featured = ' course-card--featured' if slug in FEATURED else ''
    delay_attr = f' style="--card-delay:{(i % 12) * 45}ms"' if i < 12 else ''
    if not resumo:
        resumo = FALLBACK[area]

    chips = []
    if carga:
        chips.append(f'<span class="course-card-chip"><iconify-icon icon="solar:clock-circle-linear" width="13"></iconify-icon>{carga}</span>')
    if c['modalidade'] == 'mentoria':
        chips.append('<span class="course-card-chip"><iconify-icon icon="solar:user-speak-linear" width="13"></iconify-icon>1:1</span>')
    elif c['modalidade'] == 'gravado':
        chips.append('<span class="course-card-chip"><iconify-icon icon="solar:play-circle-linear" width="13"></iconify-icon>Assíncrono</span>')
    else:
        chips.append('<span class="course-card-chip"><iconify-icon icon="solar:videocamera-record-linear" width="13"></iconify-icon>Ao vivo</span>')
    chips.append('<span class="course-card-chip"><iconify-icon icon="solar:diploma-verified-linear" width="13"></iconify-icon>Certificado</span>')
    chips_html = '\n                '.join(chips)

    card = (
        f'          <article class="course-card course-card--premium{featured} catalog-card-enter"{delay_attr} '
        f'data-modalidade="{c["modalidade"]}" data-area="{area}">\n'
        f'            <a href="cursos/{slug}.html" class="course-card-link">\n'
        f'              <div class="course-card-cover">\n'
        f'                <img src="../assets/imagens/cursos/{img}" alt="{title}" loading="lazy">\n'
        f'                <div class="course-card-cover-overlay" aria-hidden="true"></div>\n'
        f'                <span class="course-badge {badge_cls}">{badge_txt}</span>\n'
        f'                <span class="course-badge course-badge--area">{area_label}</span>\n'
        f'              </div>\n'
        f'              <div class="course-card-body">\n'
        f'                <h3>{title}</h3>\n'
        f'                <p class="course-card-excerpt">{resumo}</p>\n'
        f'                <div class="course-card-chips">\n'
        f'                {chips_html}\n'
        f'                </div>\n'
        f'                <span class="course-card-cta">Explorar curso <iconify-icon icon="solar:arrow-right-linear" width="14"></iconify-icon></span>\n'
        f'              </div>\n'
        f'            </a>\n'
        f'          </article>'
    )
    cards.append(card)

with open('_course-cards-v2.html', 'w', encoding='utf-8') as out:
    out.write('\n\n'.join(cards))
print(len(cards), 'cards')
