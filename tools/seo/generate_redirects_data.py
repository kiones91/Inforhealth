import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_ROOT = REPO_ROOT / "site"
CONTENT_ROOT = REPO_ROOT / "content"

# 1. Load blog articles mapping
blog_posts_path = SITE_ROOT / "js" / "blog-posts.json"
with open(blog_posts_path, encoding="utf-8") as f:
    posts = json.load(f)

blog_redirects = []
for p in posts:
    url = p["url"]
    slug_match = re.search(r"edu\.inforhealth\.com\.br/([^/]+)/", url)
    if slug_match:
        old_slug = slug_match.group(1)
        new_slug = p["slug"]
        blog_redirects.append({
            "from": f"/{old_slug}",
            "to": f"/blog/artigos/{new_slug}"
        })

# 2. Load courses index
index_path = CONTENT_ROOT / "07-indice-cursos.md"
courses_redirects = []

# Special course redirects based on identified exceptions
special_course_lps = {
    "gestao-estrategica-corpo-clinico": ["/gestao-estrategica-do-corpo-clinico", "/curso-gestao-estrategica-do-corpo-clinico"],
    "mentoria-auditoria-qualidade": ["/mentoria-auditoria-interna-e-gestao-da-qualidade"],
    "drg-conceito-aplicacao": ["/drg-do-conceito-a-aplicacao", "/curso-drg-do-conceito-a-aplicacao"],
    "governanca-regulatoria-ans-2026-2028": ["/governanca-regulatorio-estrategica", "/curso-governanca-regulatorio-estrategica"]
}

special_course_woos = {
    "drg-conceito-aplicacao": ["/cursos/drg-do-conceito-a-aplicacao"]
}

with open(index_path, encoding="utf-8") as f:
    for line in f:
        m = re.match(r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(\S+)\s*\|\s*\[([^\]]+)\]", line)
        if m:
            title = m.group(1).strip()
            filename = m.group(3)
            slug = filename.replace(".md", "").replace("curso-", "")
            
            # Standard LP
            lp_sources = [f"/curso-{slug}"]
            if slug in special_course_lps:
                lp_sources.extend(special_course_lps[slug])
                
            # Standard WooCommerce
            woo_sources = [f"/cursos/{slug}"]
            if slug in special_course_woos:
                woo_sources.extend(special_course_woos[slug])
                
            for src in lp_sources:
                courses_redirects.append({
                    "title": title,
                    "from": src,
                    "to": f"/cursos/{slug}",
                    "type": "Landing Page"
                })
            for src in woo_sources:
                if src != f"/cursos/{slug}":
                    courses_redirects.append({
                        "title": title,
                        "from": src,
                        "to": f"/cursos/{slug}",
                        "type": "WooCommerce"
                    })

# 3. Institutional Redirects
institutional_redirects = [
    {"from": "/sobre", "to": "/sobre", "type": "Institucional"},
    {"from": "/contato", "to": "/contato", "type": "Institucional"},
    {"from": "/equipe", "to": "/equipe", "type": "Institucional"},
    {"from": "/curso-in-company", "to": "/in-company", "type": "Institucional"},
    {"from": "/academia-corporativa-360", "to": "/academia-360", "type": "Institucional"},
    {"from": "/ebook", "to": "/ebook", "type": "Institucional"},
    {"from": "/e-book", "to": "/ebook", "type": "Institucional"},
    {"from": "/eventos", "to": "/eventos", "type": "Institucional"},
    {"from": "/blog_inforhealth-educacao-excelencia-saude", "to": "/blog", "type": "Institucional"}
]

# Create full flat redirect list
all_redirects = []
all_redirects.extend(institutional_redirects)

for r in courses_redirects:
    all_redirects.append({
        "from": r["from"],
        "to": r["to"],
        "type": f"Curso ({r['type']})"
    })

for r in blog_redirects:
    all_redirects.append({
        "from": r["from"],
        "to": r["to"],
        "type": "Artigo do Blog"
    })

# Filter out self-redirects to prevent infinite loops in all config files
all_redirects = [r for r in all_redirects if r["from"].rstrip("/") != r["to"].rstrip("/")]

# Add trailing slash versions automatically for Netlify & Vercel
expanded_redirects = []
for r in all_redirects:
    # Remove trailing slash to normalize the base 'from'
    base_from = r["from"].rstrip("/")
    base_to = r["to"].rstrip("/")
    
    # Skip self-redirects to avoid infinite loops!
    if base_from == base_to:
        continue
    
    # Append the base redirect
    expanded_redirects.append({
        "from": base_from,
        "to": r["to"],
        "type": r["type"]
    })
    # Append the trailing slash redirect
    expanded_redirects.append({
        "from": base_from + "/",
        "to": r["to"],
        "type": r["type"]
    })

# Deduplicate expanded redirects
seen_froms = set()
deduped_redirects = []
for r in expanded_redirects:
    if r["from"] not in seen_froms:
        seen_froms.add(r["from"])
        deduped_redirects.append(r)

# Sort by length descending
deduped_redirects.sort(key=lambda x: -len(x["from"]))

# 4. Generate docs/mapa-urls-inforhealth.md
docs_path = REPO_ROOT / "docs" / "mapa-urls-inforhealth.md"
with open(docs_path, "w", encoding="utf-8") as out:
    out.write("# Mapa de Redirecionamentos 301 — Portal Inforhealth\n\n")
    out.write("> Este documento contém o mapeamento estratégico e técnico de URLs antigas para a nova estrutura do portal.\n\n")
    
    out.write("## 1. Páginas Institucionais\n\n")
    out.write("| URL de Origem (Antiga) | URL de Destino (Nova) | Tipo / Observação |\n")
    out.write("| :--- | :--- | :--- |\n")
    for r in sorted(institutional_redirects, key=lambda x: x["from"]):
        out.write(f"| `{r['from']}/` | `{r['to']}` | Unificação institucional |\n")
    out.write("\n")
    
    out.write("## 2. Cursos (WooCommerce & Landing Pages)\n\n")
    out.write("| Nome do Curso | URL de Origem (Antiga) | URL de Destino (Nova) | Origem |\n")
    out.write("| :--- | :--- | :--- | :--- |\n")
    for r in sorted(courses_redirects, key=lambda x: (x["title"], x["from"])):
        out.write(f"| {r['title']} | `{r['from']}/` | `{r['to']}` | {r['type']} |\n")
    out.write("\n")
    
    out.write("## 3. Artigos do Blog (WordPress)\n\n")
    out.write("| Título do Artigo | URL de Origem (Antiga) | URL de Destino (Nova) |\n")
    out.write("| :--- | :--- | :--- |\n")
    post_map = {p["slug"]: p["title"] for p in posts}
    for r in sorted(blog_redirects, key=lambda x: x["from"]):
        slug = r["to"].split("/")[-1]
        title = post_map.get(slug, "Artigo do Blog")
        out.write(f"| {title} | `{r['from']}/` | `{r['to']}` |\n")

print(f"Gerado {docs_path} com {len(all_redirects)} mapeamentos básicos.")

# Save JSON data
with open(REPO_ROOT / "tools" / "seo" / "redirects-data.json", "w", encoding="utf-8") as f:
    json.dump(deduped_redirects, f, indent=2, ensure_ascii=False)


# 5. Write site/_redirects
redirects_file_path = SITE_ROOT / "_redirects"
old_content = ""
if redirects_file_path.exists():
    old_content = redirects_file_path.read_text(encoding="utf-8")

clean_rules = []
for line in old_content.splitlines():
    if line.strip() and not line.strip().startswith("#") and "301" not in line:
        clean_rules.append(line)

new_redirects_lines = ["# Redirects 301 (gerados automaticamente)"]
for r in deduped_redirects:
    new_redirects_lines.append(f"{r['from']} {r['to']} 301")

new_redirects_lines.append("")
new_redirects_lines.append("# Netlify — URLs limpas")
new_redirects_lines.extend(clean_rules)

redirects_file_path.write_text("\n".join(new_redirects_lines) + "\n", encoding="utf-8")
print(f"Updated {redirects_file_path}")


# 6. Write site/vercel.json
vercel_path = SITE_ROOT / "vercel.json"
vercel_data = {}
if vercel_path.exists():
    with open(vercel_path, encoding="utf-8") as f:
        vercel_data = json.load(f)

vercel_data["redirects"] = [
    {"source": r["from"], "destination": r["to"], "permanent": True}
    for r in deduped_redirects
]

with open(vercel_path, "w", encoding="utf-8") as f:
    json.dump(vercel_data, f, indent=2, ensure_ascii=False)
print(f"Updated {vercel_path}")


# 7. Write site/.htaccess (using RedirectMatch for exact match to prevent prefix issues)
htaccess_path = SITE_ROOT / ".htaccess"
htaccess_lines = []
if htaccess_path.exists():
    content = htaccess_path.read_text(encoding="utf-8")
    content_clean = re.sub(r"# Redirects 301 \(gerados\)[\s\S]*?# Fim dos Redirects 301\n?", "", content)
    htaccess_lines.append(content_clean.strip())

apache_redirects = ["# Redirects 301 (gerados)"]
for r in sorted(all_redirects, key=lambda x: -len(x["from"])):
    # RedirectMatch 301 ^/slug/?$ /target
    base_from = r["from"].rstrip("/")
    apache_redirects.append(f"RedirectMatch 301 ^{base_from}/?$ {r['to']}")
apache_redirects.append("# Fim dos Redirects 301\n")

new_htaccess = "\n".join(apache_redirects) + "\n" + "\n".join(htaccess_lines)
htaccess_path.write_text(new_htaccess, encoding="utf-8")
print(f"Updated {htaccess_path}")
