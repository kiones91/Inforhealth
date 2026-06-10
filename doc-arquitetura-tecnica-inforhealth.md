# Documento de Arquitetura Técnica: Modernização do Portal Inforhealth Educação

## 1. Visão Geral
O objetivo é a transição de uma estrutura híbrida fragmentada (WordPress + HostGator + arquivos estáticos) para uma arquitetura de **Jamstack**, visando performance, SEO e facilidade de manutenção.

## 2. Stack Tecnológica Proposta
- **Framework**: Astro (ou 11ty) - Para geração de sites estáticos (SSG) com alta performance.
- **CMS (Content Management System)**: Strapi ou Contentful (Headless CMS) - Para gestão de cursos, eventos e FAQs sem dependência de código.
- **Hospedagem/Deploy**: Vercel ou Netlify - Com pipeline de CI/CD integrado ao GitHub.
- **Armazenamento de Imagens**: Cloudinary ou AWS S3 - Para otimização automática de assets.

## 3. Diagrama de Fluxo de Dados (Lógico)
`[CMS Headless]` $\rightarrow$ `[Build Process (Astro)]` $\rightarrow$ `[Static Assets (HTML/CSS/JS)]` $\rightarrow$ `[CDN/Edge Network]` $\rightarrow$ `[Usuário Final]`

## 4. Definições de Implementação

### 4.1. Estratégia de Unificação de Domínios
- **DNS**: Centralização de todas as zonas de DNS no Cloudflare.
- **Redirecionamento**: Implementação de regras de `_redirects` no nível do servidor para converter `edu.inforhealth.com.br/*