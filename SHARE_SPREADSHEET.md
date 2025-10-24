# 🔧 Fix Google Sheets Access

## Problem
The service account cannot access your Google Spreadsheet, so submissions are not being saved.

## Solution
You need to **share the spreadsheet** with the service account email.

---

## 📋 Step-by-Step Instructions

### 1. Copy the Service Account Email

```
contract-automation@vibrant-victory-455816-r5.iam.gserviceaccount.com
```

### 2. Share Your Spreadsheet

1. **Open your spreadsheet:**  
   https://docs.google.com/spreadsheets/d/1DNJ1gt3KlzdlAWQ5T0yVcySUZ1cYCPiUQ3GUzEryu58/edit

2. **Click the "Share" button** (top-right corner)

3. **Paste the service account email:**
   ```
   contract-automation@vibrant-victory-455816-r5.iam.gserviceaccount.com
   ```

4. **Set permissions to "Editor"**

5. **Uncheck "Notify people"** (it's a service account, not a real person)

6. **Click "Share"** or "Send"

---

## ✅ Test the Connection

After sharing, run this test:

```bash
python3 test_sheets.py
```

You should see:
- ✅ Authentication successful
- ✅ Spreadsheet opened
- ✅ Successfully wrote test row

---

## 🎯 What This Enables

Once properly shared, the system will:
- ✅ Log all contract submissions to the spreadsheet
- ✅ Track timestamps and submission details
- ✅ Record email delivery status
- ✅ Provide a permanent record of all contracts

---

## 🔍 Troubleshooting

**Still not working?**

1. **Double-check the email is exactly:**
   ```
   contract-automation@vibrant-victory-455816-r5.iam.gserviceaccount.com
   ```

2. **Verify permissions are "Editor" (not "Viewer")**

3. **Make sure the spreadsheet ID matches:**
   ```
   1DNJ1gt3KlzdlAWQ5T0yVcySUZ1cYCPiUQ3GUzEryu58
   ```

4. **Check the service account credentials file exists:**
   ```bash
   ls -la credentials/google_sheets_key.json
   ```

---

## 📚 More Info

- Service accounts are special Google accounts used by applications
- They need explicit sharing just like regular users
- They don't receive email notifications
- They're perfect for automated systems like this

---

**Questions?** Check the main README.md or TROUBLESHOOTING.md

