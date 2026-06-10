#!/usr/bin/env python3
"""Script de verificação de links quebrados (erros 404) em todo o site gerado em dist/."""
import json
import re
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DIST_ROOT = REPO_ROOT / "dist"
REDIRECTS_JSON = REPO_ROOT / "tools" / "seo" / "redirects-data.json"

def load_redirects():
    if REDIRECTS_JSON.exists():
        try:
            with open(REDIRECTS_JSON, encoding="utf-8") as f:
                data = json.load(f)
                # Map source to target for lookup
                return {r["from"].rstrip("/"): r["to"] for r in data}
        except Exception as e:
            print(f"Erro ao carregar redirecionamentos: {e}")
    return {}

def check_links():
    if not DIST_ROOT.exists():
        print(f"Erro: diretório de build '{DIST_ROOT}' não existe. Execute 'npm run build' primeiro.")
        return False

    redirects_map = load_redirects()
    html_files = list(DIST_ROOT.glob("**/*.html"))
    print(f"Escaneando {len(html_files)} arquivos HTML em '{DIST_ROOT.relative_to(REPO_ROOT)}'...")

    broken_links = []
    redirected_links = []
    checked_count = 0

    # Pattern to match src="..." or href="..."
    link_pattern = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        links = link_pattern.findall(content)
        
        file_relative = html_file.relative_to(DIST_ROOT)
        
        for link in links:
            # 1. Skip external/protocol-relative/anchor links/bypasses
            if (link.startswith("http://") or 
                link.startswith("https://") or 
                link.startswith("//") or 
                link.startswith("mailto:") or 
                link.startswith("tel:") or 
                link.startswith("javascript:") or 
                link.startswith("whatsapp:") or
                link.startswith("data:") or
                link.startswith("/cdn-cgi/") or
                link.startswith("#")):
                continue


            checked_count += 1
            
            # 2. Clean query strings and fragment identifiers
            cleaned_link = link.split("#")[0].split("?")[0]
            if not cleaned_link:
                continue
                
            # Decode URL characters (e.g. %20 -> space)
            cleaned_link = urllib.parse.unquote(cleaned_link)

            # 3. Determine target file path
            if cleaned_link.startswith("/"):
                # Root-relative path
                target_path = DIST_ROOT / cleaned_link.lstrip("/")
            else:
                # Relative path
                target_path = html_file.parent / cleaned_link

            # Normalize target path to resolve things like '..'
            target_path = target_path.resolve()

            # 4. Perform existence checks
            exists = False
            
            # If target exists directly
            if target_path.exists():
                exists = True
            else:
                # Check with .html appended (for URLs like /cursos/auditoria-clinica)
                if not target_path.suffix:
                    html_target = target_path.with_suffix(".html")
                    if html_target.exists():
                        exists = True
                
                # Check if it's a directory and has index.html
                if not exists and target_path.is_dir():
                    index_target = target_path / "index.html"
                    if index_target.exists():
                        exists = True

            # 5. If not found, check if it's a valid redirect
            if not exists:
                # Normalize link for redirect comparison (remove trailing slashes)
                normalized_link = "/" + str(cleaned_link).lstrip("/").rstrip("/")
                if normalized_link in redirects_map:
                    redirected_links.append({
                        "file": file_relative,
                        "link": link,
                        "redirect_to": redirects_map[normalized_link]
                    })
                else:
                    broken_links.append({
                        "file": file_relative,
                        "link": link,
                        "target_resolved": str(target_path.relative_to(REPO_ROOT) if target_path.is_relative_to(REPO_ROOT) else target_path)
                    })

    # Summary reports
    print(f"\nBusca concluída. {checked_count} links locais checados.")
    
    if redirected_links:
        print(f"\n[AVISO] Encontrados {len(redirected_links)} links que serão redirecionados (301):")
        for item in redirected_links[:20]:
            print(f"  - No arquivo '{item['file']}': link '{item['link']}' redireciona para '{item['redirect_to']}'")
        if len(redirected_links) > 20:
            print(f"  ... e mais {len(redirected_links) - 20} redirecionamentos.")

    if broken_links:
        print(f"\n[ERRO] Encontrados {len(broken_links)} links quebrados (404):")
        for item in broken_links:
            print(f"  - No arquivo '{item['file']}': link '{item['link']}' quebrado (não existe: {item['target_resolved']})")
        return False
    else:
        print("\n[SUCCESS] Nenhum link quebrado encontrado! Todos os recursos locais e URLs estão íntegros.")
        return True

if __name__ == "__main__":
    import sys
    success = check_links()
    sys.exit(0 if success else 1)
