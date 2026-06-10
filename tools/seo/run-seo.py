#!/usr/bin/env python3
"""Pipeline SEO completo — executar após alterações no site."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SEO_DIR = Path(__file__).resolve().parent
TOOLS = SEO_DIR.parent


def run(script: str) -> None:
    path = SEO_DIR / script
    print(f"\n>> {script}")
    subprocess.run([sys.executable, str(path)], check=True)


def run_npm_tailwind() -> None:
    frontend = TOOLS / "frontend"
    if not (frontend / "node_modules").exists():
        print("\n>> npm install (tailwind)")
        subprocess.run(["npm", "install"], check=True, cwd=str(frontend), shell=True)
    print("\n>> npm run build (tailwind)")
    subprocess.run(["npm", "run", "build"], check=True, cwd=str(frontend), shell=True)


def main() -> None:
    print("=== Protocolo SEO Inforhealth (Fase 1 + 2) ===")
    run("migrate-blog-images.py")
    run_npm_tailwind()
    run("generate-course-pages.py")
    run("apply-performance.py")
    subprocess.run(
        [sys.executable, "build-cursos.py"],
        check=True,
        cwd=str(TOOLS),
    )
    subprocess.run(
        [sys.executable, str(TOOLS / "scripts" / "inject-closing-footer.py")],
        check=True,
        cwd=str(TOOLS),
    )
    run("inject-seo.py")
    run("generate_redirects_data.py")
    run("generate-sitemap.py")
    print("\nOK Protocolo SEO concluido (imagens locais, tailwind, GA4, footer social)")



if __name__ == "__main__":
    main()
