# Inforhealth — Portal Educação

Site estático do portal Inforhealth Educação e Excelência em Saúde.

## Estrutura

```
Inforhealth/
├── site/                 # Site publicável (HTML, CSS, JS, blog)
├── assets/imagens/       # Imagens (equipe, cursos, parceiros, institucional)
├── content/              # Conteúdo-fonte em Markdown (cursos, equipe, etc.)
├── tools/                # Scripts de build e manutenção
└── docs/                 # Documentação do projeto
```

## Visualizar localmente

Na pasta `site/`, sirva os arquivos com um servidor HTTP:

```bash
cd site
python -m http.server 8080
```

Abra [http://localhost:8080](http://localhost:8080).

> As imagens ficam em `assets/imagens/` (um nível acima de `site/`). O servidor precisa ser iniciado a partir de `site/` — os caminhos relativos `../assets/imagens/` funcionam corretamente.

## Regenerar conteúdo

**Catálogo de cursos** (a partir dos Markdown em `content/`):

```bash
cd tools
python build-cursos.py
```

**Artigos do blog** (a partir de `site/js/blog-posts.json`):

```bash
cd tools/scripts
python generate-blog.py --from-json
```

## Páginas principais

| Rota | Arquivo |
|------|---------|
| Home | `site/index.html` |
| Cursos | `site/cursos.html` |
| Blog | `site/blog.html` |
| Sobre | `site/sobre.html` |
| Equipe | `site/equipe.html` |
| Contato | `site/contato.html` |

## SEO

O portal inclui protocolo SEO automatizado. Após alterações no site:

```bash
cd tools/seo
python run-seo.py
```

Isso gera/atualiza:

- 36 landing pages em `site/cursos/{slug}.html`
- Meta tags (canonical, Open Graph, Schema.org) em todas as páginas
- `site/sitemap.xml` (85 URLs) e `site/robots.txt`

Documentação completa: [`docs/SEO-PROTOCOLO.md`](docs/SEO-PROTOCOLO.md)

## Deploy

Publique o conteúdo de `site/` e `assets/` mantendo a estrutura relativa:

```
/
├── index.html          ← conteúdo de site/
├── css/
├── js/
├── blog/
└── assets/
    └── imagens/
```

Ou configure o host para servir a raiz do repositório com `site/` como document root e `assets/` acessível via `../assets/` (GitHub Pages, Netlify, etc.).

## Licença

© Inforhealth Educação e Excelência em Saúde.
