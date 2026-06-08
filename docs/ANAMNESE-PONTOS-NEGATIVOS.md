# Anamnese — Pontos Negativos

> **Projeto:** Portal Inforhealth Educação  
> **Referência:** [edu.inforhealth.com.br](https://edu.inforhealth.com.br/)  
> **Data:** 07/06/2026  
> **Documento complementar:** `ANAMNESE-PONTOS-POSITIVOS.md`

---

## 1. Arquitetura técnica (crítico)

| Ponto | Impacto | Detalhe |
|-------|---------|---------|
| **Dois builders no mesmo portal** | Alto | Homepage e contato usam Website Builder (HostGator); equipe, cursos e blog usam WordPress + Elementor + WooCommerce — manutenção duplicada, visual inconsistente |
| **URLs duplicadas para cursos** | Alto | Mesmo curso pode existir em `/curso-xxx/` (landing) e `/cursos/xxx/` (WooCommerce legado) — confunde SEO e usuário |
| **~159 landing pages + 28 produtos** | Médio | Excesso de páginas soltas na raiz, muitas de eventos passados — dilui autoridade e dificulta gestão |
| **Sitemap.xml com erro 500** | Baixo | `sitemap.xml` direto falha; só `sitemap_index.xml` funciona — possível problema para crawlers menos tolerantes |
| **Páginas com URL malformada** | Médio | Ex.: `/https-edu-inforhealth-com-br-gestao-hospitalar-gestao-6-congresso-v2/` — lixo técnico indexado |

---

## 2. Navegação e experiência do usuário

| Ponto | Impacto | Detalhe |
|-------|---------|---------|
| **"Quem Somos" quebrado** | Alto | Menu aponta para `inforhealth.com.br/sobre/` que retorna **404** — primeira impressão negativa |
| **Dois domínios sem integração** | Alto | `edu.inforhealth.com.br` vs `inforhealth.com.br` — usuário não entende onde está a empresa vs. cursos |
| **Menu sobrecarregado** | Médio | Quem Somos · Equipe · Cursos · In Company · Pós · Consultoria · Contato · Blog — muitos itens, alguns externos |
| **Homepage vs. catálogo confuso** | Médio | Lista longa de cursos na home sem filtros claros; categorias existem mas não são o fluxo principal |
| **Congressos misturados ao catálogo** | Médio | Eventos de 2024/2025 ainda indexados junto com cursos permanentes — sensação de site desatualizado |
| **Dependência excessiva do WhatsApp** | Baixo | Para dúvidas funciona, mas falta formulário estruturado e jornada de compra self-service em parte dos fluxos |

---

## 3. Conteúdo e consistência

| Ponto | Impacto | Detalhe |
|-------|---------|---------|
| **Cursos duplicados na home** | Médio | "Formação de Auditores ONA 2026" aparece duas vezes na listagem ao vivo |
| **Nomenclatura inconsistente** | Médio | Mesmo tema com títulos variados entre home, landing e WooCommerce |
| **Profundidade desigual nos .md** | Médio | Alguns cursos extraídos têm FAQ rico; outros só resumo SEO e 3 bullet points |
| **Conteúdo FAQ genérico repetido** | Baixo | Várias páginas repetem blocos idênticos (pagamento Pix, Kiwify, certificado) — redundância no rebuild |
| **Blog desconectado** | Médio | URL longa (`blog_inforhealth-educacao-excelencia-saude`) e sem integração visual clara com o restante |
| **Parceiros/clientes ausentes** | Médio | 190+ empresas citadas, mas **sem logos ou cases** visíveis — prova social subaproveitada |

---

## 4. Assets e identidade visual

| Ponto | Impacto | Detalhe |
|-------|---------|---------|
| **Imagens genéricas na home** | Médio | Seções usam Unsplash e CDN HostGator — pouca identidade própria |
| **Múltiplas versões de logo** | Baixo | Vários crops e formatos (`logo_inforhealth_cursos`, `logo_inforhealth_2020`) — falta padronização |
| **Arquivos locais desorganizados** | Alto | Pasta `Cursos/` continha a homepage; `curso-in-company/` vazia; 251 arquivos com JS/CSS duplicados |
| **HTML monolítico** | Alto | Páginas salvas com 200–500 KB — impossível editar manualmente; dependência de script para extração |
| **Cobertura local mínima** | Alto | Apenas 4 de ~225 páginas baixadas (~1,7%) antes da reorganização |

---

## 5. SEO e performance

| Ponto | Impacto | Detalhe |
|-------|---------|---------|
| **Cannibalização de keywords** | Alto | Várias URLs competindo pelo mesmo curso/tema |
| **Páginas de evento expiradas indexadas** | Médio | Congressos passados ainda no sitemap — risco de conteúdo morto no Google |
| **Peso das páginas** | Médio | WordPress + Elementor + LiteSpeed + dezenas de scripts — carregamento provavelmente pesado |
| **HTTP 406 em fetch automatizado** | Baixo | Servidor bloqueia alguns user-agents — dificulta integrações e monitoramento automatizado |
| **Categoria `uncategorized`** | Baixo | Existe no sitemap — sinal de conteúdo mal classificado |

---

## 6. Operacional e gestão

| Ponto | Impacto | Detalhe |
|-------|---------|---------|
| **Gestão de conteúdo fragmentada** | Alto | Editar um curso pode exigir alterar landing Elementor + produto WooCommerce + card na home |
| **Sem fonte única de verdade** | Alto | Conteúdo espalhado entre builders, wp-content e CDN externo |
| **Eventos sem arquivamento** | Médio | Não há área "eventos passados" ou redirect — páginas ficam órfãs |
| **Docentes extras só nas LPs** | Médio | Renata Apolinário, Luan Henrique, Dra. Débora etc. aparecem em cursos mas não na página `/equipe/` |
| **Academia 360 pouco explorada** | Médio | Produto citado na home com link, mas sem conteúdo local organizado ainda |

---

## 7. Riscos para o novo portal (se não corrigidos)

| Risco | Consequência |
|-------|--------------|
| Replicar a estrutura atual | Manter caos de URLs e duplicidade |
| Migrar só a homepage | Perder 120+ landing pages ainda indexadas |
| Ignorar redirects 301 | Queda de tráfego orgânico na migração |
| Não unificar "Quem Somos" | Continuidade do link quebrado ou conteúdo duplicado |
| Não definir CMS único | Mesmo problema de manutenção em dobro |

---

## 8. Resumo — fragilidades principais

1. **Plataforma híbrida** (2 builders + WooCommerce legado)  
2. **Arquitetura de informação confusa** — URLs, duplicatas e eventos misturados  
3. **Identidade visual inconsistente** — logos, imagens stock e templates diferentes  
4. **Conteúdo difícil de manter** — sem repositório central antes deste projeto  
5. **Prova social incompleta** — números sim, logos de clientes não  
6. **Links quebrados** — Quem Somos em domínio externo com 404  

---

## 9. Prioridades sugeridas para o rebuild

| Prioridade | Ação |
|------------|------|
| P0 | Um único stack/CMS e uma URL por curso |
| P0 | Unificar institucional (sobre, equipe, contato) no mesmo domínio |
| P1 | Mapa de redirects 301 da estrutura antiga |
| P1 | Catálogo com filtros (modalidade + tema) substituindo lista infinita na home |
| P2 | Arquivar ou remover eventos expirados do sitemap |
| P2 | Página de clientes/parceiros com logos reais |
| P3 | Consolidar FAQ comum em componente reutilizável |

---

*Estes pontos devem orientar decisões na fase de arquitetura do novo portal (`REFERENCIA-PORTAL.md`).*
