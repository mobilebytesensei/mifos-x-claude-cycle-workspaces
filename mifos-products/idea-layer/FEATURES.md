# Features — Mifos Products

> The site is a single content-driven landing page. "Features" here model its
> sections; the catalog data itself lives in `source/mifos-products/content/site.yaml`.

| # | Feature | Description | Status |
|:-:|---------|-------------|:------:|
| 1 | Catalog Landing | Hero + product grid + community CTA + footer, all from `site.yaml`. | ✅ implemented |
| 2 | Product Grid | Responsive card grid; per-product accent, category, tags, sub-product chips, deep-link. | ✅ implemented |
| 3 | Light/Dark Theme | Persisted, no-flash theme toggle driven by `tokens.css`. | ✅ implemented |
| 4 | SEO / Sitemap | `@astrojs/sitemap`, OG meta, canonical via `SITE_URL`. | ✅ implemented |
| 5 | Mobile Apps page (`/mobile`) | KMP-centric showcase; mirrors products.mifos.org/mobile. Hero + KMP strip + White-Label Template band + per-app cards. | ✅ implemented |
| 6 | Per-product own-site links | Every mobile app links to its OWN dedicated site (Group Banking → mifossave.pages.dev; others pending). | ✅ implemented |
| 7 | Per-app detail pages (`/mobile/<id>`) | Dedicated detail page per app + the template (overview, highlights, platforms, links, KMP note). Static routes via `getStaticPaths`. | ✅ implemented |
| 7a | MifosSave full page (`/mobile/group-banking`) | Bespoke full product page sourced from the mifos-x-group-banking idea-layer: hero + problem + 5 values + 8 features + meeting lifecycle + 9 group models + roles + KMP tech + demo credentials + CTA. Indigo brand. | ✅ implemented |
| 8 | White-Label Template | `openMF/kmp-project-template` featured as the white-label starting point — band on `/mobile` + `/mobile/kmp-project-template` detail page. | ✅ implemented |
| 9 | i18n catalog | Localized copy. | ⭘ backlog (v1.2) |
| 10 | Real product-level app pages | Each `/mobile/<id>` rebuilt from the app's actual GitHub README (fixed 2 wrong facts: Mifos Mobile is self-service banking not "white-label banking"; "Open Banking App" was wrongly linked to `mobile-wallet` — the real repo is `mifos-x-open-banking-pisp-app`; template is branded "App Toolkit"). Componentized: AppHero/Overview/Problem/FeatureGrid/TechStrip/Downloads/Highlights, alternating-band scroll rhythm. | ✅ implemented |

## Catalog contents (mirrored from products.mifos.org)

| Product | Category | Deep-link |
|---------|----------|-----------|
| Mifos X | Core Banking Platform | mifos.org/mifos-x |
| Payment Hub EE | Payment Orchestration Engine | payments.mifos.org |
| Mifos Gazelle | DPI as a Packaged Solution | mifos.gazelle.mifos.org |
| Mobile Banking & Wallet Apps | Customer-facing Apps · KMP | `/mobile` |

## Mobile apps (`/mobile`, mirrors products.mifos.org/mobile) — KMP-centric

| App | Brand | Category | Platforms | Own site | Source |
|-----|-------|----------|-----------|----------|--------|
| Group Banking | MifosSave | Group / Community Banking | Android · iOS · Web | ✅ mifossave.pages.dev | openMF/mifos-x-group-banking |
| Mifos Pay | — | Consumer & Merchant Wallet | Android · iOS · Desktop · Web | ⭘ pending | openMF/mifos-pay |
| Mifos Mobile | — | Mobile Banking | Android · iOS | ⭘ pending | openMF/mifos-mobile |
| Field Officer App | — | Field Operations | Android · iOS | ⭘ pending | openMF/mifos-x-field-officer-app |
| Open Banking App | — | Open Banking · PISP/3PPI | Android · iOS | ⭘ pending | openMF/mobile-wallet |

> Design intent: every app follows the Group-Banking → MifosSave pattern — each gets its
> OWN dedicated site, linked from its card. All apps are Kotlin Multiplatform + Compose
> Multiplatform (shared UI + logic across Android/iOS/Desktop/Web), wired to the Mifos X core.
