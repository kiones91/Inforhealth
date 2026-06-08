# Como dar acesso para deploy (sem senha da Cloudflare)

Não compartilhe login/senha do painel. Use **API Token** ou **GitHub Actions**.

---

## Opção A — GitHub Actions (recomendado)

Deploy automático a cada `git push` na `main`.

### 1. Criar API Token na Cloudflare

1. [dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens)
2. **Create Token** → template **Edit Cloudflare Workers**
3. Permissões: Workers Scripts Edit + Account Settings Read
4. **Create Token** → copie o token (só aparece uma vez)

### 2. Pegar Account ID

No painel Cloudflare → qualquer página → barra lateral direita → **Account ID** (copiar)

### 3. Secrets no GitHub

Repositório `kiones91/Inforhealth` → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Nome | Valor |
|------|-------|
| `CLOUDFLARE_API_TOKEN` | token criado no passo 1 |
| `CLOUDFLARE_ACCOUNT_ID` | ID da conta |

### 4. Disparar deploy

- Push na `main` dispara sozinho, ou
- GitHub → **Actions** → **Deploy Cloudflare** → **Run workflow**

### 5. Domínio

O Worker `inforhealth` e `inforhealth.buffallos.com.br` já configurados no painel continuam válidos.

---

## Opção B — Deploy local (Cursor / terminal)

No terminal, na pasta do projeto:

```bash
npx wrangler login
```

Abre o navegador → autorize → volte ao chat e peça para rodar o deploy.

Ou com token (sessão atual):

```bash
export CLOUDFLARE_API_TOKEN="seu-token-aqui"
npm run deploy
```

No Windows (PowerShell):

```powershell
$env:CLOUDFLARE_API_TOKEN="seu-token-aqui"
npm run deploy
```

---

## Opção C — Desativar build Git da Cloudflare

Se usar GitHub Actions, no painel **Workers & Pages** → **inforhealth** → **Settings**:

- Desconecte o repositório Git **ou** pause builds automáticos

Evita dois deploys competindo.

---

## Verificar sucesso

Log deve mostrar centenas de assets:

```
Build OK: 317 arquivos em dist/
Uploaded XXX assets
```

URLs:

- https://inforhealth.kionesperegrino91.workers.dev/
- https://inforhealth.buffallos.com.br/
