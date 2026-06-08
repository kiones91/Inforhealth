# Deploy — Cloudflare Pages (`inforhealth.buffallos.com.br`)

## DNS — está certo?

| Config atual | Veredito |
|--------------|----------|
| `AAAA` → `100::` + proxy laranja | **Funciona** se o domínio foi vinculado pelo painel Pages/Workers |
| Padrão dos seus outros sites (`app`, `venda`) | **CNAME** → `projeto.pages.dev` |

**Recomendação:** use **CNAME** igual ao `app` e `venda`:

| Tipo | Nome | Conteúdo | Proxy |
|------|------|----------|-------|
| **CNAME** | `inforhealth` | `inforhealth.pages.dev` | Com proxy |

O `AAAA 100::` é um placeholder da Cloudflare — só resolve tráfego **depois** que o projeto Pages existir e o domínio customizado estiver ligado no painel.

---

## Passo a passo — Workers & Pages (Git)

### 1. Criar projeto

1. [Cloudflare Dashboard](https://dash.cloudflare.com) → **Workers & Pages** → **Create** → **Connect to Git**
2. Repositório: `kiones91/Inforhealth`
3. Configuração:

| Campo | Valor |
|-------|-------|
| **Project name** | `inforhealth` |
| **Production branch** | `main` |
| **Build command** | *(deixe vazio)* ou `npm install` |
| **Deployment command** | `npm install && npm run deploy` |
| **Non-production deploy** | `npm install && npm run deploy` |

> `npm run deploy` = build (`dist/`) + `wrangler deploy` no mesmo passo.  
> **Importante:** `dist/` nao pode estar no `.gitignore` — wrangler ignora arquivos gitignored.
| **Path** (avançado) | `/` *(raiz do repo)* |

O `wrangler.toml` na raiz aponta `[assets]` → `dist/`.

4. **Variáveis de ambiente:** nenhuma obrigatória
5. **API Token:** a Cloudflare cria automaticamente ao conectar o Git — não precisa preencher manualmente

### Alternativa — só Pages (sem Worker)

Se aparecer opção **Pages** (sem deploy command obrigatório):

| Campo | Valor |
|-------|-------|
| **Build command** | `python tools/deploy-build.py` |
| **Build output** | `dist` |
| **Deployment command** | *(vazio)* |

### 2. Domínio customizado

1. No projeto Pages → **Custom domains** → **Set up a custom domain**
2. Digite: `inforhealth.buffallos.com.br`
3. Se a zona `buffallos.com.br` já está na mesma conta, a Cloudflare cria/atualiza o DNS automaticamente

### 3. Conferir DNS (após vincular)

Deve ficar assim (igual `app` / `venda`):

```
inforhealth  CNAME  inforhealth.pages.dev  (proxied)
```

Se preferir manter `AAAA 100::`, também vale — desde que o domínio esteja **conectado no projeto Pages**.

---

## Estrutura publicada (`dist/`)

```
/
├── index.html
├── css/
├── js/
├── blog/
├── cursos/
├── sitemap.xml
├── robots.txt
├── _redirects
└── assets/
    └── imagens/
```

Gerada por:

```bash
python tools/deploy-build.py
```

---

## URLs limpas

O arquivo `site/_redirects` é copiado para `dist/` e funciona no Cloudflare Pages:

- `/cursos/slug` → `/cursos/slug.html`
- `/blog/artigos/slug` → `/blog/artigos/slug.html`

---

## Domínio do cliente (`edu.inforhealth.com.br`)

Quando o cliente apontar o DNS de `edu.inforhealth.com.br`:

1. Pages → **Custom domains** → adicionar `edu.inforhealth.com.br`
2. No DNS do cliente (ou na zona transferida): CNAME `edu` → `inforhealth.pages.dev` **ou** registro que a Cloudflare indicar

Atualize `tools/seo/seo-config.json` → `site_url` se o domínio canônico mudar, e rode `python tools/seo/run-seo.py`.

---

## Troubleshooting

| Problema | Causa provável |
|----------|----------------|
| 522 / erro de origem | Projeto Pages não deployou ou build falhou |
| Imagens quebradas | Build sem `deploy-build.py` (faltou pasta `assets/`) |
| DNS não resolve | CNAME/AAAA sem projeto Pages vinculado |
| 404 em `/cursos/foo` | `_redirects` ausente no `dist/` |
