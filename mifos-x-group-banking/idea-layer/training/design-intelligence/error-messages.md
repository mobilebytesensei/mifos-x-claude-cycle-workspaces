# Error Messages — mifos-x-group-banking

## Error Display Patterns

| Error Type | Display Pattern | Dismissible |
|-----------|----------------|-------------|
| Network offline | Persistent banner (top) | No — auto-dismisses on reconnect |
| Auth expired (401) | Full-screen dialog → login | No |
| Server error (500/503) | Snackbar + Retry | Yes |
| Validation error | Inline field error | N/A |
| Destructive action warning | Confirmation dialog | Yes (Cancel) |
| Sync conflict | Conflict chip in sync-status | Manual |

## Message Tone

Friendly, non-technical. Avoid "Error 401" — translate to plain language.
Target audience: rural Kenya, primary language may be Swahili.

| Code | User-Facing Message (English) |
|------|------------------------------|
| 401 | "Your session has expired. Please log in again." |
| 403 | "You don't have permission to do that." |
| 404 | "That record could not be found." |
| 503 | "The server is not responding. Working from cached data." |
| offline | "No internet connection. You can still work offline." |
| loan.ceiling_exceeded | "This loan exceeds your group's approved ceiling of KES {amount}." |
| meeting.already_recorded | "This meeting has already been recorded for this date." |
| savings.insufficient | "Insufficient balance for this withdrawal." |
| sync.conflict | "Data conflict during sync. Tap to review." |
