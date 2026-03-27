# App Flow Connections — kmp-project-template

## Navigation Graph

| From | To | Trigger | Type |
|------|-----|---------|------|
| splash | tasks | Auto (UserUnlocked state) | Auto |
| tasks | editTask | FAB "New Task" / Task card tap | Navigate |
| tasks | settings | Settings icon in header | Navigate |
| tasks | profile | Bottom nav "Profile" tab | Tab |
| profile | tasks | Bottom nav "Tasks" tab | Tab |
| settings | notifications | "Notification Preferences" card | Navigate |
| settings | tasks | Back button | Back |
| notifications | settings | Back button | Back |
| editTask | tasks | Back button / Save action | Back |

## Entry Points

- **Entry**: `splash` (app launch)
- **Main Hub**: `tasks` (bottom nav home)

## Bottom Navigation

| Tab | Screen | Icon |
|-----|--------|------|
| Tasks | tasks | home |
| Profile | profile | person |

## Dialogs (Inline)

| Screen | Dialog | Trigger |
|--------|--------|---------|
| tasks | Year Picker | Year text tap |
| editTask | Date Picker | Due date field tap |
| editTask | Time Picker | Due time field tap |
| settings | Theme Settings | "Change Theme" card |
| settings | Language Preference | "Change Language" card |
| profile | Sign Out Confirmation | "Sign Out" button |
