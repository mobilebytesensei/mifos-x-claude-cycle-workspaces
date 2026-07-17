# FIGMA_LINKS.md — member-invite

<!-- schema: v3.2 | generated: 2026-07-17T05:48:01.885Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [3717008183183231397](https://stitch.google.com/projects/3717008183183231397) |
| Design System ID | 17261554270924114992 |
| Generated | 2026-07-17T05:48:01.881Z |
| Success | 5/5 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 031cddc107c94511a1ba2da4ddaeed9c | 01-member-invite-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 2d0c3ca499f84dfa8233371dd00409e4 | 02-member-invite-content | PNG ✅ | HTML ✅ | ✅ generated |
| generating | — | 03-member-invite-generating | PNG ❌ | HTML ✅ | ⏳ pending |
| generated | e13308139f384bd2bb49adb97b3e60b8 | 04-member-invite-generated | PNG ✅ | HTML ✅ | ✅ generated |
| error | 6c9058f2a3814914ae48dd75bab3d4ee | 05-member-invite-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/3717008183183231397/screens/031cddc107c94511a1ba2da4ddaeed9c) | — |
| content | [Open](https://stitch.google.com/projects/3717008183183231397/screens/2d0c3ca499f84dfa8233371dd00409e4) | — |
| generating | — | — |
| generated | [Open](https://stitch.google.com/projects/3717008183183231397/screens/e13308139f384bd2bb49adb97b3e60b8) | — |
| error | [Open](https://stitch.google.com/projects/3717008183183231397/screens/6c9058f2a3814914ae48dd75bab3d4ee) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-group-banking --features member-invite --force
```