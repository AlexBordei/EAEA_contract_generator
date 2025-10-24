# Credentials Folder

This folder should contain your Google Sheets service account credentials.

## Required File

**`google_sheets_key.json`** - Google Cloud service account key

## How to Get This File

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to: **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **Service Account**
5. Fill in the details and create
6. Click on the created service account
7. Go to **Keys** tab
8. Click **Add Key** → **Create new key**
9. Select **JSON** format
10. Download the file
11. Rename it to `google_sheets_key.json`
12. Place it in this folder

## What the File Contains

The JSON file contains:
- `type`: "service_account"
- `project_id`: Your Google Cloud project ID
- `private_key_id`: Key identifier
- `private_key`: RSA private key (keep secret!)
- `client_email`: Service account email (ends with @*.iam.gserviceaccount.com)
- `client_id`: Service account ID
- Other metadata

## Important Notes

⚠️ **Security:**
- Never commit this file to version control
- Keep it secure and private
- Don't share it publicly
- The `.gitignore` file already excludes it

📧 **Don't forget:**
- Share your Google Spreadsheet with the `client_email` from this JSON
- Give it "Editor" permissions
- Otherwise, the app won't be able to write to your sheet

## File Structure

```
credentials/
├── README.md                    # This file
└── google_sheets_key.json       # Your service account key (add this)
```

## Verification

After adding the file, run:
```bash
python3 test_setup.py
```

It will verify that the credentials file exists and is properly configured.

