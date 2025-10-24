"""Email service using Gmail API with OAuth2."""
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class EmailService:
    """Handle email sending via Gmail API with OAuth2 authentication."""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        """Initialize email service with OAuth2 credentials.
        
        Args:
            client_id: Gmail API client ID
            client_secret: Gmail API client secret
            refresh_token: OAuth2 refresh token
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.service = None
        
        if client_id and client_secret and refresh_token:
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API using OAuth2."""
        try:
            # Create credentials from refresh token
            credentials = Credentials(
                token=None,
                refresh_token=self.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.SCOPES
            )
            
            # Refresh the token
            credentials.refresh(Request())
            
            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=credentials)
            
        except Exception as e:
            print(f"Error authenticating with Gmail API: {e}")
            self.service = None
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body_html: str,
        body_text: str = "",
        cc_emails: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Send an email with optional attachments.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML body content
            body_text: Plain text body content (fallback)
            cc_emails: List of CC email addresses
            attachments: List of file paths to attach
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.service:
            print("Error: Email service not authenticated")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['To'] = to_email
            message['Subject'] = subject
            
            if cc_emails:
                message['Cc'] = ', '.join(cc_emails)
            
            # Add text and HTML parts
            if body_text:
                part_text = MIMEText(body_text, 'plain', 'utf-8')
                message.attach(part_text)
            
            part_html = MIMEText(body_html, 'html', 'utf-8')
            message.attach(part_html)
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if Path(file_path).exists():
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        
                        attachment = MIMEApplication(file_data)
                        attachment.add_header(
                            'Content-Disposition',
                            'attachment',
                            filename=Path(file_path).name
                        )
                        message.attach(attachment)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"Email sent successfully. Message ID: {send_message['id']}")
            return True
            
        except HttpError as error:
            print(f"An error occurred sending email: {error}")
            return False
        except Exception as e:
            print(f"Unexpected error sending email: {e}")
            return False
    
    def send_contract_email(
        self,
        client_email: str,
        client_name: str,
        student_name: str,
        contract_pdf_path: str,
        admin_email: str
    ) -> bool:
        """Send contract email to client and admin.
        
        Args:
            client_email: Client's email address
            client_name: Client's full name
            student_name: Student's full name
            contract_pdf_path: Path to generated contract PDF
            admin_email: Admin email for CC
            
        Returns:
            True if email sent successfully
        """
        subject = f"Contract de Prestări Servicii - {student_name}"
        
        # HTML email body
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    border-radius: 0 0 5px 5px;
                }}
                .footer {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Early Alpha Engineering S.R.L.</h1>
                </div>
                <div class="content">
                    <p>Bună ziua, {client_name},</p>
                    
                    <p>Vă mulțumim pentru înscrierea la cursurile de robotică!</p>
                    
                    <p>Atașat acestui email veți găsi contractul de prestări servicii pentru <strong>{student_name}</strong>.</p>
                    
                    <p>Vă rugăm să păstrați o copie a acestui document pentru evidența dumneavoastră.</p>
                    
                    <p>Dacă aveți întrebări sau aveți nevoie de clarificări, nu ezitați să ne contactați.</p>
                    
                    <p>Vă mulțumim,<br>
                    <strong>Echipa Early Alpha Engineering</strong></p>
                    
                    <div class="footer">
                        <p>Early Alpha Engineering S.R.L.<br>
                        Călărași, județul Călărași, str. Stadionului 40 Bis<br>
                        Email: info@earlyalpha.ro<br>
                        CUI: 49100118</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        body_text = f"""
        Bună ziua, {client_name},
        
        Vă mulțumim pentru înscrierea la cursurile de robotică!
        
        Atașat acestui email veți găsi contractul de prestări servicii pentru {student_name}.
        
        Vă rugăm să păstrați o copie a acestui document pentru evidența dumneavoastră.
        
        Dacă aveți întrebări sau aveți nevoie de clarificări, nu ezitați să ne contactați.
        
        Vă mulțumim,
        Echipa Early Alpha Engineering
        
        ---
        Early Alpha Engineering S.R.L.
        Călărași, județul Călărași, str. Stadionului 40 Bis
        Email: info@earlyalpha.ro
        CUI: 49100118
        """
        
        return self.send_email(
            to_email=client_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
            cc_emails=[admin_email] if admin_email else None,
            attachments=[contract_pdf_path] if Path(contract_pdf_path).exists() else None
        )

