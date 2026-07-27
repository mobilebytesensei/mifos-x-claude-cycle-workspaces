# FIGMA_LINKS.md — m01-dashboard

<!-- schema: v3.2 | generated: 2026-07-26T09:55:07.141Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-07-26T09:55:07.072Z |
| Success | 6/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 108f861e3e644f548d5b427f4da7ac34 | 01-m01-dashboard-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 467d586536224770a155a0df77c40d9e | 02-m01-dashboard-content | PNG ✅ | HTML ✅ | ✅ generated |
| empty | 4b18779973c14c74a51e5ec1f1f8e588 | 03-m01-dashboard-empty | PNG ✅ | HTML ✅ | ✅ generated |
| partial-tile-error | 4653848ff1e545d9b78a59ec117cf3a3 | 04-m01-dashboard-partial-tile-error | PNG ✅ | HTML ✅ | ✅ generated |
| no-network | 11b5c0f351c74cd4aeb9fe93c6edd2a9 | 05-m01-dashboard-no-network | PNG ✅ | HTML ✅ | ✅ generated |
| error | 0c02ddaf2fe642bf838c9a82e61cd032 | 06-m01-dashboard-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/108f861e3e644f548d5b427f4da7ac34) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/467d586536224770a155a0df77c40d9e) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/4b18779973c14c74a51e5ec1f1f8e588) | — |
| partial-tile-error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/4653848ff1e545d9b78a59ec117cf3a3) | — |
| no-network | [Open](https://stitch.google.com/projects/10243803383444073820/screens/11b5c0f351c74cd4aeb9fe93c6edd2a9) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/04dde2688108412bad4c00dda7afd019) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features m01-dashboard --force
```