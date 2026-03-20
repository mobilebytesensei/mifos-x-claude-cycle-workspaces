# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/server-layer/endpoints/USER.md"
# last_modified: "2026-03-20"

# User Settings Endpoints

> **Category**: User Settings
> **Endpoints**: 1
> **Service**: `UserService`

---

## PUT /user/password

**Purpose**: Update user password

**Service**: `UserService.updatePassword(payload)`

**Request**:
```json
{
    "newPassword": "newSecurePassword123",
    "confirmPassword": "newSecurePassword123"
}
```

**Response**:
```json
{
    "message": "Password updated successfully"
}
```

**DTO**: `UpdatePasswordPayload`
```kotlin
@Serializable
data class UpdatePasswordPayload(
    val newPassword: String,
    val confirmPassword: String,
)
```

---

## Notes

- Password must meet complexity requirements (server-configured)
- User must be authenticated to change password
- Old password may be required depending on server configuration

---

## Related

- Design Layer: [settings/API.md](../../design-spec-layer/features/settings/API.md)
- Patterns: [CLIENT_PATTERNS.md](../CLIENT_PATTERNS.md)
