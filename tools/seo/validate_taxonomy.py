import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT_ROOT = REPO_ROOT / "content"
INDEX_PATH = CONTENT_ROOT / "07-indice-cursos.md"
GEN_CARDS_PATH = REPO_ROOT / "tools" / "gen-cards.py"

def load_gen_cards_vars():
    """Loads AREA_MAP and SHORT from tools/gen-cards.py dynamically."""
    if not GEN_CARDS_PATH.exists():
        print(f"Erro: {GEN_CARDS_PATH} não encontrado.")
        return None, None
        
    content = GEN_CARDS_PATH.read_text(encoding="utf-8")
    
    # Extract AREA_MAP
    area_match = re.search(r"AREA_MAP = \{([^}]+)\}", content, re.S)
    # Extract SHORT
    short_match = re.search(r"SHORT = \{([^}]+)\}", content, re.S)
    
    exec_globals = {}
    if area_match:
        exec("AREA_MAP = {" + area_match.group(1) + "}", exec_globals)
    if short_match:
        exec("SHORT = {" + short_match.group(1) + "}", exec_globals)
        
    return exec_globals.get("AREA_MAP", {}), exec_globals.get("SHORT", {})

def load_index_courses():
    """Reads content/07-indice-cursos.md to get courses and their modalities."""
    if not INDEX_PATH.exists():
        print(f"Erro: {INDEX_PATH} não encontrado.")
        return []
        
    courses = []
    with open(INDEX_PATH, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(\S+)\s*\|\s*\[([^\]]+)\]", line)
            if m:
                title = m.group(1).strip()
                modality = m.group(2).strip().lower()
                filename = m.group(3)
                slug = filename.replace(".md", "").replace("curso-", "")
                courses.append({
                    "title": title,
                    "index_modality": modality,
                    "filename": filename,
                    "slug": slug,
                    "filepath": CONTENT_ROOT / "cursos" / filename
                })
    return courses

def parse_course_md_modality(filepath):
    """Parses a course markdown file to get its declared modality."""
    if not filepath.exists():
        return None
    content = filepath.read_text(encoding="utf-8")
    # Search for '**Modalidade:** Gravado' or '**Modalidade:** Ao Vivo' or '**Modalidade:** Mentoria'
    m = re.search(r"\*\*Modalidade:\*\*\s*(.+)", content, re.I)
    if m:
        val = m.group(1).strip().lower()
        if "ao vivo" in val:
            return "ao-vivo"
        elif "gravado" in val:
            return "gravado"
        elif "mentoria" in val:
            return "mentoria"
        return val
    return None

def validate():
    print("Iniciando validação cruzada da taxonomia dos cursos...")
    
    area_map, short_map = load_gen_cards_vars()
    courses = load_index_courses()
    
    if not courses:
        print("Nenhum curso encontrado no índice.")
        return False
        
    errors = []
    
    # Modality normalizations
    # Index uses: ao-vivo, gravado, mentoria
    # MD uses: Ao Vivo, Gravado, Mentoria
    
    print(f"Analisando {len(courses)} cursos...")
    
    for c in courses:
        slug = c["slug"]
        filepath = c["filepath"]
        
        # 1. Check if slug exists in AREA_MAP
        if slug not in area_map:
            errors.append(f"Área não definida: Curso '{c['title']}' (slug: {slug}) não está no AREA_MAP de gen-cards.py")
        
        # 2. Check if slug exists in SHORT map
        if slug not in short_map:
            errors.append(f"Nome curto não definido: Curso '{c['title']}' (slug: {slug}) não está no SHORT de gen-cards.py")
            
        # 3. Check if markdown file exists
        if not filepath.exists():
            errors.append(f"Arquivo ausente: {filepath.name} para o curso '{c['title']}'")
            continue
            
        # 4. Parse modality from Markdown and check consistency with index
        md_modality = parse_course_md_modality(filepath)
        if not md_modality:
            errors.append(f"Modalidade ausente no MD: Arquivo {filepath.name} não define '**Modalidade:**'")
        elif md_modality != c["index_modality"]:
            errors.append(f"Inconsistência de Modalidade: Curso '{c['title']}' no índice é '{c['index_modality']}', mas no MD é '{md_modality}'")

    if errors:
        print(f"\n[FAIL] Inconsistências encontradas ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("\n[SUCCESS] Taxonomia validada com sucesso! Todos os metadados estão 100% consistentes entre os Markdowns, o Índice e o Código.")
        return True

if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
