# 🔧 Troubleshooting Guide

Common issues and their solutions for the Contract Automation System.

## Installation Issues

### "Module not found" errors

**Problem:** Python can't find installed packages

**Solutions:**
```bash
# Reinstall dependencies
pip3 install -r requirements.txt

# Check Python version (needs 3.8+)
python3 --version

# Make sure you're using the right pip
which pip3
```

### Virtual environment issues

**Problem:** Packages installed but not found

**Solutions:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Gmail OAuth2 Issues

### "Error authenticating with Gmail API"

**Problem:** OAuth2 credentials are invalid or expired

**Solutions:**

1. **Re-run the setup script:**
   ```bash
   python3 setup_gmail_oauth.py
   ```

2. **Check Gmail API is enabled:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to: APIs & Services → Library
   - Search for "Gmail API"
   - Ensure it's enabled

3. **Verify OAuth2 credentials type:**
   - In Google Cloud Console → Credentials
   - Your OAuth 2.0 Client ID should be type: **Desktop app**
   - NOT "Web application" or "Other"

4. **Check redirect URIs:**
   - Edit your OAuth 2.0 Client
   - Authorized redirect URIs should include:
     - `http://localhost`
     - `http://localhost:8000`

### "Refresh token not found"

**Problem:** `.env` file missing refresh token

**Solutions:**
```bash
# Delete old .env
rm .env

# Re-run OAuth setup
python3 setup_gmail_oauth.py
```

### "Invalid grant" error

**Problem:** Refresh token has expired or been revoked

**Solutions:**
1. Revoke access in [Google Account](https://myaccount.google.com/permissions)
2. Re-run `setup_gmail_oauth.py`
3. Authorize the application again

## Google Sheets Issues

### "Could not authenticate with Google Sheets"

**Problem:** Service account credentials missing or invalid

**Solutions:**

1. **Check file exists:**
   ```bash
   ls -la credentials/google_sheets_key.json
   ```

2. **Verify file format:**
   ```bash
   # Should be valid JSON starting with:
   head -n 5 credentials/google_sheets_key.json
   # {
   #   "type": "service_account",
   #   "project_id": "...",
   ```

3. **Re-download credentials:**
   - Go to Google Cloud Console
   - APIs & Services → Credentials
   - Find your service account
   - Keys tab → Add Key → Create new key → JSON

### "Spreadsheet not found" or "Permission denied"

**Problem:** Spreadsheet not shared with service account

**Solutions:**

1. **Get service account email:**
   ```bash
   grep client_email credentials/google_sheets_key.json
   ```
   Should be something like: `account-name@project-id.iam.gserviceaccount.com`

2. **Share spreadsheet:**
   - Open your Google Spreadsheet
   - Click "Share" button
   - Paste the service account email
   - Give "Editor" permissions
   - Uncheck "Notify people"
   - Click "Share"

3. **Verify spreadsheet ID:**
   - URL format: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`
   - Copy the ID between `/d/` and `/edit`
   - Update in `.env`: `GOOGLE_SHEETS_SPREADSHEET_ID=your_id_here`

### "Google Sheets API not enabled"

**Problem:** API not activated in Google Cloud

**Solutions:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to: APIs & Services → Library
3. Search for "Google Sheets API"
4. Click "Enable"

## Application Issues

### Application won't start

**Problem:** Import errors or configuration issues

**Solutions:**

1. **Run test script:**
   ```bash
   python3 test_setup.py
   ```

2. **Check for missing files:**
   ```bash
   # Verify app structure
   ls -la app/
   ```

3. **Check Python path:**
   ```bash
   # Should show app/ directory
   python3 -c "import sys; print('\n'.join(sys.path))"
   ```

### "Port already in use"

**Problem:** Port 8000 is occupied

**Solutions:**

1. **Use different port:**
   ```bash
   python3 -m uvicorn app.main:app --port 8080
   ```

2. **Find and kill process:**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   
   # Kill it
   kill -9 <PID>
   ```

### Form submission fails

**Problem:** Server returns error on submit

**Solutions:**

1. **Check browser console** (F12)
   - Look for JavaScript errors
   - Check network tab for failed requests

2. **Check server logs:**
   - Terminal where uvicorn is running
   - Look for error messages and stack traces

3. **Verify form data:**
   - Ensure all required fields are filled
   - Check CNP format (13 digits)
   - Verify email format

## PDF Generation Issues

### PDF is blank or poorly formatted

**Problem:** Current implementation uses simple text rendering

**Solutions:**

**Option 1 - Use PDF Form Fields:**
1. Edit original PDF in Adobe Acrobat
2. Add form fields matching placeholder names
3. Use PyPDF2 to fill form fields instead of text replacement

**Option 2 - Use DOCX Template:**
```python
# Install python-docx
pip install python-docx

# Modify pdf_handler.py to:
# 1. Load DOCX template
# 2. Replace placeholders
# 3. Convert to PDF
```

**Option 3 - Use Advanced PDF Library:**
```bash
pip install PyMuPDF  # or pdfplumber
```

### Special characters not displaying

**Problem:** Romanian characters (ă, î, ș, ț, â) not rendered

**Solutions:**

1. **Use Unicode font in ReportLab:**
   ```python
   from reportlab.pdfbase import pdfmetrics
   from reportlab.pdfbase.ttfonts import TTFont
   
   # Register a Unicode font
   pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
   c.setFont('Arial', 10)
   ```

2. **Ensure UTF-8 encoding everywhere**

## Email Issues

### Emails not being received

**Problem:** Emails sent but not arriving

**Solutions:**

1. **Check spam/junk folders**

2. **Verify email address:**
   ```bash
   # Check .env file
   grep ADMIN_EMAIL .env
   ```

3. **Check Gmail sending limits:**
   - Gmail API has sending limits
   - Free tier: ~100 emails/day
   - Check [quota usage](https://console.cloud.google.com/apis/dashboard)

4. **Test email service:**
   ```python
   # Test sending
   from app.email_service import EmailService
   from app.config import settings
   
   service = EmailService(
       settings.gmail_client_id,
       settings.gmail_client_secret,
       settings.gmail_refresh_token
   )
   
   result = service.send_email(
       to_email="test@example.com",
       subject="Test",
       body_html="<p>Test email</p>",
       body_text="Test email"
   )
   print(f"Email sent: {result}")
   ```

### Email attachments missing

**Problem:** PDF not attached to email

**Solutions:**

1. **Check PDF exists:**
   ```bash
   ls -la output/
   ```

2. **Verify PDF path in code:**
   - Check `email_service.py` → `send_contract_email()`
   - Ensure `contract_pdf_path` is correct

3. **Check file size:**
   - Gmail has 25MB attachment limit
   - Most contracts should be < 1MB

## Configuration Issues

### ".env file not found"

**Problem:** Configuration file missing

**Solutions:**

1. **Create from template:**
   ```bash
   cp env.example .env
   ```

2. **Or run OAuth setup:**
   ```bash
   python3 setup_gmail_oauth.py
   ```
   It will create `.env` automatically

### "Settings validation error"

**Problem:** Invalid values in .env

**Solutions:**

1. **Check .env format:**
   ```bash
   # Each line should be: KEY=value
   # No spaces around =
   # No quotes needed
   cat .env
   ```

2. **Verify required variables:**
   ```bash
   grep -E "GMAIL_CLIENT_ID|GMAIL_CLIENT_SECRET|GMAIL_REFRESH_TOKEN|ADMIN_EMAIL|GOOGLE_SHEETS_SPREADSHEET_ID" .env
   ```

3. **Check for special characters:**
   - If values contain special chars, use quotes:
     ```env
     ADMIN_EMAIL="user+tag@example.com"
     ```

## Performance Issues

### Slow PDF generation

**Problem:** Contract takes long to generate

**Solutions:**

1. **Use PDF form fields** instead of text rendering
2. **Optimize PDF template** (reduce file size)
3. **Consider caching** for repeated data

### High memory usage

**Problem:** Application uses too much RAM

**Solutions:**

1. **Process PDFs in batches**
2. **Clear temp files:**
   ```bash
   rm -rf output/*.pdf
   ```
3. **Restart application periodically**

## Database/Sheets Issues

### Duplicate entries in Google Sheets

**Problem:** Same submission appears multiple times

**Solutions:**

1. **Add unique constraint** in code
2. **Check for double submissions**
3. **Implement idempotency keys**

### Sheets formatting broken

**Problem:** Data not aligning with columns

**Solutions:**

1. **Re-initialize headers:**
   ```python
   from app.sheets_service import SheetsService
   from app.config import settings
   
   service = SheetsService(
       settings.google_sheets_credentials_file,
       settings.google_sheets_spreadsheet_id
   )
   service.ensure_headers()
   ```

2. **Manually fix headers** in Google Sheets

## Testing & Debugging

### Enable debug logging

```bash
# Run with debug output
python3 -m uvicorn app.main:app --reload --log-level debug
```

### Test individual components

```python
# Test PDF handler
from app.pdf_handler import PDFHandler
handler = PDFHandler("contract_template.pdf")
placeholders = handler.get_placeholders_from_pdf()
print(placeholders)

# Test Sheets service
from app.sheets_service import SheetsService
service = SheetsService("credentials/google_sheets_key.json", "sheet_id")
result = service.append_submission({"test": "data"})
print(f"Sheets write: {result}")

# Test Email service
from app.email_service import EmailService
service = EmailService("client_id", "client_secret", "refresh_token")
# service.send_email(...)
```

### Check health endpoint

```bash
curl http://localhost:8000/health
```

Response should show:
```json
{
  "status": "healthy",
  "gmail_configured": true,
  "sheets_configured": true,
  "pdf_template_exists": true
}
```

## Getting More Help

### Useful Commands

```bash
# View real-time logs
tail -f app.log

# Check Python environment
python3 -m pip list

# Verify network connectivity
curl https://www.googleapis.com

# Check file permissions
ls -la credentials/
```

### Where to Find Logs

- **Application logs:** Terminal where uvicorn is running
- **Browser logs:** F12 → Console
- **Gmail API logs:** [Google Cloud Console](https://console.cloud.google.com/logs)
- **Sheets API logs:** Same as above

### Report Issues

If you still have issues:

1. Run the test script:
   ```bash
   python3 test_setup.py > test_results.txt
   ```

2. Check health endpoint:
   ```bash
   curl http://localhost:8000/health > health.json
   ```

3. Collect logs from terminal

4. Review error messages carefully

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gmail API Guide](https://developers.google.com/gmail/api)
- [Google Sheets API Guide](https://developers.google.com/sheets/api)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

**Still stuck? Review README.md and QUICKSTART.md for step-by-step setup instructions.**

