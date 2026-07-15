#!/usr/bin/env node
// Inject the root registry.json into the data island of docs/index.html.
// Single source of truth: registry.json. The island in index.html is a
// generated artifact — re-run this whenever the registry changes.
//
//   node docs/build.mjs
//
// Zero dependencies. Idempotent: replaces only the marked <script> island.

import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const registryPath = join(here, "..", "registry.json");
const htmlPath = join(here, "index.html");

const ISLAND = /(<script id="registry" type="application\/json" data-registry>)([\s\S]*?)(<\/script>)/;

const raw = await readFile(registryPath, "utf8");
const registry = JSON.parse(raw); // throws on malformed registry — fail loud

const html = await readFile(htmlPath, "utf8");
if (!ISLAND.test(html)) {
  console.error("build: could not find the registry data island in index.html");
  process.exit(1);
}

// Compact JSON on one line, HTML-safe: escape "<" so a stray "</script>" in
// any field can't close the island early.
const payload = JSON.stringify(registry).replace(/</g, "\\u003c");
const next = html.replace(ISLAND, `$1\n${payload}\n  $3`);

if (next === html) {
  console.log("build: registry unchanged, index.html already current");
} else {
  await writeFile(htmlPath, next);
  const n = Array.isArray(registry.skills) ? registry.skills.length : 0;
  console.log(`build: injected ${n} module(s) from registry.json into docs/index.html`);
}
