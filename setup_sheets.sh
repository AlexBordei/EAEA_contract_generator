#!/bin/bash

# Setup script for Google Sheets integration

echo "📊 Google Sheets Setup Helper"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Extract service account email
SERVICE_EMAIL=$(python3 -c "import json; data = json.load(open('credentials/google_sheets_key.json')); print(data['client_email'])" 2>/dev/null)

if [ -z "$SERVICE_EMAIL" ]; then
    echo -e "${RED}❌ Could not find service account credentials${NC}"
    echo "   Make sure credentials/google_sheets_key.json exists"
    exit 1
fi

echo -e "${GREEN}✅ Service Account Found${NC}"
echo ""
echo "📧 Service Account Email:"
echo -e "${YELLOW}$SERVICE_EMAIL${NC}"
echo ""

# Spreadsheet ID
SPREADSHEET_ID="1DNJ1gt3KlzdlAWQ5T0yVcySUZ1cYCPiUQ3GUzEryu58"

echo "📋 Spreadsheet:"
echo "   ID: $SPREADSHEET_ID"
echo "   URL: https://docs.google.com/spreadsheets/d/$SPREADSHEET_ID/edit"
echo ""

echo "🔧 ACTION REQUIRED:"
echo "================================"
echo ""
echo "1. Open your spreadsheet:"
echo "   https://docs.google.com/spreadsheets/d/$SPREADSHEET_ID/edit"
echo ""
echo "2. Click the 'Share' button (top-right)"
echo ""
echo "3. Add this email with 'Editor' permissions:"
echo -e "   ${YELLOW}$SERVICE_EMAIL${NC}"
echo ""
echo "4. Uncheck 'Notify people' (it's a service account)"
echo ""
echo "5. Click 'Share'"
echo ""

echo "✅ After sharing, test the connection:"
echo "   python3 test_sheets.py"
echo ""

