#!/bin/bash

# Reset Microsoft Outlook Profile (macOS)
# Fixes "Loading Profile", sync issues, and corrupted database problems

BACKUP="${1:-true}"

echo "=== Outlook Profile Reset Tool (macOS) ==="
echo "Backup Old Profile: $BACKUP"
sleep 0.5
echo ""

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

echo "🔍 Checking Outlook status..."
sleep 0.5

# Check if Outlook is running
OUTLOOK_RUNNING=false
if pgrep -x "Microsoft Outlook" > /dev/null; then
    OUTLOOK_RUNNING=true
    echo "✓ Outlook is currently running"
    sleep 0.5
fi

echo ""

# Define Outlook data locations
OUTLOOK_DATA="$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook"
OUTLOOK_PROFILE="$OUTLOOK_DATA/Outlook 15 Profiles"
OUTLOOK_CACHE="$HOME/Library/Caches/com.microsoft.Outlook"
OUTLOOK_PREFS="$HOME/Library/Preferences/com.microsoft.Outlook.plist"

# If Outlook is running, close it
if [ "$OUTLOOK_RUNNING" = true ]; then
    echo "🔧 Closing Outlook..."
    sleep 0.5
    osascript -e 'tell application "Microsoft Outlook" to quit' 2>/dev/null
    sleep 2
    
    # Force quit if still running
    if pgrep -x "Microsoft Outlook" > /dev/null; then
        killall "Microsoft Outlook" 2>/dev/null
        sleep 1
    fi
    
    echo "✓ Outlook closed"
    sleep 0.5
    echo ""
fi

# Backup current profile if requested
if [ "$BACKUP" = "true" ]; then
    BACKUP_DIR="$HOME/Desktop/Outlook_Backup_$(date +%Y%m%d_%H%M%S)"
    echo "💾 Creating backup..."
    sleep 0.5
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup profile
    if [ -d "$OUTLOOK_PROFILE" ]; then
        cp -R "$OUTLOOK_PROFILE" "$BACKUP_DIR/Profiles" 2>/dev/null
        echo "✓ Backed up profile"
        sleep 0.5
    fi
    
    # Backup main database
    if [ -d "$OUTLOOK_DATA" ]; then
        cp -R "$OUTLOOK_DATA"/*.db* "$BACKUP_DIR/" 2>/dev/null
        echo "✓ Backed up database files"
        sleep 0.5
    fi
    
    echo "✅ Backup created at: $(basename $BACKUP_DIR)"
    sleep 0.5
    echo ""
fi

# Reset Outlook profile
echo "🔧 Resetting Outlook profile..."
sleep 0.5

# Method 1: Remove profile folder
if [ -d "$OUTLOOK_PROFILE" ]; then
    rm -rf "$OUTLOOK_PROFILE" 2>/dev/null
    echo "✓ Removed old profile"
    sleep 0.5
fi

# Method 2: Clear Outlook cache
if [ -d "$OUTLOOK_CACHE" ]; then
    rm -rf "$OUTLOOK_CACHE" 2>/dev/null
    echo "✓ Cleared cache"
    sleep 0.5
fi

# Method 3: Reset preferences
if [ -f "$OUTLOOK_PREFS" ]; then
    rm "$OUTLOOK_PREFS" 2>/dev/null
    echo "✓ Reset preferences"
    sleep 0.5
fi

# Method 4: Clear identity database (causes fresh profile creation)
if [ -d "$OUTLOOK_DATA" ]; then
    # Remove Main Profile folder which triggers profile recreation
    find "$OUTLOOK_DATA" -name "Main Profile" -type d -exec rm -rf {} + 2>/dev/null
    echo "✓ Cleared main profile folder"
    sleep 0.5
fi

echo ""
echo "✅ Outlook profile has been reset!"
sleep 0.5
echo ""
echo "📝 Next steps:"
sleep 0.5
echo "   1. Outlook will now reopen"
echo "   2. You'll be prompted to sign in again"
echo "   3. Enter your email and password"
echo "   4. Wait for initial sync to complete (this may take a few minutes)"
sleep 0.5
echo ""

# Reopen Outlook
echo "🔄 Reopening Outlook..."
sleep 0.5
open -a "Microsoft Outlook"
echo "✓ Outlook opened"
sleep 0.5

echo ""
echo "⏱️  Please wait for Outlook to:"
echo "   • Create a new profile"
echo "   • Download your mailbox"
echo "   • Sync your calendar and contacts"
sleep 0.5
echo ""
echo "💡 If issues persist:"
echo "   • Check your internet connection"
echo "   • Verify your email credentials"
echo "   • Contact IT support for server-side issues"
echo ""

exit 0
