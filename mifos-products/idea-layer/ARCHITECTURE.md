# Architecture — Mifos Products

## Shape

A **static Astro (SSG)** site. No server runtime; all HTML is generated at build
and served from Cloudflare Pages CDN.

```
source/mifos-products/
├── content/
│   ├── site.yaml      # single source of truth for the catalog (brand, hero, products, nav, footer)
│   └── tokens.css     # Mifos brand palette (theme-aware light/dark) — the ONLY color source
├── src/
│   ├── lib/content.js         # the ONLY content seam (loads site.yaml)
│   ├── layouts/Base.astro     # shell: token inject + theme toggle + Nav/Footer
│   ├── components/            # Nav · Hero · ProductGrid · ProductCard · Community · Footer
│   └── pages/index.astro
└── public/                    # favicon + static assets
```

## Key decisions

| Decision | Rationale |
|----------|-----------|
| Astro static output | Fast, zero-runtime, cheap to host on CF Pages; matches web-template & saveit-web. |
| Content in one `site.yaml` | Catalog edits are one-file PRs; shell stays brand-free (white-label seam). |
| Colors only in `tokens.css` | Rebrand = swap one file, no `src/**` change. Theme-aware via `data-theme`. |
| No backend | Pure catalog; product deep-links point at canonical Mifos properties. |

## Layer mapping (this project)

| Layer | Role here |
|-------|-----------|
| idea | This docset — SoT for what the site should show. |
| feature | Site sections (catalog landing, theme, SEO). |
| infrastructure | Astro build + Cloudflare Pages deploy config. |
| server / client | Thin/placeholder — no backend or network services yet. |
| testing | Build + render checks (Playwright light/dark). |
| docs | Contributor + deploy docs. |
| platform | N/A (KMP-only). |

## Data flow

`content/site.yaml` → `src/lib/content.js` (`loadSite()`) → components → static HTML in `dist/`.
