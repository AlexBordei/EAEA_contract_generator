"""Helper script to setup Gmail OAuth2 credentials."""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_credentials():
    """Get Gmail OAuth2 credentials interactively."""
    print("=" * 60)
    print("Gmail OAuth2 Setup - Similar to n8n")
    print("=" * 60)
    print()
    print("This script will help you get your Gmail OAuth2 credentials.")
    print()
    print("Prerequisites:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable Gmail API")
    print("4. Create OAuth 2.0 Client ID credentials (Desktop app)")
    print("5. Download the credentials JSON file")
    print()
    
    # Ask for credentials file
    creds_file = input("Enter path to your OAuth2 credentials JSON file: ").strip()
    
    if not os.path.exists(creds_file):
        print(f"\nError: File not found: {creds_file}")
        return
    
    try:
        # Create flow
        flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
        
        # Run local server for OAuth flow
        print("\n🔐 Opening browser for authentication...")
        print("Please log in with your Gmail account and authorize the application.")
        creds = flow.run_local_server(port=0)
        
        print("\n✅ Successfully authenticated!")
        print("\n" + "=" * 60)
        print("Add these to your .env file:")
        print("=" * 60)
        print()
        print(f"GMAIL_CLIENT_ID={creds.client_id}")
        print(f"GMAIL_CLIENT_SECRET={creds.client_secret}")
        print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
        print()
        print("=" * 60)
        
        # Offer to create .env file
        create_env = input("\nDo you want to create/update .env file automatically? (y/n): ").strip().lower()
        
        if create_env == 'y':
            env_content = f"""# Gmail API OAuth2 Credentials
GMAIL_CLIENT_ID={creds.client_id}
GMAIL_CLIENT_SECRET={creds.client_secret}
GMAIL_REFRESH_TOKEN={creds.refresh_token}

# Admin Email
ADMIN_EMAIL=your_email@example.com

# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials/google_sheets_key.json

# Contract Configuration
CONTRACT_PDF_PATH=crm.eaea.ro Draft - Contract prestari servicii Early Alpha.docx (1).pdf
OUTPUT_FOLDER=output

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
"""
            with open('.env', 'w') as f:
                f.write(env_content)
            
            print("\n✅ .env file created successfully!")
            print("⚠️  Don't forget to update ADMIN_EMAIL and GOOGLE_SHEETS_SPREADSHEET_ID")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you've enabled the Gmail API in Google Cloud Console")
        print("2. Verify your OAuth2 credentials are for a Desktop application")
        print("3. Check that redirect URIs include http://localhost")


if __name__ == "__main__":
    get_gmail_credentials()

