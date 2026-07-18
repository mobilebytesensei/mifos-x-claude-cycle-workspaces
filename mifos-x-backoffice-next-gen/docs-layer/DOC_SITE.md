---
_blueprint:
  version: "1.0.0"
  date: "2026-05-15"
  layer: "docs-layer"
  applies_to: "kmp-library"
---

# Doc Site — mifos-x-backoffice-next-gen

> Documentation website configuration and deployment status.

---

## Overview

| Attribute | Value |
|-----------|-------|
| Framework | Docusaurus / GitHub Pages |
| Source | `source/mifos-x-backoffice-next-gen/docusaurus/` |
| Deployed URL | ❌ Not yet deployed |
| Deploy trigger | Release tag (`v*`) |

---

## Content Inventory

| Document | Path | Status |
|----------|------|:------:|
| Quick-start guide | `docs/quick-start.md` | ❌ Not written |
| API reference (Dokka) | Auto-generated | ❌ Not deployed |
| Migration guides | `docs/migration/` | ❌ Not needed yet |

---

## GitHub Pages Deployment (CI template)

```yaml
# .github/workflows/docs.yml
name: Deploy Docs
on:
  push:
    tags: ['v*']
jobs:
  deploy-docusaurus:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd docusaurus && npm install && npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docusaurus/build
  deploy-dokka:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew :{{artifact_id}}:dokkaHtml
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: {{artifact_id}}/build/dokka/html
          destination_dir: api
```

---

## Local Development

```bash
cd source/mifos-x-backoffice-next-gen/docusaurus
npm install && npm start
# Opens http://localhost:3000
```
