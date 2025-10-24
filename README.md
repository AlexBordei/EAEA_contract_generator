# Contract Automation System

Automated contract generation, Google Sheets logging, and email delivery system for Early Alpha Engineering S.R.L.

## 🚀 Features

- ✅ Modern web form for contract data collection
- ✅ Automatic PDF contract generation with placeholder replacement
- ✅ Google Sheets integration for submission logging
- ✅ Gmail OAuth2 authentication (like n8n)
- ✅ Automated email delivery to clients and admin
- ✅ Professional, responsive UI with Bootstrap 5
- ✅ Real-time form validation
- ✅ Error handling and user feedback

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud account (for Gmail API and Google Sheets API)
- Gmail account for sending emails

## 🛠️ Installation

### 1. Clone or Download the Project

```bash
cd contract_completion
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Setup Gmail OAuth2 (like n8n)

1. **Create a Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Note your project ID

2. **Enable Gmail API:**
   - In the Cloud Console, go to "APIs & Services" > "Library"
   - Search for "Gmail API" and click "Enable"

3. **Create OAuth2 Credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - Choose "Desktop app" as application type
   - Name it (e.g., "Contract Automation")
   - Download the credentials JSON file

4. **Run the Setup Script:**
   ```bash
   python setup_gmail_oauth.py
   ```
   - Follow the prompts
   - Provide the path to your downloaded credentials JSON
   - Authorize the application in your browser
   - The script will generate your `.env` file with OAuth2 tokens

### Step 2: Setup Google Sheets API

1. **Enable Google Sheets API:**
   - In Google Cloud Console, go to "APIs & Services" > "Library"
   - Search for "Google Sheets API" and click "Enable"

2. **Create Service Account:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in service account details
   - Click "Create and Continue"
   - Skip optional steps and click "Done"

3. **Create Service Account Key:**
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format
   - Download the file and save it as `credentials/google_sheets_key.json`

4. **Create a Google Spreadsheet:**
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new spreadsheet
   - Copy the spreadsheet ID from the URL:
     ```
     https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
     ```
   - Share the spreadsheet with the service account email (found in the JSON file)
     - Give it "Editor" permissions

5. **Update `.env` file:**
   ```env
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
   ```

### Step 3: Configure Admin Email

Update the `.env` file with your admin email:

```env
ADMIN_EMAIL=your_email@example.com
```

### Step 4: Verify Configuration

Check your `.env` file looks like this:

```env
# Gmail API OAuth2 Credentials
GMAIL_CLIENT_ID=your_client_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token

# Admin Email
ADMIN_EMAIL=admin@example.com

# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials/google_sheets_key.json

# Contract Configuration
CONTRACT_PDF_PATH=crm.eaea.ro Draft - Contract prestari servicii Early Alpha.docx (1).pdf
OUTPUT_FOLDER=output

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
```

## 🚀 Running the Application

### Development Mode

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the built-in runner:

```bash
python -m app.main
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

## 📝 Usage

1. **Open the web form** at `http://localhost:8000`
2. **Fill in all required fields:**
   - Contract metadata (number, date)
   - Contact person information
   - Emergency contact details
   - Student information
   - Course details
3. **Submit the form**
4. **The system will:**
   - Generate a PDF contract with filled data
   - Save the submission to Google Sheets
   - Send the contract via email to the client (with admin CC'd)
   - Display success/error messages

## 📁 Project Structure

```
contract_completion/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration settings
│   ├── pdf_handler.py       # PDF processing
│   ├── email_service.py     # Gmail OAuth2 email service
│   ├── sheets_service.py    # Google Sheets integration
│   └── templates/
│       └── form.html        # Contract form UI
├── static/
│   ├── css/
│   └── js/
├── credentials/
│   └── google_sheets_key.json
├── output/                   # Generated contracts
├── requirements.txt
├── setup_gmail_oauth.py     # OAuth2 setup helper
├── env.example              # Environment variables template
├── .env                     # Your configuration (gitignored)
├── placeholders.json        # Extracted placeholders
└── README.md
```

## 🔍 Health Check

Check if all services are configured correctly:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "gmail_configured": true,
  "sheets_configured": true,
  "pdf_template_exists": true
}
```

## 📊 Extracted Placeholders

The system uses these placeholders in the contract template:

- `{no}` - Contract number
- `{date}` - Contract date
- `{contact_first_name}` - Contact first name
- `{contact_last_name}` - Contact last name
- `{contact_address}` - Contact address
- `{contact_phone}` - Contact phone
- `{contact_email}` - Contact email
- `{contact_id_series}` - ID series
- `{contact_id_no}` - ID number
- `{contact_personal_no}` - CNP
- `{contact_emergency_first_name}` - Emergency contact first name
- `{contact_emergency_last_name}` - Emergency contact last name
- `{contact_emergency_phone_no}` - Emergency contact phone
- `{student_first_name}` - Student first name
- `{student_last_name}` - Student last name
- `{student_birth_date}` - Student birth date
- `{if_14_student_first_name}` - Student first name (if under 14)
- `{if_14_student_last_name}` - Student last name (if under 14)
- `{if_14_date}` - Date (if under 14)
- `{subscriptions_types}` - Subscription types
- `{timeslots}` - Course timeslots

## 🐛 Troubleshooting

### Gmail Authentication Issues

**Problem:** "Error authenticating with Gmail API"

**Solutions:**
1. Re-run `setup_gmail_oauth.py`
2. Verify Gmail API is enabled in Google Cloud Console
3. Check that OAuth2 credentials are for "Desktop application"
4. Ensure redirect URIs include `http://localhost`

### Google Sheets Issues

**Problem:** "Could not authenticate with Google Sheets"

**Solutions:**
1. Verify service account JSON file exists at `credentials/google_sheets_key.json`
2. Check that Google Sheets API is enabled
3. Ensure the spreadsheet is shared with the service account email
4. Verify spreadsheet ID in `.env` is correct

### PDF Generation Issues

**Problem:** PDF is blank or formatting is incorrect

**Solutions:**
1. The current implementation creates a simple text-based PDF
2. For better formatting, consider using:
   - PDF form fields in the original template
   - A DOCX template with python-docx
   - Professional PDF libraries like PyMuPDF or pdfplumber

### Email Not Sending

**Problem:** Emails are not being delivered

**Solutions:**
1. Check that `ADMIN_EMAIL` is set in `.env`
2. Verify Gmail OAuth2 tokens are valid
3. Check spam/junk folders
4. Review application logs for error messages

## 🔒 Security Notes

- Never commit `.env` file or credentials to version control
- Keep OAuth2 tokens secure
- Restrict service account permissions to only necessary scopes
- Use environment variables for all sensitive data
- Consider adding authentication for the web form in production

## 📧 Email Template

The system sends professionally formatted HTML emails with:
- Company branding
- Client and student names
- Attached PDF contract
- CC to admin email

## 🔄 Workflow

1. **Client fills form** → 2. **Data validation** → 3. **PDF generation** → 4. **Save to Sheets** → 5. **Send emails** → 6. **Confirmation**

## 📚 Technologies Used

- **FastAPI** - Modern Python web framework
- **Jinja2** - Template engine
- **Bootstrap 5** - Frontend UI framework
- **PyPDF2** - PDF text extraction
- **ReportLab** - PDF generation
- **Google APIs** - Gmail and Sheets integration
- **OAuth2** - Secure authentication
- **Pydantic** - Data validation

## 🎯 Future Enhancements

- [ ] Add user authentication
- [ ] Improve PDF generation with better formatting
- [ ] Add support for multiple contract templates
- [ ] Implement contract versioning
- [ ] Add digital signatures
- [ ] Create admin dashboard
- [ ] Add contract search and filtering
- [ ] Implement email templates customization
- [ ] Add SMS notifications
- [ ] Support multiple languages

## 📝 License

Proprietary - Early Alpha Engineering S.R.L.

## 👥 Support

For support, contact: info@earlyalpha.ro

---

**Built with ❤️ for Early Alpha Engineering S.R.L.**

