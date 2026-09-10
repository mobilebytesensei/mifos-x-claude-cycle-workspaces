# mifos-products (`mifos-x/mifos-products`)

The **Mifos Products showcase site** — a static Astro catalog of the Mifos
open-source DPGs. Migration of [`products.mifos.org`](https://products.mifos.org)
onto Astro + Cloudflare Pages.

| | |
|---|---|
| **Workspace** | `mifos-x` |
| **Type** | `web-app` (Astro SSG, TypeScript) |
| **Source** | [`source/mifos-products/`](source/mifos-products/) |
| **Deploys to** | Cloudflare Pages `mifos-products` → `mifos-products.pages.dev` → `products.mifos.org` |
| **Status** | active — first draft, device-free verified |

## Canonical layout (`/project-add`)

```
mifos-products/
├── PROJECT.md, PROJECT_CONFIG.yaml     # project metadata + layer config
├── source/mifos-products/              # the Astro site (build here)
├── idea-layer/                         # SoT: IDEA, REQUIREMENTS, FEATURES, ARCHITECTURE, ROADMAP
├── plan-layer/ · server-layer/ · client-layer/ · feature-layer/
├── infrastructure-layer/ · testing-layer/ · docs-layer/
```
(platform-layer is KMP-only → disabled for web.)

## Build the site

```bash
cd source/mifos-products
npm install
npm run dev        # http://localhost:4321
npm run build      # → dist/ (static)
```

## Edit the catalog

Everything renders from `source/mifos-products/content/site.yaml` (products, hero,
nav, footer) + `tokens.css` (brand palette). See that file and the source README.

## Deploy (pending human)

Create the GitHub repo, link Cloudflare Pages project `mifos-products` (build
`npm run build`, output `dist`, base dir `source/mifos-products`), then cut over
`products.mifos.org`.
