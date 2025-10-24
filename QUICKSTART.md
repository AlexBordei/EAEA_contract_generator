# 🚀 Quick Start Guide

Get the Contract Automation System running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Gmail account
- Google Cloud account (free tier works)

## Step-by-Step Setup

### 1. Install Dependencies (2 minutes)

```bash
pip3 install -r requirements.txt
```

### 2. Setup Gmail OAuth2 (5 minutes)

#### a) Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "Contract Automation"
3. Enable **Gmail API** and **Google Sheets API**

#### b) Create OAuth2 Credentials
1. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
2. Configure consent screen (internal use is fine)
3. Choose **"Desktop app"** as application type
4. Download credentials JSON

#### c) Run Setup Script
```bash
python3 setup_gmail_oauth.py
```
- Provide path to downloaded credentials JSON
- Authorize in browser
- Script creates `.env` file automatically

### 3. Setup Google Sheets (3 minutes)

#### a) Create Service Account
1. In Google Cloud Console → "Credentials"
2. "Create Credentials" → "Service Account"
3. Create new key → JSON format
4. Save as `credentials/google_sheets_key.json`

#### b) Create Spreadsheet
1. Create new Google Spreadsheet
2. Copy ID from URL: `docs.google.com/spreadsheets/d/[THIS-IS-THE-ID]/edit`
3. Share spreadsheet with service account email (from JSON file)
4. Give "Editor" permissions

#### c) Update Configuration
Edit `.env` file:
```env
GOOGLE_SHEETS_SPREADSHEET_ID=paste_your_spreadsheet_id_here
ADMIN_EMAIL=your_admin_email@example.com
```

### 4. Run the Application

```bash
./run.sh
```

Or:
```bash
python3 -m uvicorn app.main:app --reload --port 8000
```

### 5. Test It Out

1. Open browser: http://localhost:8000
2. Fill in the form
3. Submit
4. Check:
   - ✅ PDF generated in `output/` folder
   - ✅ Entry added to Google Sheets
   - ✅ Email sent to client (check inbox/spam)

## 🎉 You're Done!

The system is now running and ready to automate your contracts.

## Common Issues

### "Gmail authentication failed"
- Re-run `setup_gmail_oauth.py`
- Make sure you selected "Desktop app" for OAuth2
- Check Gmail API is enabled

### "Spreadsheet not found"
- Verify spreadsheet ID in `.env`
- Confirm spreadsheet is shared with service account
- Check Google Sheets API is enabled

### "Module not found"
- Run: `pip3 install -r requirements.txt`
- Make sure you're using Python 3.8+

## 📧 Need Help?

Check the full [README.md](README.md) for detailed documentation.

## 🔐 Security Tip

Never commit these files to git:
- `.env` (contains secrets)
- `credentials/*.json` (service account keys)
- `output/*.pdf` (contains personal data)

---

**Ready to automate! 🎊**

