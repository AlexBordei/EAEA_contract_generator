"""Configuration settings for the application."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gmail API OAuth2 Credentials
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_refresh_token: str = ""
    
    # Admin Email
    admin_email: str = ""
    
    # Google Sheets Configuration
    google_sheets_spreadsheet_id: str = ""
    google_sheets_credentials_file: str = "credentials/google_sheets_key.json"
    
    # Contract Configuration
    contract_pdf_path: str = "crm.eaea.ro Draft - Contract prestari servicii Early Alpha.docx (1).pdf"
    output_folder: str = "output"
    
    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()

