#!/bin/bash

# Reset Microsoft Outlook Profile (macOS)
# Fixes "Loading Profile", sync issues, and corrupted database problems

BACKUP="${1:-true}"

# echo "=== Outlook Profile Reset Tool (macOS) ==="
# echo "Backup Old Profile: $BACKUP"
# echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script only works on macOS"
    exit 1
fi

# Check if Outlook is installed
OUTLOOK_PATH="/Applications/Microsoft Outlook.app"
if [ ! -d "$OUTLOOK_PATH" ]; then
    echo "Error: Microsoft Outlook is not installed"
    exit 1
fi

# echo "🔍 Checking Outlook status..."

# Check if Outlook is running
OUTLOOK_RUNNING=false
if pgrep -x "Microsoft Outlook" > /dev/null; then
    OUTLOOK_RUNNING=true
    # echo "✓ Outlook is currently running"
fi

# echo ""
# echo "📋 Actions to perform:"
# echo "   1. Close Outlook (if running)"
# echo "   2. Backup current profile database"
# echo "   3. Reset Outlook profile"
# echo "   4. Clear cache and temp files"
# echo "   5. Restart Outlook"
# echo ""

# Define Outlook data locations
OUTLOOK_DATA="$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook"
OUTLOOK_PROFILE="$OUTLOOK_DATA/Outlook 15 Profiles"
OUTLOOK_CACHE="$HOME/Library/Caches/com.microsoft.Outlook"
OUTLOOK_PREFS="$HOME/Library/Preferences/com.microsoft.Outlook.plist"

# If Outlook is running, close it
if [ "$OUTLOOK_RUNNING" = true ]; then
    # echo "🔧 Closing Outlook..."
    osascript -e 'tell application "Microsoft Outlook" to quit' 2>/dev/null
    sleep 3
    
    # Force quit if still running
    if pgrep -x "Microsoft Outlook" > /dev/null; then
        killall "Microsoft Outlook" 2>/dev/null
        sleep 2
    fi
    
    # echo "✓ Outlook closed"
    # echo ""
fi

# Backup current profile if requested
if [ "$BACKUP" = "true" ]; then
    BACKUP_DIR="$HOME/Desktop/Outlook_Backup_$(date +%Y%m%d_%H%M%S)"
    # echo "💾 Creating backup..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup profile
    if [ -d "$OUTLOOK_PROFILE" ]; then
        cp -R "$OUTLOOK_PROFILE" "$BACKUP_DIR/Profiles" 2>/dev/null
        # echo "✓ Backed up profile"
    fi
    
    # Backup main database
    if [ -d "$OUTLOOK_DATA" ]; then
        cp -R "$OUTLOOK_DATA"/*.db* "$BACKUP_DIR/" 2>/dev/null
        # echo "✓ Backed up database files"
    fi
    
    echo "✅ Backup created at: $BACKUP_DIR"
    # echo ""
fi

# Reset Outlook profile
# echo "🔧 Resetting Outlook profile..."

# Method 1: Remove profile folder
if [ -d "$OUTLOOK_PROFILE" ]; then
    rm -rf "$OUTLOOK_PROFILE" 2>/dev/null
    # echo "✓ Removed old profile"
fi

# Method 2: Clear Outlook cache
if [ -d "$OUTLOOK_CACHE" ]; then
    rm -rf "$OUTLOOK_CACHE" 2>/dev/null
    # echo "✓ Cleared cache"
fi

# Method 3: Reset preferences
if [ -f "$OUTLOOK_PREFS" ]; then
    rm "$OUTLOOK_PREFS" 2>/dev/null
    # echo "✓ Reset preferences"
fi

# Method 4: Clear identity database (causes fresh profile creation)
if [ -d "$OUTLOOK_DATA" ]; then
    # Remove Main Profile folder which triggers profile recreation
    find "$OUTLOOK_DATA" -name "Main Profile" -type d -exec rm -rf {} + 2>/dev/null
    # echo "✓ Cleared main profile folder"
fi

# Use Outlook's built-in database utility if available
if [ -f "/Applications/Microsoft Outlook.app/Contents/MacOS/Microsoft Database Utility.app/Contents/MacOS/Microsoft Database Utility" ]; then
    # echo "🔧 Running Microsoft Database Utility..."
    open "/Applications/Microsoft Outlook.app/Contents/MacOS/Microsoft Database Utility.app" 2>/dev/null
    sleep 2
    
    # Try to automate clicking "Rebuild" button
    osascript <<EOF 2>/dev/null
tell application "System Events"
    repeat 10 times
        try
            if exists (process "Microsoft Database Utility") then
                tell process "Microsoft Database Utility"
                    click button "Rebuild" of window 1
                    delay 1
                    exit repeat
                end if
            end if
        end try
        delay 0.5
    end repeat
end tell
EOF
    
    # echo "✓ Database utility launched"
else
    # If utility not found, just do manual reset
    :
fi

echo ""
echo "✅ Outlook profile has been reset!"
echo ""
echo "📝 Next steps:"
echo "   1. Outlook will now reopen"
echo "   2. You'll be prompted to sign in again"
echo "   3. Enter your email and password"
echo "   4. Wait for initial sync to complete (this may take a few minutes)"
echo ""

# Reopen Outlook
# echo "🔄 Reopening Outlook..."
sleep 2
open -a "Microsoft Outlook"
# echo "✓ Outlook opened"

echo ""
echo "⏱️  Please wait for Outlook to:"
echo "   • Create a new profile"
echo "   • Download your mailbox"
echo "   • Sync your calendar and contacts"
echo ""
echo "💡 If issues persist:"
echo "   • Check your internet connection"
echo "   • Verify your email credentials"
echo "   • Contact IT support for server-side issues"
echo ""

exit 0

