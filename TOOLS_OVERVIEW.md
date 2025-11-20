# IT Support Agent - Tools Overview

This document describes the three IT support tools available in the demo.

---

## 1. Enable Camera/Microphone Permissions

**Tool Name:** `enable_camera_mic`

**Problem it Solves:**
Video conferencing apps (Zoom, Teams, Slack) can't detect camera or microphone.

**What it Does:**
- Detects if the app is currently running
- Opens macOS System Settings to Privacy & Security
- Navigates to Camera/Microphone permissions
- **Automatically clicks "Quit & Reopen" button** when user enables permissions
- Restarts the app with permissions enabled

**Example User Requests:**
- "My Zoom camera isn't working"
- "Teams can't detect my microphone"
- "I can't get my mic to work in Zoom"

**Technical Details:**
- Uses AppleScript to control System Settings
- Uses `open x-apple.systempreferences:` URL scheme for direct navigation
- Polls for the "Quit & Reopen" dialog and clicks it automatically
- Requires Terminal to have Accessibility permissions for auto-clicking

---

## 2. Clear Chrome Cookies for SSO Loops

**Tool Name:** `clear_chrome_cookies`

**Problem it Solves:**
Users stuck in infinite redirect loops when trying to sign in with corporate SSO (Microsoft, Okta, Google).

**What it Does:**
- Closes Chrome gracefully
- Opens Chrome's Clear Browsing Data settings
- Attempts to automatically clear cookies
- **Falls back to direct SQLite database manipulation** for target domain
- Reopens Chrome ready for fresh login

**Example User Requests:**
- "I'm stuck in a login loop with Microsoft SSO"
- "Can't log into my corporate account, it keeps redirecting"
- "My Okta login is broken"

**Technical Details:**
- Closes Chrome via AppleScript quit command
- Opens `chrome://settings/clearBrowserData`
- Uses SQLite to directly delete cookies from `~/Library/Application Support/Google/Chrome/Default/Cookies`
- Creates automatic backup before modifying cookie database
- Supports any domain (default: `login.microsoftonline.com`)

---

## 3. Reset Outlook Profile

**Tool Name:** `reset_outlook_profile`

**Problem it Solves:**
Outlook stuck on "Loading Profile", won't sync, or has corrupted database.

**What it Does:**
- Closes Outlook
- **Backs up current profile** to Desktop (optional)
- Removes corrupted profile folders
- Clears cache and preferences
- Launches Microsoft Database Utility (if available)
- Reopens Outlook to create fresh profile

**Example User Requests:**
- "Outlook is stuck on Loading Profile"
- "My Outlook won't sync"
- "Outlook keeps crashing on startup"

**Technical Details:**
- Removes `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles`
- Clears `~/Library/Caches/com.microsoft.Outlook`
- Resets `~/Library/Preferences/com.microsoft.Outlook.plist`
- Launches Microsoft Database Utility for database rebuild
- Creates timestamped backup folder on Desktop

---

## Demo Flow Examples

### Example 1: Camera Issue
```
User: "Hey, my Zoom camera isn't working, can you help?"

Agent: "I'll help you enable camera permissions for Zoom. Let me open the settings for you."

[Tool executes: enable_camera_mic]
[System Settings opens to Camera permissions]

Agent: "I've opened the Camera permissions. Please check the box next to 'zoom.us'. Once you do, I'll automatically click 'Quit & Reopen' for you."

[User checks the box]
[Dialog appears: "zoom.us will not have access..."]
[Script automatically clicks "Quit & Reopen"]
[Zoom restarts]

Agent: "Done! Your camera should now work in Zoom."
```

### Example 2: SSO Loop
```
User: "I keep getting redirected when trying to log into my Microsoft work account"

Agent: "That sounds like an SSO cookie issue. Let me clear the authentication cookies for you."

[Tool executes: clear_chrome_cookies with domain "login.microsoftonline.com"]
[Chrome closes, cookies cleared, Chrome reopens]

Agent: "I've cleared the SSO cookies. Try logging in again - the redirect loop should be fixed."
```

### Example 3: Outlook Stuck
```
User: "Outlook won't start, it's stuck on Loading Profile"

Agent: "I can reset your Outlook profile. This will create a fresh start. I'll back up your current profile first."

[Tool executes: reset_outlook_profile with backup=true]
[Outlook closes, profile backed up, database reset, Outlook reopens]

Agent: "Your Outlook profile has been reset and backed up to your Desktop. Please sign in again and wait for the initial sync to complete."
```

---

## Why These Tools Impress

1. **Real Automation** - Not just showing instructions, actually doing the work
2. **GUI Interaction** - Opens apps, clicks buttons, navigates settings
3. **Smart Detection** - Knows if apps are running, handles edge cases
4. **Automatic Backups** - Professional safety measures
5. **Cross-Platform Ready** - Built for macOS, easily adaptable to Windows

---

## Future Enhancements

- Add VPN connection troubleshooting
- Add printer driver reinstallation
- Add network diagnostics
- Add Active Directory password reset
- Add bulk operations (reset multiple profiles, clear multiple domains)

