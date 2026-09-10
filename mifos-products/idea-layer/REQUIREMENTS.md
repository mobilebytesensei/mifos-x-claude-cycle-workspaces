# Requirements — Mifos Products

> First draft. Enrich with `/idea-plan`.

## Functional

| ID | Requirement | Status |
|----|-------------|:------:|
| FR-1 | Display a hero with the DPG tagline and a primary CTA to the catalog. | ✅ |
| FR-2 | Render every product from `site.yaml#products[]` as a card (name, category, description, tags, deep-link). | ✅ |
| FR-3 | Surface sub-products (e.g. MifosSave, Mobile Wallet, Mifos Mobile) as chips on the relevant card. | ✅ |
| FR-4 | Provide a community CTA (GitHub, Slack, mifos.org) and a footer with grouped links. | ✅ |
| FR-5 | Support light/dark theme with persistence and no flash-of-wrong-theme. | ✅ |
| FR-6 | Emit sitemap + OG/canonical meta for SEO. | ✅ |

## Non-functional

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Static output; no server runtime. | Astro `output: static` |
| NFR-2 | Performance | Lighthouse ≥ 95 |
| NFR-3 | Accessibility | Focus-visible, reduced-motion, semantic landmarks |
| NFR-4 | Rebrandable | Colors only in `tokens.css`; copy only in `site.yaml` |
| NFR-5 | Deploy | `npm run build` → `dist/` on Cloudflare Pages |
