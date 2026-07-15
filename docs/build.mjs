#!/usr/bin/env node
// Build the vitrine from the single source of truth, registry.json.
//
//   node docs/build.mjs
//
// Two steps:
//   1. Inject registry.json into the <script data-registry> island of every
//      page that has one (index.html and og-template.html). These islands are
//      generated artifacts — never hand-edit them.
//   2. Rasterize the Open Graph card (og-template.html -> og.png) with a system
//      headless Chrome/Chromium. This step is optional: if no browser is found,
//      it warns and leaves the existing og.png untouched. Point CHROME_BIN at a
//      binary to override discovery.
//
// No npm dependencies. Step 1 is pure Node; step 2 shells out to a browser.

import { readFile, writeFile } from "node:fs/promises";
import { existsSync, mkdtempSync, rmSync, statSync } from "node:fs";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { tmpdir } from "node:os";

const here = dirname(fileURLToPath(import.meta.url));
const registryPath = join(here, "..", "registry.json");
const ISLAND = /(<script id="registry" type="application\/json" data-registry>)([\s\S]*?)(<\/script>)/;

// ---- Step 1: inject the registry into every data island -------------------

const registry = JSON.parse(await readFile(registryPath, "utf8")); // fail loud on malformed registry
// Compact, HTML-safe: escape "<" so a stray "</script>" in any field can't close the island early.
const payload = JSON.stringify(registry).replace(/</g, "\\u003c");
const nSkills = Array.isArray(registry.skills) ? registry.skills.length : 0;

const islandTargets = ["index.html", "og-template.html"];
for (const name of islandTargets) {
  const path = join(here, name);
  const html = await readFile(path, "utf8");
  if (!ISLAND.test(html)) {
    console.error(`build: no registry island found in docs/${name}`);
    process.exit(1);
  }
  const next = html.replace(ISLAND, `$1\n${payload}\n  $3`);
  if (next === html) {
    console.log(`build: docs/${name} island already current`);
  } else {
    await writeFile(path, next);
    console.log(`build: injected ${nSkills} module(s) into docs/${name}`);
  }
}

// ---- Step 2: rasterize the OG card (needs a system browser) ---------------

function findChrome() {
  const named = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"];
  const absolute = [
    process.env.CHROME_BIN,
    process.env.CHROME_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  ].filter(Boolean);
  for (const p of absolute) if (existsSync(p)) return p;
  return named[0]; // fall back to PATH lookup; execFile throws ENOENT if absent
}

// Render by polling for the written screenshot, then killing the browser.
// Some Chrome builds don't self-exit after --screenshot, so waiting for a clean
// exit hangs; instead we watch og.png and stop the process once it's stable.
function renderOg(chrome, templatePath, ogPath, profile) {
  const before = existsSync(ogPath) ? statSync(ogPath).mtimeMs : 0;
  return new Promise((resolve) => {
    let proc;
    try {
      proc = spawn(chrome, [
        "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-color-profile=srgb", `--user-data-dir=${profile}`,
        "--window-size=1200,630", `--screenshot=${ogPath}`,
        `file://${templatePath}`,
      ], { stdio: "ignore" });
    } catch (e) { resolve({ ok: false, reason: e.code || e.message }); return; }

    let settled = false, lastSize = -1;
    const finish = (ok, reason) => {
      if (settled) return; settled = true;
      clearInterval(poll); clearTimeout(cap);
      try { proc.kill("SIGKILL"); } catch (_) {}
      resolve({ ok, reason });
    };
    proc.on("error", (e) => finish(false, e.code || e.message)); // e.g. ENOENT: no browser
    proc.on("exit", () => { if (fresh()) finish(true); });       // clean-exiting Chrome
    const fresh = () => existsSync(ogPath) && statSync(ogPath).mtimeMs > before;
    const poll = setInterval(() => {
      if (!fresh()) return;
      const size = statSync(ogPath).size;
      if (size > 1024 && size === lastSize) finish(true); // stable across two ticks
      lastSize = size;
    }, 400);
    const cap = setTimeout(() => finish(false, "timeout"), 40000);
  });
}

const templatePath = join(here, "og-template.html");
const ogPath = join(here, "og.png");
const profile = mkdtempSync(join(tmpdir(), "og-chrome-"));
try {
  const { ok, reason } = await renderOg(findChrome(), templatePath, ogPath, profile);
  if (ok) {
    console.log("build: rendered docs/og.png (1200x630)");
  } else if (reason === "ENOENT") {
    console.warn("build: no Chrome/Chromium found — set CHROME_BIN to regenerate og.png. Existing og.png unchanged.");
  } else {
    console.warn(`build: could not render og.png (${reason}). Existing og.png unchanged.`);
  }
} finally {
  rmSync(profile, { recursive: true, force: true });
}
