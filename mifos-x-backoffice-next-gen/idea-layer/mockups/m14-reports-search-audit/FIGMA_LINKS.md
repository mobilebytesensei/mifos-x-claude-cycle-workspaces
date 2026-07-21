# FIGMA_LINKS.md — m14-reports-search-audit

<!-- schema: v3.2 | generated: 2026-07-21T18:45:37.689Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-07-21T18:45:37.688Z |
| Success | 6/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | — | 01-m14-reports-search-audit-loading | PNG ❌ | HTML ✅ | ⏳ pending |
| content | 6e833e66d67045e388e6a59ea2a09cd1 | 02-m14-reports-search-audit-content | PNG ✅ | HTML ✅ | ♻ resumed |
| running | cd6539de5c4346c19e597493228a6621 | 03-m14-reports-search-audit-running | PNG ✅ | HTML ✅ | ♻ resumed |
| result | 6f4b9bc17a174b8b9c2e76584e7a8232 | 04-m14-reports-search-audit-result | PNG ✅ | HTML ✅ | ♻ resumed |
| empty | — | 05-m14-reports-search-audit-empty | PNG ❌ | HTML ✅ | ⏳ pending |
| error | 991f979831af425083fb0a51c1473210 | 06-m14-reports-search-audit-error | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | — | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/6e833e66d67045e388e6a59ea2a09cd1) | — |
| running | [Open](https://stitch.google.com/projects/10243803383444073820/screens/cd6539de5c4346c19e597493228a6621) | — |
| result | [Open](https://stitch.google.com/projects/10243803383444073820/screens/6f4b9bc17a174b8b9c2e76584e7a8232) | — |
| empty | — | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/991f979831af425083fb0a51c1473210) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features m14-reports-search-audit --force
```