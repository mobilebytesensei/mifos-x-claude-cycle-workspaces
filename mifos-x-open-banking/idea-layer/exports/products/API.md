# API — Products

Client contracts for `products`. This project owns no backend: these are Ktorfit contracts against
the OBP sandbox, not owned schema.
Consumers: `ProductsRepository`, `AccountsRepository`.

---

## obp_get_my_accounts

| | |
|---|---|
| Endpoint | `GET /obp/v3.0.0/my/accounts` |
| Tag | Account |
| Trigger | On load — `AccountsRepository.myAccounts` |

The user's accounts. **The distinct `bank_id` values determine which bank catalogues are offered** in
the selector — this screen does not list every ASPSP, only the banks the customer actually holds
accounts with.

| Field      | Type            |
|------------|-----------------|
| `accounts` | `List<Account>` |
| `bank_id`  | `String`        |

Errors: `401 USER_NOT_LOGGED_IN`.

---

## obp_products

| | |
|---|---|
| Endpoint | `GET /obp/v3.0.0/banks/{bankId}/products` |
| Tag | Product |
| Trigger | On load per bank held, and on `onRetry` — `ProductsRepository.listProducts(bankId)` |

**Fetched per bank, in parallel, once per session.** Per-bank fetching is why a single bank's
failure degrades to the inline `products_bank_load_failed` row rather than emptying the screen — the
other banks' catalogues are unaffected.

| Field         | Type            |
|---------------|-----------------|
| `products`    | `List<Product>` |
| `code`        | `String`        |
| `name`        | `String`        |
| `description` | `String`        |
| `category`    | `String`        |
| `family`      | `String`        |

---

## Both enums are derived client-side

Neither `ProductScope` nor `ProductCategory` comes from the API as a usable value.

**`ProductScope`** — `PERSONAL` / `BUSINESS`. Derived from `code`/`name` keywords via
`BUSINESS_MARKERS` / `scopeOf`. The audience tabs filter on this derived value, not on a server field.

**`ProductCategory`** — `EVERYDAY` / `SAVINGS` / `CARDS` / `LOANS`. Derived via `categoryOf`
**because `category` is null on the sandbox**. The response carries the field; it just has no value,
so the badge is computed from code and name instead.

Note there is **no MORTGAGES bucket** — no mortgage product exists in the catalogue, and `LOANS`
covers what does. Adding a mortgage category would create an always-empty filter.

Both derivations are heuristics over text. They are recorded here so that a future implementer does
not "fix" the badge by binding it to `category` and get nulls, or add a scope field the API never
returns.

---

## search_products — DEFERRED

Declared with `deferred: true`. Product search was never wired on this screen and the top-bar search
action was removed. **No endpoint is called.** It is kept in `api.yaml` so the intent survives, not
because there is anything to call.

---

## Outbound

The only outbound affordance is `more_info_url`, opened in the platform browser via
`compose.ui.platform.LocalUriHandler`. There is no in-app apply or details journey, and
`flow.yaml#navigates_to` is `[]` accordingly — full terms live on the bank's own site.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/products/api.yaml. -->
