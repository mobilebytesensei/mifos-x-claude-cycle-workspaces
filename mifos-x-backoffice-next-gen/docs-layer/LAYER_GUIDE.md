---
_blueprint:
  version: "1.0.0"
  date: "2026-05-15"
  layer: "docs-layer"
  applies_to: "kmp-library"
---

# Docs Layer Guide — mifos-x-backoffice-next-gen

> Tracks the library's documentation artifacts: KDoc/Dokka site, changelog, migration guides, and docusaurus/GitHub Pages.

---

## Purpose

| Concern | What lives here |
|---------|----------------|
| API docs | Dokka HTML generation status and hosting |
| Changelog | Per-version CHANGELOG.md entries |
| Migration guides | Breaking-version upgrade paths |
| Doc site | Docusaurus / GitHub Pages pipeline status |
| Quick-start | Consumer quick-start guide freshness |

---

## Structure

```
docs-layer/
  LAYER_GUIDE.md
  LAYER_STATUS.md
  CHANGELOG_INDEX.md       ← Index of changelog entries per version
  MIGRATION_GUIDES.md      ← Migration guide registry
  DOC_SITE.md              ← Doc site config + deployment status
  KDOC_REPORT.md           ← Latest Dokka coverage report
```

---

## Changelog Format

Entries live in the library's root `CHANGELOG.md` (source of truth).
`CHANGELOG_INDEX.md` here is the framework-level index pointing to those entries.

---

## Dokka Pipeline

```bash
# Generate KDoc site
./gradlew dokkaHtml

# Output: build/dokka/html/
# Deploy to GitHub Pages via CI on release tag
```

---

## Doc Site (Docusaurus)

| File | Purpose |
|------|---------|
| `docusaurus/` | Source for documentation website |
| `docusaurus/docs/quick-start.md` | Consumer quick-start |
| `docusaurus/docs/concepts/` | Architecture / design concepts |

---

## Commands

| Command | Purpose |
|---------|---------|
| `/lib-publish` | Triggers Dokka generation as part of release prep |
| `/lib-release` | Validates CHANGELOG.md has entry for new version |
