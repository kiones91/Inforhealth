#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_ROOT = REPO_ROOT / "site"
CONTENT_ROOT = REPO_ROOT / "content"
TOOLS_ROOT = REPO_ROOT / "tools"
ASSETS_IMGS = REPO_ROOT / "assets" / "imagens"

def optimize_image_file(file_path: Path):
    if file_path.name == "favicon.png":
        return None
        
    try:
        orig_size = file_path.stat().st_size
        img = Image.open(file_path)
        
        # Determine category based on parent folder name
        category = file_path.parent.name
        
        # Decide new dimensions
        width, height = img.size
        new_width, new_height = width, height
        
        if category == "equipe":
            max_dim = 400
            if max(width, height) > max_dim:
                ratio = max_dim / max(width, height)
                new_width, new_height = int(width * ratio), int(height * ratio)
        elif category == "cursos":
            max_w = 600
            if width > max_w:
                ratio = max_w / width
                new_width, new_height = max_w, int(height * ratio)
        elif category == "institucional":
            max_w = 400
            if width > max_w:
                ratio = max_w / width
                new_width, new_height = max_w, int(height * ratio)
        elif category in {"hospitais", "parceiros"}:
            max_dim = 200
            if max(width, height) > max_dim:
                ratio = max_dim / max(width, height)
                new_width, new_height = int(width * ratio), int(height * ratio)
        elif category == "blog":
            max_w = 800
            if width > max_w:
                ratio = max_w / width
                new_width, new_height = max_w, int(height * ratio)
        else:
            max_dim = 800
            if max(width, height) > max_dim:
                ratio = max_dim / max(width, height)
                new_width, new_height = int(width * ratio), int(height * ratio)
                
        # Perform resize if dimensions changed
        if (new_width, new_height) != (width, height):
            # Convert to RGBA or RGB appropriately
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                img = img.convert("RGB").resize((new_width, new_height), Image.Resampling.LANCZOS)
                
        dest_path = file_path.with_suffix(".webp")
        
        # Save as WebP
        if img.mode in ("RGBA", "LA"):
            img.save(dest_path, "WEBP", quality=85)
        else:
            img.convert("RGB").save(dest_path, "WEBP", quality=85)
            
        img.close()
        new_size = dest_path.stat().st_size
        
        # Delete original file
        os.remove(file_path)
        
        saved_pct = (1 - (new_size / orig_size)) * 100
        print(f"Optimized {category}/{file_path.name}: {orig_size/1024:.1f}KB -> {new_size/1024:.1f}KB (Saved {saved_pct:.1f}%)")
        return file_path.name, dest_path.name
        
    except Exception as e:
        print(f"Error optimizing {file_path}: {e}")
        return None

def update_references():
    print("\nUpdating references in source files...")
    
    # Simple regex to replace .png / .jpg / .jpeg references inside images path
    # Except favicon.png
    pattern = re.compile(r'assets/imagens/(equipe|cursos|institucional|hospitais|parceiros|blog)/((?!favicon)[a-zA-Z0-9_\-\.\/]+)\.(png|jpg|jpeg)', re.I)
    
    # Also replace raw course/team filenames without path prefix (e.g. "auditoria-clinica.webp" -> "auditoria-clinica.webp")
    # For cursos
    curso_file_pat = re.compile(r'(?<![a-zA-Z0-9_\-\.\/])([a-zA-Z0-9_\-]+)\.(png|jpg|jpeg)(?=["\'\s])', re.I)
    
    extensions = {".html", ".md", ".json", ".py", ".js", ".css"}
    updated_files = 0
    
    # Walk all directories
    for root_dir in [SITE_ROOT, CONTENT_ROOT, TOOLS_ROOT]:
        for path in root_dir.rglob("*"):
            if path.is_file() and path.suffix in extensions:
                try:
                    content = path.read_text(encoding="utf-8", errors="replace")
                    new_content = pattern.sub(r'assets/imagens/\1/\2.webp', content)
                    
                    # Also replace local filenames in tools or content
                    # But exclude certain names like favicon
                    def repl_local_file(match):
                        name = match.group(1)
                        ext = match.group(2)
                        if name in {"favicon"}:
                            return match.group(0)
                        return f"{name}.webp"
                        
                    new_content = curso_file_pat.sub(repl_local_file, new_content)
                    
                    if new_content != content:
                        path.write_text(new_content, encoding="utf-8")
                        updated_files += 1
                except Exception as e:
                    print(f"Error updating file {path}: {e}")
                    
    print(f"References updated in {updated_files} files.")

def main():
    print("Starting image optimization pipeline...")
    if not ASSETS_IMGS.exists():
        print(f"Directory {ASSETS_IMGS} does not exist!")
        sys.exit(1)
        
    optimized_count = 0
    for path in ASSETS_IMGS.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            res = optimize_image_file(path)
            if res:
                optimized_count += 1
                
    print(f"\nOptimization completed. {optimized_count} images converted to WebP.")
    
    update_references()

if __name__ == "__main__":
    main()
