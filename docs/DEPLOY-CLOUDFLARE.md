# Deploy — Cloudflare Worker (`inforhealth.buffallos.com.br`)

> Repositório: [kiones91/Inforhealth](https://github.com/kiones91/Inforhealth)  
> URL de homologação: https://inforhealth.buffallos.com.br/  
> Stack: **Worker com assets estáticos** (`wrangler.toml` → `dist/`), **não** Cloudflare Pages.

---

## Visão geral da ordem

```
1. Limpar DNS antigo
2. Criar registro DNS (antes do Worker)
3. Criar Worker + conectar GitHub
4. Vincular domínio customizado
5. Verificar deploy
```

---

## Etapa 0 — Limpeza (faça antes de tudo)

No painel Cloudflare:

1. **Workers & Pages** → delete o Worker/projeto `inforhealth` antigo (se existir).
2. **DNS** da zona `buffallos.com.br` → remova registros antigos de `inforhealth` (CNAME, AAAA, A, etc.).

---

## Etapa 1 — Configurar DNS (antes de criar o Worker)

1. Acesse [dash.cloudflare.com](https://dash.cloudflare.com) → zona **buffallos.com.br** → **DNS** → **Records**.
2. Clique em **Add record** e preencha:

| Campo | Valor |
|-------|-------|
| **Type** | `AAAA` |
| **Name** | `inforhealth` |
| **IPv6 address** | `100::` |
| **Proxy status** | **Proxied** (nuvem laranja) |
| **TTL** | Auto |

3. Salve o registro.

> O `AAAA 100::` é o placeholder padrão da Cloudflare para Workers na mesma conta. O tráfego só responde **depois** que o Worker existir e o domínio customizado estiver vinculado (etapa 4).

**Não use** `CNAME → inforhealth.pages.dev` — esse padrão é para **Pages**. Este projeto usa **Worker**.

---

## Etapa 2 — Criar o Worker e conectar o GitHub

1. **Workers & Pages** → **Create** → **Connect to Git**.
2. Autorize o GitHub e selecione o repositório **`kiones91/Inforhealth`**.
3. Configure o build:

| Campo | Valor |
|-------|-------|
| **Project name** | `inforhealth` |
| **Production branch** | `main` |
| **Root directory** | `/` *(raiz do repo)* |
| **Build command** | *(deixe vazio)* |
| **Deploy command** | `npm ci && npx wrangler deploy` |

4. **Environment variables:** nenhuma obrigatória.
5. **API Token:** a Cloudflare cria automaticamente ao conectar o Git — não precisa token manual.
6. Clique em **Save and Deploy** e aguarde o primeiro deploy.

### O que o deploy faz

- `wrangler.toml` na raiz define `name = "inforhealth"` e `[assets] directory = "dist"`.
- A pasta `dist/` (317 arquivos) está versionada no Git — o wrangler publica esses assets.
- `dist/` **não pode** estar no `.gitignore` (wrangler ignora arquivos gitignored).

### Log de sucesso esperado

```
Uploaded XXX assets
Deployed inforhealth triggers...
```

URL temporária: `https://inforhealth.<sua-conta>.workers.dev/`

---

## Etapa 3 — Vincular domínio customizado

1. **Workers & Pages** → **inforhealth** → **Settings** → **Domains & Routes**.
2. **Add** → **Custom domain**.
3. Digite: `inforhealth.buffallos.com.br`
4. Confirme. A Cloudflare deve reconhecer o registro `AAAA 100::` criado na etapa 1.

### Conferir DNS final

```
inforhealth  AAAA  100::  (proxied)
```

Status do domínio no painel: **Active**.

---

## Etapa 4 — Verificar

| URL | Esperado |
|-----|----------|
| https://inforhealth.buffallos.com.br/ | Home do portal |
| https://inforhealth.buffallos.com.br/cursos.html | Catálogo |
| https://inforhealth.buffallos.com.br/assets/imagens/... | Imagens carregando |

Se der erro 522 ou página em branco: o deploy falhou — veja **Deployments** → último build → log.

---

## Deploy automático (escolha **uma** opção)

### Opção A — Git da Cloudflare (recomendado para este projeto)

Já configurado na etapa 2. Cada `git push` na `main` dispara deploy automático.

Arquivo de referência: `.cf-deploy.json`

### Opção B — GitHub Actions

Workflow: `.github/workflows/deploy-cloudflare.yml`

Secrets necessários no GitHub (`Settings` → `Secrets`):

| Nome | Valor |
|------|-------|
| `CLOUDFLARE_API_TOKEN` | Token com permissão **Workers Scripts Edit** |
| `CLOUDFLARE_ACCOUNT_ID` | `0b131555c0c7837faef8b83205e05e54` |

> Se usar a Opção B, **desative** o build Git no painel Cloudflare para evitar dois deploys competindo.

---

## Atualizar o portal localmente

A pasta publicada é `site/` (fonte) → copiada para `dist/` (deploy):

```bash
# Rebuild dist/ a partir de site/ + assets/
FORCE_BUILD=1 npm run build

# Commit e push
git add site/ dist/
git commit -m "Atualizar portal"
git push origin main
```

O deploy na Cloudflare roda automaticamente após o push.

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

Gerada por `npm run build` (`tools/deploy-build.mjs`).

---

## Domínio de produção do cliente (`edu.inforhealth.com.br`)

Quando o cliente apontar o DNS:

1. Worker **inforhealth** → **Domains & Routes** → adicionar `edu.inforhealth.com.br`
2. Atualizar `tools/seo/seo-config.json` → `site_url` para o domínio canônico
3. Rodar SEO: `python tools/seo/run-seo.py` e rebuild `dist/`

Os canonicals em `site/` hoje apontam para `edu.inforhealth.com.br` (correto para produção futura).

---

## Troubleshooting

| Problema | Causa provável | Solução |
|----------|----------------|---------|
| 522 / erro de origem | Worker não deployou | Ver log em Deployments |
| 0 assets uploaded | `dist/` no `.gitignore` | Remover `dist/` do gitignore e commitar |
| DNS não resolve | Registro ausente ou DNS only | Conferir `AAAA 100::` proxied |
| 404 em `/cursos/foo` | URL sem `.html` | `wrangler.toml` já tem `html_handling = "auto-trailing-slash"` |
| Imagens quebradas | Build sem `assets/` | `FORCE_BUILD=1 npm run build` |
| Dois deploys conflitando | CF Git + GitHub Actions | Desativar um dos dois |
