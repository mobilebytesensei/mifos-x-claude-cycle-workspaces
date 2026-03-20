# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/.claude/memory/patterns-used.md"
# last_modified: "2026-03-20"

# Patterns Applied

> Tracks patterns used in this project for consistency.
> Max entries: 20 | Prune if unused > 30 days

---

## Pattern Summary

| Pattern | Category | Uses | First Applied | Last Applied | Source |
|---------|----------|:----:|---------------|--------------|--------|
<!-- Patterns are tracked here automatically -->

---

## Pattern Details

<!-- Detailed pattern entries appear below -->

---

## Schema Reference

```yaml
pattern_entry:
  name: "Pattern name"
  category: "Architecture | Data | UI | Navigation | DI | Testing"
  uses: "Number of times applied"
  first_applied: "YYYY-MM-DD"
  last_applied: "YYYY-MM-DD"
  source: "Framework | Learned | External"

detail_entry:
  title: "### {Pattern Name}"
  code_example: |
    ```kotlin
    // Example code showing the pattern
    ```
  when_to_use: "When to apply this pattern"
  why: "Why this pattern is preferred"
  related_files: "Files where pattern is used"
```

---

## Common Pattern Categories

| Category | Examples |
|----------|----------|
| Architecture | MVI, MVVM, Repository, UseCase |
| Data | DataState wrapper, Flow patterns, DTO mapping |
| UI | Composable patterns, State hoisting, Preview |
| Navigation | Sealed events, Type-safe routes |
| DI | Koin modules, Factory patterns |
| Testing | Fake repositories, Fixtures, Turbine |

---

## Related Files

| File | Purpose |
|------|---------|
| `decisions.md` | Decisions that introduce patterns |
| `RULE-MEMORY-001.md` | Memory persistence rules |
