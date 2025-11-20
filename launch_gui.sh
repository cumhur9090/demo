#!/bin/bash

# Quick launch script for IT Support Agent GUI

echo "🚀 Launching IT Support Agent GUI..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env with your OPENAI_API_KEY"
    echo ""
    exit 1
fi

# Check if Python is available
if command -v python3 &> /dev/null; then
    python3 gui.py
elif command -v python &> /dev/null; then
    python gui.py
else
    echo "❌ Error: Python not found!"
    echo "Please install Python 3.x"
    exit 1
fi

