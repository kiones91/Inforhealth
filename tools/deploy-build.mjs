#!/usr/bin/env node
/** Build dist/ para deploy (Node — funciona no CI da Cloudflare). */
import { cp, rm, mkdir, readdir, stat } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SITE = join(ROOT, "site");
const ASSETS = join(ROOT, "assets");
const DIST = join(ROOT, "dist");

async function countFiles(dir) {
  let n = 0;
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) n += await countFiles(p);
    else n += 1;
  }
  return n;
}

async function main() {
  const index = join(DIST, "index.html");
  const isForce = process.env.FORCE_BUILD === "1" || process.argv.includes("--force");
  if (!isForce) {
    try {
      await stat(index);
      const total = await countFiles(DIST);
      console.log(`dist/ ja existe (${total} arquivos) — pulando rebuild`);
      return;
    } catch {
      /* gera dist */
    }
  }

  await rm(DIST, { recursive: true, force: true });
  await mkdir(DIST, { recursive: true });
  await cp(SITE, DIST, { recursive: true });
  await cp(ASSETS, join(DIST, "assets"), { recursive: true });

  // Remove o _redirects do Netlify que conflita com o roteamento da Cloudflare
  try {
    await rm(join(DIST, "_redirects"), { force: true });
    console.log("Removido dist/_redirects (Netlify) para evitar conflitos na Cloudflare");
  } catch (err) {
    console.warn("Aviso: não foi possível remover dist/_redirects:", err);
  }

  try {
    await stat(join(DIST, "index.html"));
  } catch {
    console.error("ERRO: dist/index.html ausente");
    process.exit(1);
  }

  const total = await countFiles(DIST);
  console.log(`Build OK: ${total} arquivos em dist/`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
