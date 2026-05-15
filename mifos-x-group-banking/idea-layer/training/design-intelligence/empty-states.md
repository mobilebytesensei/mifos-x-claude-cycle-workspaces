# Empty States — mifos-x-group-banking

## Pattern: Actionable Empty States

All empty states include a primary CTA. Never show a bare "No data" message.

| Screen | Empty Condition | Message | CTA |
|--------|----------------|---------|-----|
| group-list | No groups assigned | "No groups assigned to you yet." | Contact admin |
| member-list | Group has no members | "No members in this group yet." | + Add Member |
| loan-list | No active loans | "No loans recorded for this group." | + Apply for Loan |
| meeting-calendar | No meetings scheduled | "No upcoming meetings." | + Schedule Meeting |
| sync-status | Queue empty | "All data is synced. ✓" | (none — success state) |
| personal-loans | No loan history | "You have no active or past loans." | Request a Loan |
| personal-savings | No transactions | "No savings transactions yet." | (informational) |

## Offline Empty State

When data is unavailable due to offline + no cache:
- Icon: cloud_off
- Message: "No cached data available. Connect to internet to load."
- CTA: Retry (visible when connectivity restored)
