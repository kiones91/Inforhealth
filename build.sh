#!/usr/bin/env bash
# Build para Cloudflare Workers/Pages (Linux/macOS/Git Bash)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DIST="$ROOT/dist"

rm -rf "$DIST"
mkdir -p "$DIST"

cp -r "$ROOT/site/." "$DIST/"
cp -r "$ROOT/assets" "$DIST/assets"

COUNT="$(find "$DIST" -type f | wc -l | tr -d ' ')"
echo "Build OK: $COUNT arquivos em dist/"
test -f "$DIST/index.html" || { echo "ERRO: dist/index.html ausente"; exit 1; }
