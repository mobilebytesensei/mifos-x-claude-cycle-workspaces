# Product Idea — Mifos Products

> **Version**: 1.0
> **Last Updated**: 2026-08-15
> **Status**: Active

---

## Vision Statement

A single, fast, open-source showcase site for the Mifos suite of Digital Public
Goods — the migration of `products.mifos.org` (currently WordPress) onto Astro +
Cloudflare Pages, giving the community a maintainable, content-driven catalog of
every Mifos product in one place.

## Problem

`products.mifos.org` runs on WordPress: slow, harder to keep in sync with the
community, and not owned in the openMF codebase. Contributors can't update the
product catalog through a normal PR flow, and the site is decoupled from the
rest of the Mifos open-source estate.

## Solution

A static Astro site whose entire catalog is driven from one `content/site.yaml`
(+ theme-aware `tokens.css`). Adding or editing a product is a one-file PR; the
shell (`src/**`) is generic and brand-free. Deploys to Cloudflare Pages, cuts
over to `products.mifos.org`.

---

## Target Users

| Persona | Role | Primary Need | Key Workflow |
|---------|------|-------------|-------------|
| Prospective adopter | Bank / fintech / FI evaluator | Understand what Mifos offers and which product fits | Land → scan catalog → deep-link to the product's own site/docs |
| Community contributor | Developer / maintainer | Keep the catalog current | Edit `content/site.yaml` → PR → auto-deploy |
| Ecosystem partner | Integrator / DPI implementer | Find the right building block + repo | Catalog → GitHub / Slack |

---

## Core Value Propositions

1. **One catalog, always current** — every Mifos DPG in one place, updated by PR.
2. **Fast + free to host** — static Astro on Cloudflare Pages, no CMS to maintain.
3. **Content-driven & white-label** — one YAML drives the whole site; the shell is reusable.

---

## Platform & Technology

| Attribute | Value |
|-----------|-------|
| Platforms | web |
| Backend | none (pure static) |
| Project Type | web-app (Astro SSG) |

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Lighthouse performance | ≥ 95 | CI / Lighthouse audit |
| Catalog freshness | edits land via PR, deploy < 5 min | CF Pages build time |
| Products covered | all Mifos DPGs from products.mifos.org | manual catalog review |

---

## Constraints & Assumptions

### Technical Constraints
- Static output only (no server runtime); any dynamic data is build-time.
- Must build on Cloudflare Pages with `npm run build` → `dist/`.

### Business Constraints
- Content and destinations owned by the Mifos community; external product URLs
  must point at canonical Mifos properties.

### Assumptions
- Product deep-links (mifos.org, payments.mifos.org, mobile.mifos.org, …) remain stable.

---

## Known Limitations

- External product URLs are best-effort and need community confirmation (planned for v1.1).
- No per-product detail pages yet — cards deep-link out (planned for v1.1).

---

## Scope Boundaries

### In Scope
- Product catalog landing page mirroring products.mifos.org.
- Hero, product grid, community CTA, footer — theme-aware.

### Out of Scope
- Blog / news / events (lives on mifos.org).
- Any authenticated or dynamic functionality.

---

## Ideas Backlog

> Add ideas with `/idea add "description"`.

| # | Idea | From | Priority | Status | Added |
|:-:|------|------|:--------:|:------:|:-----:|
| 1 | Per-product detail pages | migration | P2 | backlog | 2026-08-15 |
| 2 | Localized (i18n) catalog | community | P3 | backlog | 2026-08-15 |
