# Demo Data

> Project-wide demo data registry. Each DTO type has its own YAML file.
> Convention: `demo-data/{dto_name}.yaml` — referenced from screen `api.yaml` via `demo_source: {dto_name}`.

## Status: Empty-slate scaffold (2026-05-22)

No DTOs declared yet because product feature scope is undefined. Once `/idea add` declares features and `/idea generate-dtos` extracts DTOs from `screens/*/api.yaml`, the corresponding demo-data YAMLs land here.

For the current scaffolding (home/profile/settings), no project-specific DTOs exist beyond `UserPreferences` which is internal to `core/datastore` and doesn't need demo data.

## Future structure (example)

```
demo-data/
  README.md             ← this file
  Account.yaml          ← demo Account DTOs
  Transaction.yaml      ← demo Transaction DTOs
  ...
```
