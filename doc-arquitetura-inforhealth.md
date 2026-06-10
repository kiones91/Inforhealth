# Documento de Arquitetura Técnica: Portal Inforhealth Educação

## 1. Visão Geral
O objetivo é migrar de uma estrutura híbrida fragmentada (WordPress + HostGator) para uma arquitetura de **Static Site Generation (SSG)**, visando performance extrema, segurança e facilidade de manutenção.

## 2. Stack Tecnológica Proposta
- **Framework**: Astro.build (devido à arquitetura de "Ilhas" que permite interatividade apenas onde necessário).
- **Gestão de Conteúdo (CMS)**: Headless CMS (ex: Strapi ou Sanity) para que a equipe de marketing publique sem tocar no código.
- **Hospedagem**: Vercel ou Netlify (Edge Computing para LCP < 2.5s).
- **Armazenamento de Ativos**: AWS S3 ou Cloudinary (para otimização automática de imagens/logos).

## 3. Diagrama de Fluxo de Dados
`CMS (Conteúdo/Markdown)` $\rightarrow$ `Build Pipeline (GitHub Actions)` $\rightarrow$ `Astro (Geração de HTML Estático)` $\rightarrow$ `CDN (Distribuição Global)` $\rightarrow$ `Usuário Final`

## 4. Soluções para Pontos Críticos

### 4.1 Unificação de Domínios e SEO
- **Canonicalization**: Implementação de tags `<link rel="canonical">` em todas as páginas para evitar conteúdo duplicado.
- **Redirection Engine**: Configuração de arquivo `_redirects` no nível do servidor para mapear todas as URLs antigas do WordPress para a nova estrutura.

### 4.2 Novo Catálogo de Cursos/Eventos
- **Estrutura**: Implementação de um sistema de filtragem via *Client-side JS* (React ou Vue) que consome um JSON gerado no build, permitindo filtros por:
    - **Modalidade**: (Online, Presencial, Híbrido).
    - **Tema**: (Gestão, Clínica, Tecnologia, etc).

### 4.3 Componentização
- **FAQ Component**: Componente único de Accordion consumindo dados via Markdown/CMS, garantindo consistência visual em todas as páginas.

## 5. Matriz de Infraestrutura
| Camada | Atual | Proposto | Ganho |
|--------|--------|----------|-------|
| Servidor | HostGator (Shared) | Edge Network (Vercel) | Latência $\downarrow$ |
| Renderização | SSR (WordPress) | SSG (Astro) | TTFB $\downarrow$ |
| Gestão | Painel WP | Headless CMS | Flexibilidade $\uparrow$ |
| Deploy | Manual/FTP | CI/CD (Git) | Confiabilidade $\uparrow$ |
```

---

O objetivo é migrar de uma estrutura híbrida fragmentada (WordPress + HostGator) para uma arquitetura de **Static Site Generation (SSG)**, visando performance extrema, segurança e facililidade de manutenção.
```markdown checklist-operacional-inforhealth.md
# Checklist Operacional: Implementação e Migração

## 🟢 Fase 1: Preparação e Inventário (Semana 1-2)
- [ ] Mapear todas as URLs atuais (`edu.inforhealth.com.br` e `inforhealth.com.br`).
- [ ] Exportar todos os posts e páginas do WordPress para formato `.md` ou `.json`.
- [ ] Inventariar todos os assets (imagens, PDFs e logos de parceiros).
- [ ] Definir a taxonomia de filtros (quais as categorias e tags oficiais de cada curso).

## 🔵 Fase 2: Desenvolvimento e Integração (Semana 3-6)
- [ ] Configurar repositório Git e pipeline de CI/CD.
- [ ] Desenvolver o layout base (Shell) e componentes globais (Header, Footer, FAQ).
- [ ] Implementar a lógica de filtragem do Catálogo.
- [ ] Configurar a integração com o Headless CMS.
- [ ] Criar o mapa de redirecionamentos 301 (Planilha de De $\rightarrow$ Para).

## 🟡 Fase 3: Validação e QA (Semana 7)
- [ ] Testar links quebrados (404) em todo o site.
- [ ] Validar renderização em dispositivos móveis (Responsividade).
- [ ] Testar a performance via Google PageSpeed Insights (Meta: LCP < 2.5s).
- [ ] Validar a indexação do novo `sitemap.xml` no Google Search Console.

## 🔴 Fase 4: Go-Live e Pós-Lançamento (Semana 8)
- [ ] Alteração de DNS para o domínio definitivo.
- [ ] Ativação dos redirects 301 no servidor de borda.
- [ ] Monitoramento de logs de erro por 72 horas.
- [ ] Treinamento operacional da equipe de conteúdo (CMS Tutorial).
- [ ] Backup final da instalação antiga do WordPress.

## 📈 KPIs de Sucesso
- [ ] **Performance**: Aumento na nota do Core Web Vitals.
- [ ] **SEO**: Estabilidade ou aumento no tráfego orgânico após a unificação.
- [ ] **UX**: Redução na taxa de rejeição (Bounce Rate) da homepage.