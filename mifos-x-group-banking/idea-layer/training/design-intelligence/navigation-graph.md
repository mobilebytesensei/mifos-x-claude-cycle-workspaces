# Navigation Graph — mifos-x-group-banking

## Entry Points

- App cold start → `login`
- `login` → (Admin) → `client-type-selector` → `admin-dashboard`
- `login` → (End User) → `personal-dashboard`

## Admin Navigation Tree

```
client-type-selector
  └── admin-dashboard (bottom nav root)
       ├── group-list → group-create → group-dashboard
       ├── group-dashboard → meeting-calendar → meeting-conduct → meeting-summary
       ├── group-dashboard → member-list → member-add | member-profile → member-savings-detail
       ├── group-dashboard → loan-list → loan-apply | loan-detail → loan-repayment-dialog
       ├── group-dashboard → share-out-preview → share-out-execute
       ├── savings-dashboard (tab within group-dashboard)
       ├── sync-status (via app-bar icon)
       └── settings → settings-logout-dialog → login
```

## End User Navigation Tree

```
personal-dashboard (bottom nav root)
  ├── personal-savings
  ├── personal-loans → loan-request
  └── settings → settings-logout-dialog → login
```

## Field Officer Navigation Tree

```
field-officer-dashboard
  └── group-list (read-only) → group-dashboard (read-only)
```

## Modal / Dialog Overlays

- `loan-mark-defaulted-dialog` — overlays loan-detail
- `loan-repayment-dialog` — overlays loan-detail
- `settings-logout-dialog` — overlays settings
- `previous-meeting-review` — pushed from meeting-calendar
