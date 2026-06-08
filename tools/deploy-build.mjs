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
  await rm(DIST, { recursive: true, force: true });
  await mkdir(DIST, { recursive: true });
  await cp(SITE, DIST, { recursive: true });
  await cp(ASSETS, join(DIST, "assets"), { recursive: true });

  const index = join(DIST, "index.html");
  try {
    await stat(index);
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
