# Blog — artigos do portal

Estrutura organizada do canal editorial Inforhealth.

## Pastas

| Caminho | Conteúdo |
|---------|----------|
| `../blog.html` | Listagem principal (página 1) |
| `../blog-pagina-2.html` · `../blog-pagina-3.html` | Paginação |
| `artigos/` | **36 páginas de artigo** (1 arquivo por slug) |
| `../js/blog-posts.json` | Metadados + conteúdo (fonte para regenerar) |
| `../../tools/scripts/generate-blog.py` | Script gerador |

## URL de um artigo

```
site/blog/artigos/{slug}.html
```

Exemplo: `site/blog/artigos/governanca-regulatoria-novo-modelo-ans-2026.html`

## Redirecionamentos legados

| URL antiga | Destino |
|------------|---------|
| `blog-artigo.html` | artigo ANS 2026 |
| `blog-artigo-drg.html` | artigo DRG |
| `blog-artigo-ona.html` | artigo Manual ONA |
| `blog-artigo-seguranca.html` | artigo Segurança do paciente |
| `blog/{slug}.html` | `blog/artigos/{slug}.html` |

## Regenerar páginas

```bash
cd tools/scripts
python generate-blog.py --from-json
```

## Índice (36 artigos)

- [Liderança na Saúde: Por que Estratégia sem Execução Destrói Resultados](artigos/lideranca-saude-estrategia-execucao-result.html) — Gestão em Saúde · 2026-04-23
- [Burnout na saúde: como identificar sinais precoces e evitar impactos na sua equipe](artigos/gestao-de-equipes-na-saude-burnoout.html) — Gestão em Saúde · 2026-04-22
- [Governança Regulatória na Saúde: o que muda com o novo modelo da ANS (2026-2028) e como se preparar](artigos/governanca-regulatoria-novo-modelo-ans-2026.html) — Gestão em Saúde · 2026-04-15
- [Guia Gratuito: DRG na prática](artigos/guia_drg_pratica.html) — Gestão em Saúde · 2025-05-05
- [O Valor dos Treinamentos e Cursos In Company para Instituições de Saúde](artigos/treinamentos-para-instituicoes-de-saude.html) — Sem Categoria · 2024-11-05
- [Planejamento Estratégico em Organizações de Saúde – 2025](artigos/planejamento-estrategico-organizacoes-saude.html) — Gestão em Saúde · 2024-10-01
- [Excelência Operacional em Saúde](artigos/excelencia-operacional-em-saude.html) — Gestão em Saúde · 2024-09-30
- [Auditoria em Gestão da Qualidade em Saúde](artigos/o-papel-do-manual-ona-para-hospitais.html) — Gestão em Saúde · 2024-09-27
- [Gestão de Custos Assistenciais para Operadoras de Planos de Saúde.](artigos/custos-assistenciais-operadoras-blog.html) — Faturamento · 2024-09-27
- [Modelo para Construção e Gestão de Protocolo Clínico da Inforhealth](artigos/modelo-para-construcao-e-gestao-de-protocolo-clinico-da-inforhealth.html) — Gestão em Saúde · 2024-09-26
- [Gestão Hospitalar: Inovações para Superar Desafios e Otimizar a Qualidade Assistencial](artigos/gestao-hospitalar-inovacoes-qualidade-saude.html) — Gestão em Saúde · 2024-09-25
- [Importância da Acreditação ONA para o Sistema de Saúde Brasileiro: Setores Público e Privado](artigos/acreditacao-ona-para-o-sistema-de-saude.html) — Sem Categoria · 2024-09-24
- [A Atuação do Médico Hospitalista](artigos/medico-hospitalista-e-sua-relevancia.html) — Sem Categoria · 2024-09-24
- [A Importância da Gestão de Contratos e Negociação na Saúde Suplementar](artigos/contratos-negociacao-saude-suplementar.html) — Gestão em Saúde · 2024-09-24
- [DRG E O MERCADO FUTURO NA SAÚDE 2024](artigos/drg-e-o-mercado-futuro-na-saude.html) — Gestão em Saúde · 2024-09-02
- [DRG no Brasil, os Principais desafios na implementação](artigos/principais-desafios-na-implementacao-do-drg.html) — Gestão em Saúde · 2024-08-22
- [Garantindo a Segurança no Atendimento de Saúde](artigos/garantindo-a-seguranca-no-atendimento.html) — Gestão em Saúde · 2024-06-12
- [Segurança do Paciente: Práticas Essenciais para um Cuidado de Excelência](artigos/seguranca-paciente-excelencia-cuidado.html) — Gestão em Saúde · 2024-06-06
- [A Tríade da Excelência na Saúde: Governança Clínica VBHC e MBE](artigos/governanca-clinica-vbhc-e-mbe-a-triade.html) — Gestão em Saúde · 2024-05-08
- [INSTRUMENTO DE GESTÃO DO CORPO CLÍNICO](artigos/instrumento-de-gestao-do-corpo-clinico.html) — Gestão em Saúde · 2023-09-13
- [MODELO DE PLANO DE AÇÃO PARA CONFORMIDADE COM A RN 518 DA ANS](artigos/modelo-de-plano-de-acao-para-conformidade-com-a-rn-518-da-ans.html) — Gestão em Saúde · 2023-09-05
- [MODELO DE CRIAÇÃO E GESTÃO DE INDICADORES EM SAÚDE](artigos/modelo-de-criacao-e-gestao-de-indicadores-de-saude.html) — Gestão em Saúde · 2023-09-04
- [A IMPORTÂNCIA VITAL DA AUDITORIA EM OPME E DMI NA ÁREA DA SAÚDE](artigos/modelo-para-construcao-de-protocolo-clinico.html) — Gestão em Saúde · 2023-08-23
- [MODELO PARA CONSTRUÇÃO DE PROTOCOLO CLÍNICO](artigos/implantacao-e-gestao-de-protocolos-clinicos-e-assustenciais.html) — Gestão em Saúde · 2023-08-08
- [RN 507 e sua Importância para Operadoras de Planos de Saúde￼](artigos/rn-507-e-sua-importancia-para-operadoras-de-planos-de-saude.html) — Gestão em Saúde · 2023-08-08
- [A IMPORTÂNCIA DA GESTÃO EFETIVA DO CORPO CLÍNICO EM ORGANIZAÇÕES DE SAÚDE￼￼](artigos/a-importancia-da-gestao-efetiva-do-corpo-clinico-em-organizacoes-de-saude.html) — Gestão em Saúde · 2023-08-08
- [A Importância da Gestão por Processos em Organizações de Saúde](artigos/a-importancia-da-gestao-por-processos-em-organizacoes-de-saude.html) — Gestão em Saúde · 2023-08-08
- [Como posso contribuir para aumentar a segurança do paciente](artigos/como-posso-contribuir-para-aumentar-a-seguranca-do-paciente.html) — Gestão em Saúde · 2023-04-27
- [Critérios Diagnósticos de Infecção Relacionada à Assistência à Saúde](artigos/blog-criterios-diagnosticos-de-infeccao-relacionada-a-assistencia-a-saude.html) — Gestão em Saúde · 2023-04-27
- [Abril pela Segurança do Paciente | Inforhealth [Sustentabilidade dos Sistemas de Saúde]](artigos/abril-pela-seguranca-do-paciente-inforhealth-sistemas-saude.html) — Gestão em Saúde · 2023-04-24
- [Abril pela Segurança do Paciente | Inforhealth [CONTROLE DE INFECÇÃO]](artigos/abril-pela-seguranca-do-paciente-inforhealth-controle-de-infeccao.html) — Gestão em Saúde · 2023-04-12
- [LIVES ABRIL –  CADASTRO CONCLUÍDO](artigos/lives-abril.html) — Gestão em Saúde · 2023-04-11
- [Abril pela Segurança do Paciente | Inforhealth [AUDITORIA]](artigos/abril-pela-seguranca-do-paciente-inforhealth.html) — Gestão em Saúde · 2023-04-11
- [LIDERANÇA EM SAÚDE – A evolução dos Sistemas de Saúde](artigos/lideranca-em-saude-a-evolucao-dos-sistemas-de-saude.html) — Sem Categoria · 2023-02-23
- [conheça os principais Indicadores de Qualidade Hospitalar:](artigos/conheca-os-principais-indicadores-de-qualidade-hospitalar.html) — Sem Categoria · 2022-02-09
- [Auditoria de Qualidade: Você sabe quais as vantagens para sua Organização?](artigos/auditoria-vantagens-para-sua-organizacao.html) — Sem Categoria · 2022-02-02
