#!/bin/bash
# Run the contract automation application

echo "🚀 Starting Contract Automation System..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please run setup_gmail_oauth.py first to configure OAuth2"
    echo ""
fi

# Check if credentials exist
if [ ! -f credentials/google_sheets_key.json ]; then
    echo "⚠️  Warning: Google Sheets credentials not found!"
    echo "   Please add credentials/google_sheets_key.json"
    echo ""
fi

# Run the application
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

