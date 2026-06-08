# Portal Novo — Inforhealth Educação

Pasta de trabalho para reorganizar conteúdo e construir o novo portal de cursos.

## Status (07/06/2026)

- [x] Análise da estrutura do site → `00-ANALISE-ESTRUTURA-SITE.md`
- [x] **Passo 1** — Imagens organizadas e renomeadas
- [x] **Passo 2** — Conteúdo extraído em Markdown
- [x] Anamnese positivos/negativos → `ANAMNESE-PONTOS-POSITIVOS.md` · `ANAMNESE-PONTOS-NEGATIVOS.md`
- [x] Referência + esqueleto HTML → `REFERENCIA-PORTAL.md` · `site/`
- [ ] Design visual (CSS final, identidade)

## Estrutura

```

├── 00-ANALISE-ESTRUTURA-SITE.md
├── ANAMNESE-PONTOS-POSITIVOS.md
├── ANAMNESE-PONTOS-NEGATIVOS.md
├── README.md
├── tools/
│   └── organizar_conteudo.py      ← script reutilizável
├── content/
│   ├── 01-sobre-empresa.md
│   ├── 02-equipe.md               ← 14 perfis com fotos
│   ├── 03-modalidades.md
│   ├── 04-in-company.md
│   ├── 05-contato.md
│   ├── 06-parceiros.md
│   ├── 07-indice-cursos.md        ← índice dos 36 cursos
│   └── cursos/                    ← 36 arquivos .md (1 por curso)
├── site/                     ← wireframe HTML navegável
│   ├── index.html                 ← home fusionada Ref.1 + Ref.2
│   ├── cursos.html · curso.html
│   ├── eventos.html · evento.html
│   ├── blog.html · blog-pagina-2.html · blog-pagina-3.html
│   ├── blog/                      ← canal editorial
│   │   ├── README.md              ← índice dos 36 artigos
│   │   └── artigos/               ← 1 HTML por slug
│   ├── js/blog-posts.json         ← metadados do blog
│   ├── scripts/generate-blog.py   ← regenerar listagem + artigos
│   ├── blog-artigo*.html          ← redirecionamentos legados
│   ├── in-company.html · academia-360.html · ebook.html
│   └── equipe.html · sobre.html · contato.html
└── imagens/
    ├── README-IMAGENS.md
    ├── CATALOGO-IMAGENS.json
    ├── equipe/                    ← 13 fotos
    ├── cursos/                    ← 35 thumbs/docentes
    ├── institucional/             ← logos + favicon
    └── parceiros/                 ← (vazio — aguardando cliente)
```

## Conteúdo gerado

| Tipo | Qtd | Pasta |
|------|-----|-------|
| Cursos (homepage) | 36 | `content/cursos/` |
| Equipe docente | 14 | `content/02-equipe.md` |
| Institucional | 5 arquivos | `content/01-*.md` … `06-*.md` |
| Imagens equipe | 13 | `imagens/equipe/` |
| Imagens cursos | 35 | `imagens/cursos/` |
| Logos | 4 | `imagens/institucional/` |

## Reexecutar extração

```bash
cd "_scripts"
python organizar_conteudo.py
```

## Fonte original

Arquivos brutos em: `../` (`Clientes/Inforhealth/`)
