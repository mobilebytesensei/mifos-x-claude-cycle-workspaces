# FIGMA_LINKS.md — search-record

<!-- schema: v3.2 | generated: 2026-08-03T17:19:58.239Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T17:19:58.110Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | ebd40ec93d8c4697b935e3a4ed7d414c | 01-search-record-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | c60ab642d3ea418b823ecb2049d19c96 | 02-search-record-content | PNG ✅ | HTML ✅ | ✅ generated |
| empty | 08440fd5d76f4a169e59c360f094a205 | 03-search-record-empty | PNG ✅ | HTML ✅ | ✅ generated |
| error | 904b2165b33e4f58a7e129102e663c3b | 04-search-record-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/ebd40ec93d8c4697b935e3a4ed7d414c) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/c60ab642d3ea418b823ecb2049d19c96) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/43bf435b6bdc430e8347189348341e88) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/904b2165b33e4f58a7e129102e663c3b) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features search-record --force
```