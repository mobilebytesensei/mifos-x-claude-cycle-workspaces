# FIGMA_LINKS.md — collection-sheet

<!-- schema: v3.2 | generated: 2026-07-26T05:36:36.750Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-07-26T05:36:36.667Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 6a0318c4c6934edf8f3598bc9250db8e | 01-collection-sheet-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 6ea13450f5c0459ba1122ac61f3b8522 | 02-collection-sheet-content | PNG ✅ | HTML ✅ | ✅ generated |
| empty | 071ad72882a24de3840c1fea79e45efc | 03-collection-sheet-empty | PNG ✅ | HTML ✅ | ✅ generated |
| error | 02491653c962483bab2e4f887dd5deda | 04-collection-sheet-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/6a0318c4c6934edf8f3598bc9250db8e) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/6ea13450f5c0459ba1122ac61f3b8522) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/071ad72882a24de3840c1fea79e45efc) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/02491653c962483bab2e4f887dd5deda) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features collection-sheet --force
```