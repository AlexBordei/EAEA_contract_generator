"""Test script to verify the application setup."""
import sys
from pathlib import Path


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import fastapi
        print("  ✓ FastAPI")
    except ImportError:
        print("  ✗ FastAPI - Run: pip install fastapi")
        return False
    
    try:
        import uvicorn
        print("  ✓ Uvicorn")
    except ImportError:
        print("  ✗ Uvicorn - Run: pip install uvicorn")
        return False
    
    try:
        import PyPDF2
        print("  ✓ PyPDF2")
    except ImportError:
        print("  ✗ PyPDF2 - Run: pip install PyPDF2")
        return False
    
    try:
        import reportlab
        print("  ✓ ReportLab")
    except ImportError:
        print("  ✗ ReportLab - Run: pip install reportlab")
        return False
    
    try:
        import gspread
        print("  ✓ gspread")
    except ImportError:
        print("  ✗ gspread - Run: pip install gspread")
        return False
    
    try:
        from google.oauth2.credentials import Credentials
        print("  ✓ Google Auth")
    except ImportError:
        print("  ✗ Google Auth - Run: pip install google-auth google-auth-oauthlib")
        return False
    
    try:
        from googleapiclient.discovery import build
        print("  ✓ Google API Client")
    except ImportError:
        print("  ✗ Google API Client - Run: pip install google-api-python-client")
        return False
    
    return True


def test_file_structure():
    """Test that required files and directories exist."""
    print("\nTesting file structure...")
    
    required_files = [
        "app/main.py",
        "app/models.py",
        "app/config.py",
        "app/pdf_handler.py",
        "app/email_service.py",
        "app/sheets_service.py",
        "app/templates/form.html",
        "requirements.txt",
        "README.md"
    ]
    
    required_dirs = [
        "app",
        "app/templates",
        "static",
        "credentials",
        "output"
    ]
    
    all_ok = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - Missing")
            all_ok = False
    
    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ - Missing")
            all_ok = False
    
    return all_ok


def test_config():
    """Test configuration."""
    print("\nTesting configuration...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("  ✓ .env file exists")
        
        # Check for required variables
        with open(env_file, 'r') as f:
            content = f.read()
            
        required_vars = [
            "GMAIL_CLIENT_ID",
            "GMAIL_CLIENT_SECRET",
            "GMAIL_REFRESH_TOKEN",
            "ADMIN_EMAIL",
            "GOOGLE_SHEETS_SPREADSHEET_ID"
        ]
        
        for var in required_vars:
            if var in content and "your_" not in content.split(var)[1].split('\n')[0]:
                print(f"  ✓ {var} is set")
            else:
                print(f"  ⚠  {var} needs to be configured")
    else:
        print("  ✗ .env file not found")
        print("     Run: python3 setup_gmail_oauth.py")
        return False
    
    # Check template PDF
    pdf_path = Path("crm.eaea.ro Draft - Contract prestari servicii Early Alpha.docx (1).pdf")
    if pdf_path.exists():
        print("  ✓ Contract template PDF exists")
    else:
        print("  ⚠  Contract template PDF not found")
    
    # Check Google Sheets credentials
    sheets_creds = Path("credentials/google_sheets_key.json")
    if sheets_creds.exists():
        print("  ✓ Google Sheets credentials exist")
    else:
        print("  ⚠  Google Sheets credentials not found")
        print("     Add credentials/google_sheets_key.json")
    
    return True


def test_app_startup():
    """Test that the app can be imported."""
    print("\nTesting application startup...")
    
    try:
        from app.main import app
        print("  ✓ Application can be imported")
        return True
    except Exception as e:
        print(f"  ✗ Application import failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Contract Automation System - Setup Test")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("File Structure", test_file_structure()))
    results.append(("Configuration", test_config()))
    results.append(("App Startup", test_app_startup()))
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        print("\nYou can now run the application:")
        print("  ./run.sh")
        print("  or")
        print("  python3 -m uvicorn app.main:app --reload")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nQuick fixes:")
        print("  1. Install dependencies: pip3 install -r requirements.txt")
        print("  2. Setup Gmail OAuth: python3 setup_gmail_oauth.py")
        print("  3. Add Google Sheets credentials to credentials/")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

