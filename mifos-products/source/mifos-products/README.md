# mifos-products — Mifos Products showcase site

Astro static site cataloging the Mifos open-source DPGs — the migration of
[`products.mifos.org`](https://products.mifos.org) onto Astro + Cloudflare Pages.
Content-driven: everything renders from `content/site.yaml` + `content/tokens.css`;
`src/**` is a generic shell.

## Structure

```
content/
  site.yaml     # brand, hero, product catalog, nav, community, footer
  tokens.css    # Mifos brand palette (theme-aware light/dark)
src/
  lib/content.js        # the ONLY content seam (loads site.yaml)
  layouts/Base.astro    # shell: tokens inject, theme toggle, Nav + Footer
  components/           # Nav, Hero, ProductGrid, ProductCard, Community, Footer
  pages/index.astro     # Hero → ProductGrid → Community
public/favicon.svg
```

## Local dev

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # → dist/ (static)
npm run preview    # serve the built site
```

## Edit the catalog

Add/reorder products in `content/site.yaml#products[]`. Each product:

```yaml
- name: Product Name
  category: Category
  icon: "🏦"                 # emoji or leave for default
  accent: brand              # brand | teal | amber | violet
  description: One-paragraph blurb.
  link: { label: "Learn More", href: "https://…", external: true }
  tags: [Tag A, Tag B]
  subproducts:               # optional chips
    - { name: "Sub", href: "https://…" }
```

Rebrand by swapping `content/tokens.css` — no `src/**` changes.

## Deploy (Cloudflare Pages)

- Build command: `npm run build` · Output dir: `dist`
- Set `SITE_URL` at build to the deployed origin (canonical/OG/sitemap).
- **Pending human**: create the GitHub repo, link it to CF Pages project
  `mifos-products` (`mifos-products.pages.dev`), then cut over `products.mifos.org`.
