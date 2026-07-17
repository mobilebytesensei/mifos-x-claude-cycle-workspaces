# share-out-preview — error state

| Field | Value |
|-------|-------|
| Feature | share-out-preview |
| State | error |
| Screen ID | b6ceb223de4243049b8c536e0723c5f5 |
| Project ID | 10006374793896725042 |
| Design System ID | 17261554270924114992 |
| Generated At | 2026-07-17T06:19:40.754Z |
| HTML Downloaded | Yes |
| PNG Downloaded | Yes |
| Figma Export | — |
| Stitch Screen | [View](https://stitch.google.com/projects/10006374793896725042/screens/b6ceb223de4243049b8c536e0723c5f5) |
| Attempts | 1 |

## Files

- `code.html` — Stitch-generated HTML mockup
- `screen.png` — Screenshot of the generated screen

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-group-banking --features share-out-preview --force
```