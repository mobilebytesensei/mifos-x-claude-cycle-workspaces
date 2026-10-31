# ADR 0001 — Astro static site for the Mifos Products catalog

- **Status**: Accepted
- **Date**: 2026-08-15

## Context

`products.mifos.org` runs on WordPress. We want a fast, community-maintainable,
openMF-owned replacement that mirrors the existing product catalog.

## Decision

Build a **static Astro (SSG)** site, content-driven from a single
`content/site.yaml` (+ theme-aware `tokens.css`), deployed to **Cloudflare Pages**.
This mirrors the conventions of `mifos-x/web-template` and `mbs/saveit-web`.

## Consequences

- **+** Catalog edits are one-file PRs; no CMS to maintain; fast + cheap hosting.
- **+** White-label shell reusable; rebrand = swap `tokens.css`.
- **−** No dynamic/server features (acceptable — pure catalog).
- **−** External product URLs must be maintained by hand (community-owned).
