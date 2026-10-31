# Changelog — Mifos Products (idea-layer)

## 2026-08-15 — Deployed to Cloudflare Pages
- Live at **https://mifos-products.pages.dev** (project `mifos-products`, production branch `main`).
- Deployed via `wrangler pages deploy` (framework `/idea-site` Cloudflare engine) using vault
  creds `mifos-x-cloudflare-{api-token,account-id}`. Config: `idea-layer/site/SITE_DEPLOY.yaml`.
- Pending human: custom-domain cutover `products.mifos.org`; connect GitHub repo for auto-deploys.


## 2026-08-15 — v1.0 first draft
- Project created via `/project-add` (web-app, mifos-x workspace).
- Source scaffolded at `source/mifos-products/` (Astro static catalog).
- Catalog mirrored from products.mifos.org (Mifos X, Payment Hub EE, Mifos
  Gazelle, Mobile Banking & Wallet Apps + MifosSave/Mobile Wallet/Mifos Mobile).
- Idea-layer docset authored (IDEA, REQUIREMENTS, FEATURES, ARCHITECTURE, ROADMAP).
- Layers scaffolded: idea, plan, server, client, feature, infrastructure, testing, docs.
