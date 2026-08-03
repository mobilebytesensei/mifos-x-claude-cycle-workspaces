# FIGMA_LINKS.md — product-editor

<!-- schema: v3.2 | generated: 2026-08-03T17:07:46.641Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T17:07:46.483Z |
| Success | 6/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 437ecf664dcc4694821b29ff5dd53980 | 01-product-editor-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 9279ec394128488fb00471a7d163ae21 | 02-product-editor-content | PNG ✅ | HTML ✅ | ♻ resumed |
| validating | eb024f455bf54d6cab8b1b5592338de5 | 03-product-editor-validating | PNG ✅ | HTML ✅ | ✅ generated |
| saving | 993f918b7a644856a577bad862c175a9 | 04-product-editor-saving | PNG ❌ | HTML ✅ | ✅ generated |
| empty | 3cd44eb918c2432492d4e6354642dd1d | 05-product-editor-empty | PNG ✅ | HTML ✅ | ✅ generated |
| error | 6bc9d523b22b41cb99c014ced26d8450 | 06-product-editor-error | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/437ecf664dcc4694821b29ff5dd53980) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/9279ec394128488fb00471a7d163ae21) | — |
| validating | [Open](https://stitch.google.com/projects/10243803383444073820/screens/eb024f455bf54d6cab8b1b5592338de5) | — |
| saving | [Open](https://stitch.google.com/projects/10243803383444073820/screens/993f918b7a644856a577bad862c175a9) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/73a8a4965215433097defc6c5952182c) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/6bc9d523b22b41cb99c014ced26d8450) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features product-editor --force
```