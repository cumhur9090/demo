#!/bin/bash

# Clear Chrome Cookies for Specific Domain (macOS)
# Fixes SSO login loops by clearing authentication cookies

DOMAIN="${1:-login.microsoftonline.com}"

echo "=== Chrome Cookie Cleaner (macOS) ==="
echo "Target Domain: $DOMAIN"
sleep 0.5
echo ""

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

echo "🔍 Checking Chrome status..."
sleep 0.5

# Check if Chrome is running
CHROME_RUNNING=false
if pgrep -x "Google Chrome" > /dev/null; then
    CHROME_RUNNING=true
    echo "✓ Chrome is currently running"
    sleep 0.5
fi

echo ""

# If Chrome is running, we need to close it
if [ "$CHROME_RUNNING" = true ]; then
    echo "🔧 Closing Chrome..."
    sleep 0.5
    osascript -e 'tell application "Google Chrome" to quit' 2>/dev/null
    sleep 1
    echo "✓ Chrome closed"
    sleep 0.5
    echo ""
fi

# Alternative: Direct file manipulation (more reliable but requires Chrome to be closed)
# Find Chrome's cookie database
COOKIE_DB="$HOME/Library/Application Support/Google/Chrome/Default/Cookies"

if [ -f "$COOKIE_DB" ]; then
    echo "🗄️  Found Chrome cookie database"
    sleep 0.5
    
    # Make a backup
    BACKUP_FILE="${COOKIE_DB}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$COOKIE_DB" "$BACKUP_FILE" 2>/dev/null
    echo "✓ Created backup"
    sleep 0.5
    
    # Try to delete cookies for specific domain using sqlite3
    if command -v sqlite3 &> /dev/null; then
        echo "🔧 Removing cookies for $DOMAIN..."
        sleep 0.5
        sqlite3 "$COOKIE_DB" "DELETE FROM cookies WHERE host_key LIKE '%${DOMAIN}%';" 2>/dev/null
        DELETED_COUNT=$(sqlite3 "$COOKIE_DB" "SELECT changes();" 2>/dev/null)
        
        if [ "$DELETED_COUNT" -gt "0" ]; then
            echo "✅ Cleared $DELETED_COUNT cookie(s) for $DOMAIN"
            sleep 0.5
        else
            echo "ℹ️  No cookies found for $DOMAIN (may have been cleared already)"
            sleep 0.5
        fi
    fi
fi

echo ""
echo "📝 Next steps:"
sleep 0.5
echo "   1. Chrome will now reopen"
echo "   2. Try logging in again to your SSO portal"
echo "   3. The login loop should be resolved"
sleep 0.5
echo ""

# Reopen Chrome
if [ "$CHROME_RUNNING" = true ]; then
    echo "🔄 Reopening Chrome..."
    sleep 0.5
    open -a "Google Chrome"
    echo "✓ Chrome reopened"
    sleep 0.5
fi

echo ""
echo "✅ Cookie clearing complete!"
sleep 0.5
echo ""
echo "💡 If the issue persists:"
echo "   • Try restarting your computer"
echo "   • Check if your network requires VPN"
echo "   • Contact your IT admin for SSO configuration"
echo ""

exit 0
