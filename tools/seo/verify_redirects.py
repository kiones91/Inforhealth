import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_ROOT = REPO_ROOT / "site"
REDIRECTS_JSON = REPO_ROOT / "tools" / "seo" / "redirects-data.json"

def verify():
    if not REDIRECTS_JSON.exists():
        print("Erro: redirects-data.json não encontrado.")
        return False

    with open(REDIRECTS_JSON, encoding="utf-8") as f:
        redirects = json.load(f)

    print(f"Validando {len(redirects)} redirecionamentos...")
    errors = []
    
    # Track sources to detect duplicates
    sources = set()
    
    for r in redirects:
        src = r["from"]
        dst = r["to"]
        
        # 1. Check for duplicates
        if src in sources:
            errors.append(f"Origem duplicada: {src}")
        sources.add(src)
        
        # 2. Check for infinite loops / self-redirects
        if src.rstrip("/") == dst.rstrip("/"):
            errors.append(f"Loop infinito (auto-redirecionamento): {src} -> {dst}")
            
        # 3. Check if target page exists in `site`
        # Target URLs are clean (e.g., /sobre or /cursos/auditoria-clinica or /blog/artigos/governanca)
        # We need to map them back to .html filenames
        if dst == "/":
            target_file = SITE_ROOT / "index.html"
        elif dst == "/blog":
            target_file = SITE_ROOT / "blog.html"
        elif dst == "/cursos":
            target_file = SITE_ROOT / "cursos.html"
        elif dst.startswith("/cursos/"):
            slug = dst.split("/cursos/")[-1]
            target_file = SITE_ROOT / "cursos" / f"{slug}.html"
        elif dst.startswith("/blog/artigos/"):
            slug = dst.split("/blog/artigos/")[-1]
            target_file = SITE_ROOT / "blog" / "artigos" / f"{slug}.html"
        else:
            # institutional or other routes (e.g. /sobre, /contato, /equipe, /in-company, /academia-360, /ebook, /eventos)
            slug = dst.lstrip("/")
            target_file = SITE_ROOT / f"{slug}.html"
            
        if not target_file.exists():
            errors.append(f"Alvo inexistente: {src} -> {dst} (Arquivo {target_file.relative_to(REPO_ROOT)} não encontrado)")

    if errors:
        print(f"\n[FAIL] Falhas encontradas ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("\n[SUCCESS] Todos os redirecionamentos são válidos! Nenhuma duplicata, loop ou link quebrado encontrado.")
        return True

if __name__ == "__main__":
    import sys
    success = verify()
    sys.exit(0 if success else 1)
