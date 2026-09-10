# Mifos Products (`mifos-x/mifos-products`)

The **Mifos Products showcase site** — a standalone Astro static site that
catalogs the Mifos open-source Digital Public Goods (DPGs) for last-mile
financial inclusion. It is the migration of [`products.mifos.org`](https://products.mifos.org)
(currently WordPress) onto Astro + Cloudflare Pages.

| | |
|---|---|
| **Workspace** | `mifos-x` |
| **Type** | `web-app` (Astro SSG, TypeScript) |
| **Deploys to** | Cloudflare Pages project `mifos-products` → `mifos-products.pages.dev` → `products.mifos.org` |
| **Starting point** | mirror of `products.mifos.org` |
| **Style reference** | `mifossave.pages.dev` (built earlier — one of the products) |
| **Status** | active — first draft scaffolded, device-free build pending |

## What it is

A product catalog / showcase, content-driven from a single `content/site.yaml`:

- `/` — hero ("DPGs for Last-Mile Financial Inclusion") + a grid of product cards,
  each with name, category, description, and a "Learn More" link to the product's
  own site/docs; plus a community CTA (GitHub, Slack).
- Theme-aware (light/dark), responsive, zero-JS beyond the theme toggle.

## The catalog (mirrored from products.mifos.org)

| Product | Category | Links to |
|---|---|---|
| Mifos X | Core Banking Platform | mifos.org |
| Payment Hub EE | Payment Orchestration Engine | payments.mifos.org |
| Mifos Gazelle | DPI as a Packaged Solution | mifos.gazelle |
| Mobile Banking & Wallet Apps | Customer-facing apps (incl. MifosSave) | mobile.mifos.org |

## White-label contract

`src/**` contains no brand, copy, colors, or product data. Everything is read at
build from `content/`:

| File | Provides |
|---|---|
| `content/site.yaml` | brand, hero, product catalog, nav, footer, community CTA |
| `content/tokens.css` | Mifos brand palette + fonts (theme-aware) |

This mirrors the `mifos-x/web-template` convention (the single-product landing
shell); this project is its **multi-product catalog** sibling.

## Local dev

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # → dist/ (static)
```

## Deploy (pending human)

- Create GitHub repo + link to Cloudflare Pages project `mifos-products`.
- `npm run build` → `dist/`; CF Pages build command `npm run build`, output `dist`.
- Custom-domain cutover `products.mifos.org` when ready.
