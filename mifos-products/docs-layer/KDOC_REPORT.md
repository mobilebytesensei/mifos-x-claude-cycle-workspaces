---
_blueprint:
  version: "1.0.0"
  date: "2026-05-15"
  layer: "docs-layer"
  applies_to: "kmp-library"
---

# KDoc Report — mifos-products

> Latest Dokka coverage report snapshot. Update before each release.
> Generate with: `./gradlew :{{artifact_id}}:dokkaHtml`
> Detailed symbol list: `api-layer/KDOC_COVERAGE.md`

---

## Summary

| Run Date | Overall Coverage | Gate (≥90%) | Dokka Output |
|:--------:|:---------------:|:-----------:|--------------|
| *Not yet run* | — | ❌ | `{{artifact_id}}/build/dokka/html/` |

---

## Per-Package Breakdown

| Package | Coverage | Status |
|---------|:--------:|:------:|
| *Not yet measured* | — | ❌ |

---

## Generate

```bash
./gradlew :{{artifact_id}}:dokkaHtml
open {{artifact_id}}/build/dokka/html/index.html
```

---

## CI Integration (add to release pipeline)

```yaml
- name: Generate KDoc
  run: ./gradlew :{{artifact_id}}:dokkaHtml
```
