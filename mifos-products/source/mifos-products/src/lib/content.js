// content.js — the ONLY seam between the generic shell and per-project content.
// Reads content/site.yaml at build; every component pulls brand/copy/catalog from
// here. NOTHING is hardcoded in src/**. Swap content/ and the shell is a new site.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const CONTENT = path.join(ROOT, "content");

/** Load + parse the per-project site manifest (brand, hero, product catalog, nav, footer). */
export function loadSite() {
  const p = path.join(CONTENT, "site.yaml");
  if (!fs.existsSync(p)) {
    throw new Error(
      "[mifos-products] content/site.yaml not found — the shell has no built-in content.",
    );
  }
  return yaml.load(fs.readFileSync(p, "utf8")) || {};
}

/** Normalize a nav/footer/CTA href so a bare in-page anchor (#products) works from ANY route. */
export function href(h) {
  if (typeof h === "string" && h.startsWith("#")) return "/" + h;
  return h;
}

/** Attrs for a link that may be external (opens in new tab, safe rel). Spread onto <a>. */
export function linkAttrs(link) {
  if (link && link.external) return { target: "_blank", rel: "noopener noreferrer" };
  return {};
}
