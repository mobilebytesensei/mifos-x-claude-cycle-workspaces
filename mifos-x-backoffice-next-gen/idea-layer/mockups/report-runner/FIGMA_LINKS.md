# FIGMA_LINKS.md — report-runner

<!-- schema: v3.2 | generated: 2026-08-03T17:10:33.197Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T17:10:33.121Z |
| Success | 6/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | f46dc356f9c34827b09fda0816e8785b | 01-report-runner-loading | PNG ✅ | HTML ✅ | ♻ resumed |
| content | 740e1730dcb94c40b3b2aee748d8083c | 02-report-runner-content | PNG ✅ | HTML ✅ | ♻ resumed |
| running | 5705f61750d8499280bd759a6b49c4f1 | 03-report-runner-running | PNG ✅ | HTML ✅ | ✅ generated |
| results | — | 04-report-runner-results | PNG ❌ | HTML ✅ | ⏳ pending |
| empty | 00b7fca70b1b474483f86e3b49259da8 | 05-report-runner-empty | PNG ✅ | HTML ✅ | ♻ resumed |
| error | 9ef2386c91c946379c5bb82499969641 | 06-report-runner-error | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/f46dc356f9c34827b09fda0816e8785b) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/740e1730dcb94c40b3b2aee748d8083c) | — |
| running | [Open](https://stitch.google.com/projects/10243803383444073820/screens/5705f61750d8499280bd759a6b49c4f1) | — |
| results | — | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/00b7fca70b1b474483f86e3b49259da8) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/9ef2386c91c946379c5bb82499969641) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features report-runner --force
```