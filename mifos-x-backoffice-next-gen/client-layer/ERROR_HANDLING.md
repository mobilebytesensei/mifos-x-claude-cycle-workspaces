# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/client-layer/ERROR_HANDLING.md"
# last_modified: "2026-03-19"

# Error Handling - mifos-x-backoffice-next-gen

> Error handling patterns for the client layer.

---

## Error Pipeline

```
HTTP Response
    ↓ ResultSuspendConverterFactory (REST) or try-catch (Supabase)
NetworkError enum (BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, REQUEST_TIMEOUT, TOO_MANY_REQUESTS, SERVER, SERIALIZATION, UNKNOWN)
    ↓ NetworkError.toThrowable()
RemoteException(networkError, userMessage)
    ↓ Repository toDataState()
DataState.Error(throwable) or DataState.NoNetwork()
```

---

## Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `NetworkResult<D, E>` | `core-base/network/` | Sealed interface: Success or Error |
| `NetworkError` | `core-base/network/` | Enum of HTTP error categories |
| `RemoteException` | `core/data/util/` | Wraps NetworkError with user message |
| `ResultExtensions` | `core/data/util/` | `toDataState()` bridge functions |

---

## Reference

For detailed error handling, see: `templates/instructions/client-layer/ERROR_HANDLING.md`
