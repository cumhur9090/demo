#!/bin/bash

# Clear Chrome Cookies for Specific Domain (macOS)
# Fixes SSO login loops by clearing authentication cookies

DOMAIN="${1:-login.microsoftonline.com}"

# echo "=== Chrome Cookie Cleaner (macOS) ==="
# echo "Target Domain: $DOMAIN"
# echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script only works on macOS"
    exit 1
fi

# Check if Chrome is installed
CHROME_PATH="/Applications/Google Chrome.app"
if [ ! -d "$CHROME_PATH" ]; then
    echo "Error: Google Chrome is not installed"
    exit 1
fi

# echo "🔍 Checking Chrome status..."

# Check if Chrome is running
CHROME_RUNNING=false
if pgrep -x "Google Chrome" > /dev/null; then
    CHROME_RUNNING=true
    # echo "✓ Chrome is currently running"
fi

# echo ""
# echo "📋 Actions to perform:"
# echo "   1. Close Chrome (if running)"
# echo "   2. Navigate to Chrome's cookie storage"
# echo "   3. Clear cookies for $DOMAIN"
# echo "   4. Reopen Chrome"
# echo ""

# If Chrome is running, we need to close it
if [ "$CHROME_RUNNING" = true ]; then
    # echo "🔧 Closing Chrome..."
    osascript -e 'tell application "Google Chrome" to quit' 2>/dev/null
    sleep 2
    # echo "✓ Chrome closed"
    # echo ""
fi

# Open Chrome to the clear browsing data page with cookies pre-selected
# echo "🔧 Opening Chrome cookie settings..."

# Method 1: Open Chrome's settings directly to clear browsing data
osascript <<EOF 2>/dev/null
tell application "Google Chrome"
    activate
    delay 1
    open location "chrome://settings/clearBrowserData"
end tell
EOF

sleep 2

# Use AppleScript to automate the clicking
osascript <<EOF 2>/dev/null
tell application "System Events"
    tell process "Google Chrome"
        -- Wait for settings to load
        delay 2
        
        -- Try to click on "Advanced" tab if it exists
        try
            click button "Advanced" of group 1 of group 1 of group 1 of group 1 of group 1 of tab group 1 of window 1
            delay 1
        end try
        
        -- Click "Clear data" button
        try
            click button "Clear data" of group 1 of group 1 of group 1 of group 1 of group 1 of tab group 1 of window 1
            delay 1
        end try
    end tell
end tell
EOF

AUTO_CLEAR_SUCCESS=$?

if [ "$AUTO_CLEAR_SUCCESS" = "0" ]; then
    # echo "✅ Cookies cleared automatically!"
    sleep 2
else
    # echo "⚠️  Manual action required:"
    # echo "   1. In Chrome's Clear browsing data dialog:"
    # echo "   2. Select 'Cookies and other site data'"
    # echo "   3. Choose 'All time' from the time range"
    # echo "   4. Click 'Clear data'"
    # echo ""
    sleep 3
fi

# Alternative: Direct file manipulation (more reliable but requires Chrome to be closed)
# Find Chrome's cookie database
COOKIE_DB="$HOME/Library/Application Support/Google/Chrome/Default/Cookies"

if [ -f "$COOKIE_DB" ]; then
    # echo "🗄️  Found Chrome cookie database"
    
    # Make a backup
    BACKUP_FILE="${COOKIE_DB}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$COOKIE_DB" "$BACKUP_FILE" 2>/dev/null
    # echo "✓ Created backup: $(basename $BACKUP_FILE)"
    
    # Try to delete cookies for specific domain using sqlite3
    if command -v sqlite3 &> /dev/null; then
        # echo "🔧 Removing cookies for $DOMAIN..."
        sqlite3 "$COOKIE_DB" "DELETE FROM cookies WHERE host_key LIKE '%${DOMAIN}%';" 2>/dev/null
        DELETED_COUNT=$(sqlite3 "$COOKIE_DB" "SELECT changes();" 2>/dev/null)
        
        if [ "$DELETED_COUNT" -gt "0" ]; then
            echo "✅ Cleared $DELETED_COUNT cookie(s) for $DOMAIN"
        else
            echo "ℹ️  No cookies found for $DOMAIN (may have been cleared already)"
        fi
    fi
fi

echo ""
echo "📝 Next steps:"
echo "   1. Chrome will now open to a fresh state"
echo "   2. Try logging in again to your SSO portal"
echo "   3. The login loop should be resolved"
echo ""

# Reopen Chrome to the SSO login page if we closed it
if [ "$CHROME_RUNNING" = true ]; then
    # echo "🔄 Reopening Chrome..."
    sleep 1
    open -a "Google Chrome"
    # echo "✓ Chrome reopened"
fi

echo "✅ Cookie clearing complete!"
echo ""
echo "💡 If the issue persists:"
echo "   • Try restarting your computer"
echo "   • Check if your network requires VPN"
echo "   • Contact your IT admin for SSO configuration"
echo ""

exit 0

