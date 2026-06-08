#!/usr/bin/env bash
# Build para Cloudflare Workers/Pages (Linux/macOS/Git Bash)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DIST="$ROOT/dist"

if [ -f "$DIST/index.html" ] && [ "${FORCE_BUILD:-0}" != "1" ]; then
  COUNT="$(find "$DIST" -type f | wc -l | tr -d ' ')"
  echo "dist/ ja existe ($COUNT arquivos) — pulando rebuild"
  exit 0
fi

rm -rf "$DIST"
mkdir -p "$DIST"

cp -r "$ROOT/site/." "$DIST/"
cp -r "$ROOT/assets" "$DIST/assets"

COUNT="$(find "$DIST" -type f | wc -l | tr -d ' ')"
echo "Build OK: $COUNT arquivos em dist/"
test -f "$DIST/index.html" || { echo "ERRO: dist/index.html ausente"; exit 1; }
