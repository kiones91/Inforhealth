# Protocolo SEO — Portal Inforhealth

> Domínio canônico: **https://edu.inforhealth.com.br**  
> Atualizado: 07/06/2026

---

## 1. Objetivo

Manter o portal otimizado para indexação no Google com:

- URLs únicas por curso e artigo
- Metadados consistentes (canonical, Open Graph, Schema.org)
- Sitemap e robots.txt atualizados
- Redirecionamentos legados preservando link equity

---

## 2. Estrutura implementada

| Recurso | Caminho | Função |
|---------|---------|--------|
| Configuração | `tools/seo/seo-config.json` | Domínio, organização, prioridades |
| Biblioteca | `tools/seo/seo_lib.py` | Funções compartilhadas de SEO |
| Injeção de meta tags | `tools/seo/inject-seo.py` | Canonical, OG, Twitter, JSON-LD |
| Páginas de curso | `tools/seo/generate-course-pages.py` | 36 LPs em `site/cursos/` |
| Sitemap | `tools/seo/generate-sitemap.py` | Gera `site/sitemap.xml` |
| Pipeline | `tools/seo/run-seo.py` | Executa tudo em sequência |
| Robots | `site/robots.txt` | Regras de rastreamento |

---

## 3. URLs indexáveis (85 no sitemap)

| Tipo | Qtd | Padrão |
|------|-----|--------|
| Home | 1 | `/` |
| Institucional | 8 | `/sobre.html`, `/equipe.html`, etc. |
| Catálogo | 1 | `/cursos.html` |
| **Cursos (LPs)** | **36** | `/cursos/{slug}.html` |
| Blog listagem | 3 | `/blog.html`, `/blog-pagina-2.html`, … |
| Artigos | 36 | `/blog/artigos/{slug}.html` |

**Excluídos do sitemap:** 40 redirecionamentos, `design_system.html`, `curso.html` (redirect).

---

## 4. Schema.org por tipo de página

| Página | JSON-LD |
|--------|---------|
| Home | `Organization` + `EducationalOrganization` + `WebSite` + `Speakable` + geo/local |
| Curso | `Course` + `BreadcrumbList` + `Speakable` |
| Artigo | `Article` + `BreadcrumbList` + `Speakable` |
| Institucional | `BreadcrumbList` |

**SEO local e IA (Google AI Overviews):** `sameAs` com redes sociais, Google Maps e site institucional; coordenadas Campinas; `hasMap`; `contactPoint` com WhatsApp.

**Redes no rodapé:** Instagram, LinkedIn, Facebook, YouTube, WhatsApp e Google Maps em todas as páginas públicas.

---

## 5. Comandos — quando executar

### Após qualquer alteração no site

```bash
cd tools/seo
python run-seo.py
```

### Passo a passo do pipeline (Fase 1 + 2)

1. `migrate-blog-images.py` — imagens do blog para `assets/imagens/blog/`
2. `npm run build` em `tools/frontend/` — compila `site/css/tailwind.min.css`
3. `generate-course-pages.py` — regenera 36 LPs de curso
4. `apply-performance.py` — remove CDN Tailwind, usa CSS compilado
5. `build-cursos.py` — atualiza catálogo com links corretos
6. `inject-closing-footer.py` — footer premium + redes sociais
7. `inject-seo.py` — meta tags, JSON-LD, GA4
8. `generate-sitemap.py` — atualiza sitemap.xml

### Após regenerar o blog

```bash
cd tools/scripts
python generate-blog.py --from-json
cd ../seo
python run-seo.py
```

---

## 6. Deploy — checklist Google

- [ ] Publicar `site/` + `assets/` + `robots.txt` + `sitemap.xml`
- [ ] Verificar HTTPS em `edu.inforhealth.com.br`
- [ ] Cadastrar propriedade no **Google Search Console**
- [ ] Enviar sitemap: `https://edu.inforhealth.com.br/sitemap.xml`
- [ ] Definir `ga4_measurement_id` em `seo-config.json` e rodar `run-seo.py`
- [ ] Cadastrar/validar **Google Meu Negócio** (Campinas) com mesmo NAP do schema
- [ ] Solicitar indexação das páginas principais

---

## 7. Fase 2 — concluída (08/06/2026)

| Item | Status |
|------|--------|
| Imagens blog locais (`assets/imagens/blog/`) | 225/230 migradas |
| Tailwind compilado (`site/css/tailwind.min.css`) | CDN removido em 87 páginas |
| GA4 preparado (`<!-- ANALYTICS:BEGIN -->`) | Aguarda ID `G-XXXXXXXX` |
| URLs limpas | `.htaccess`, `_redirects`, `vercel.json` |
| Redes sociais no footer | 85 páginas |
| Schema local + speakable | Home, cursos e artigos |

## 8. Fases pendentes (Fase 3)

| Item | Impacto |
|------|---------|
| 5 imagens externas não migradas (domínios terceiros) | Substituir manualmente |
| `alt` descritivo em todas as imagens | Imagens + a11y |
| Política de privacidade | E-E-A-T + LGPD |
| Core Web Vitals em produção (PageSpeed) | Validar após deploy |

---

## 9. Configuração

Edite `tools/seo/seo-config.json` para alterar:

- `site_url` — domínio canônico
- `ga4_measurement_id` — ID do Google Analytics 4 (ex.: `G-ABC123XYZ`)
- `default_og_image` — imagem padrão de compartilhamento
- `organization` — dados da empresa, Maps, coordenadas
- `social` — URLs das redes sociais (sameAs + footer)
- `page_defaults` — títulos/descrições por página

---

## 10. Marcadores no HTML

Cada página contém bloco identificável:

```html
<!-- SEO:BEGIN -->
  <link rel="canonical" href="...">
  <meta property="og:...">
  <script type="application/ld+json">...</script>
<!-- SEO:END -->
```

O script `inject-seo.py` substitui esse bloco a cada execução (idempotente).
