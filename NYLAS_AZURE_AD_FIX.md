# Nylas Azure AD Grant Error - Fix Guide

## Problem
You're getting error `AADSTS700016` when trying to add a grant in Nylas with Azure AD (Microsoft 365).

**Error:** Application with identifier '~oS8Q~XA5R...c20' was not found in the directory.

## Root Cause
The identifier shown in the error (`~oS8Q~XA5R...c20`) is a **client secret**, not a **client ID**.

Azure AD requires:
- **Client ID (Application ID):** UUID format (e.g., `12345678-1234-1234-1234-123456789abc`)
- **Client Secret:** The secret value (e.g., `~xxxxxx...xxx` - starts with special characters)

## Solution

### Step 1: Get the Correct Client ID from Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure Active Directory** → **App registrations**
3. Find your Nylas application
4. Copy the **Application (client) ID** - this is a UUID format
   - Example: `a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6`
   - NOT the client secret that starts with `~`

### Step 2: Update Nylas Configuration

In your Nylas connector configuration:

```json
{
  "client_id": "YOUR-APPLICATION-CLIENT-ID-UUID-HERE",
  "client_secret": "YOUR-CLIENT-SECRET-VALUE-HERE",
  "tenant": "common"  // or your specific tenant ID
}
```

**Important:**
- `client_id` = Application (client) ID from Azure (UUID format)
- `client_secret` = The secret value you generated

### Step 3: Verify Azure AD App Registration

Ensure your Azure AD app has:

1. **Correct Redirect URI** configured:
   - Add: `https://api.nylas.com/v3/connect/callback`
   - Add: `https://api.us.nylas.com/v3/connect/callback` (if using US region)

2. **API Permissions** granted:
   - Microsoft Graph → Delegated permissions:
     - `Mail.ReadWrite`
     - `Mail.Send`
     - `Calendars.ReadWrite`
     - `Contacts.ReadWrite`
     - `offline_access`
     - `User.Read`

3. **Admin consent** granted (if required by your tenant)

### Step 4: Check Tenant Configuration

The error mentions 'Fincas Martin Sanz S.L' tenant. Verify:

1. You're using the correct tenant ID or use `common` for multi-tenant
2. The app is registered in the correct directory
3. If it's a single-tenant app, use the specific tenant ID instead of `common`

### Tenant URL Options:
```
common        - Multi-tenant and personal Microsoft accounts
organizations - Multi-tenant only (work/school accounts)
consumers     - Personal Microsoft accounts only
{tenant-id}   - Specific tenant only
```

## Quick Checklist

- [ ] Using **Client ID** (UUID format) not client secret for the `client_id` field
- [ ] Client secret is correct in the `client_secret` field
- [ ] Redirect URIs include Nylas callback URL
- [ ] API permissions are configured and consented
- [ ] Using correct tenant value (`common` or specific tenant ID)
- [ ] App is published/installed in the target tenant

## Common Mistakes

1. ❌ Mixing up Client ID and Client Secret
2. ❌ Using the wrong tenant ID
3. ❌ Missing redirect URI configuration
4. ❌ Application not granted admin consent when required
5. ❌ Using single-tenant app with `common` endpoint

## Testing

After fixing the configuration:
1. Clear any cached credentials
2. Try the Nylas grant flow again
3. Check Azure AD sign-in logs if it still fails

## Additional Resources

- [Nylas Microsoft OAuth Setup](https://developer.nylas.com/docs/v3/auth/microsoft/)
- [Azure AD Error Codes](https://learn.microsoft.com/en-us/entra/identity-platform/reference-error-codes)
