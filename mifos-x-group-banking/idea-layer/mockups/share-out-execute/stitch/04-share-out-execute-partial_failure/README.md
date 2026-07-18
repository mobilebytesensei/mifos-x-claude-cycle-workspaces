# share-out-execute — partial_failure state

| Field | Value |
|-------|-------|
| Feature | share-out-execute |
| State | partial_failure |
| Screen ID | 13a940292b104400845999478bf28757 |
| Project ID | 10006374793896725042 |
| Design System ID | 17261554270924114992 |
| Generated At | 2026-07-17T06:01:15.020Z |
| HTML Downloaded | Yes |
| PNG Downloaded | Yes |
| Figma Export | — |
| Stitch Screen | [View](https://stitch.google.com/projects/10006374793896725042/screens/13a940292b104400845999478bf28757) |
| Attempts | 1 |

## Files

- `code.html` — Stitch-generated HTML mockup
- `screen.png` — Screenshot of the generated screen

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-group-banking --features share-out-execute --force
```