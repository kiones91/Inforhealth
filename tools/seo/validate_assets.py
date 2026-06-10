import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT_ROOT = REPO_ROOT / "content"
IMAGES_ROOT = REPO_ROOT / "assets" / "imagens"
CURSOS_IMAGES = IMAGES_ROOT / "cursos"

def get_courses():
    index_path = CONTENT_ROOT / "07-indice-cursos.md"
    courses = []
    with open(index_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(\S+)\s*\|\s*\[([^\]]+)\]", line)
            if m:
                title = m.group(1).strip()
                filename = m.group(3)
                slug = filename.replace(".md", "").replace("curso-", "")
                courses.append({
                    "title": title,
                    "slug": slug,
                    "file": CONTENT_ROOT / "cursos" / filename
                })
    return courses

def check_images(courses):
    results = []
    missing = []
    
    for c in courses:
        slug = c["slug"]
        md_file = c["file"]
        
        # Determine expected image name (default is {slug}.webp, .png or .jpg)
        default_webp = CURSOS_IMAGES / f"{slug}.webp"
        default_png = CURSOS_IMAGES / f"{slug}.png"
        default_jpg = CURSOS_IMAGES / f"{slug}.jpg"
        
        found_image = None
        source_of_image = "default (slug)"
        
        # Check standard default image files
        if default_webp.exists():
            found_image = default_webp
        elif default_png.exists():
            found_image = default_png
        elif default_jpg.exists():
            found_image = default_jpg
        
        # If not found, check the markdown file for an image link
        if not found_image and md_file.exists():
            content = md_file.read_text(encoding="utf-8")
            # Look for markdown image like ![alt](../../imagens/cursos/filename.ext)
            img_match = re.search(r"!\[[^\]]*\]\([^)]*imagens/cursos/([^)]+)\)", content)
            if img_match:
                img_name = img_match.group(1)
                custom_img_path = CURSOS_IMAGES / img_name
                if custom_img_path.exists():
                    found_image = custom_img_path
                    source_of_image = "custom (md file link)"
                else:
                    found_image = None
                    source_of_image = f"custom-broken ({img_name})"
        
        if found_image:
            results.append({
                "title": c["title"],
                "slug": slug,
                "image_name": found_image.name,
                "status": "Found",
                "source": source_of_image
            })
        else:
            missing.append(c)
            results.append({
                "title": c["title"],
                "slug": slug,
                "image_name": "N/A",
                "status": "Missing",
                "source": source_of_image
            })
            
    return results, missing

def main():
    print("Iniciando validação de assets de cursos...")
    courses = get_courses()
    results, missing = check_images(courses)
    
    print("\n--- Relatório de Assets de Cursos ---")
    for r in results:
        status_symbol = "[OK]" if r["status"] == "Found" else "[MISSING]"
        print(f"{status_symbol} {r['title']} -> {r['image_name']} ({r['source']})")
        
    print("\n--- Resumo ---")
    print(f"Total de Cursos: {len(courses)}")
    print(f"Cursos com imagem: {len(courses) - len(missing)}")
    print(f"Cursos com imagem ausente: {len(missing)}")
    
    if missing:
        print("\nCursos pendentes de imagem:")
        for m in missing:
            print(f"  - {m['title']} (Slug: {m['slug']})")
            
if __name__ == "__main__":
    main()
