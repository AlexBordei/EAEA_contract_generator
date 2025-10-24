"""Google Sheets integration service."""
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path


class SheetsService:
    """Handle Google Sheets operations for logging contract submissions."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        """Initialize Google Sheets service.
        
        Args:
            credentials_file: Path to service account JSON credentials
            spreadsheet_id: ID of the Google Spreadsheet
        """
        self.spreadsheet_id = spreadsheet_id
        self.credentials_file = credentials_file
        self.client = None
        self.spreadsheet = None
        
        if Path(credentials_file).exists():
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API using service account."""
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.SCOPES
            )
            self.client = gspread.authorize(credentials)
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            print(f"✅ Google Sheets connected: {self.spreadsheet.title}")
        except Exception as e:
            print(f"❌ Could not connect to Google Sheets: {e}")
            print(f"📧 Service account: {credentials.service_account_email if 'credentials' in locals() else 'N/A'}")
            print(f"📊 Spreadsheet ID: {self.spreadsheet_id}")
            print(f"⚠️  Make sure the service account has access to the spreadsheet!")
            print(f"   Run: ./setup_sheets.sh for instructions")
            self.client = None
            self.spreadsheet = None
    
    def ensure_headers(self, worksheet_name: str = "Sheet1"):
        """Ensure the worksheet has proper headers."""
        if not self.spreadsheet:
            return
        
        try:
            worksheet = self.spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = self.spreadsheet.add_worksheet(
                title=worksheet_name,
                rows=1000,
                cols=25
            )
        
        # Define headers
        headers = [
            "Timestamp",
            "Contract No",
            "Contract Date",
            "Contact First Name",
            "Contact Last Name",
            "Contact Address",
            "Contact Phone",
            "Contact Email",
            "Contact ID Series",
            "Contact ID No",
            "Contact CNP",
            "Emergency Contact First Name",
            "Emergency Contact Last Name",
            "Emergency Contact Phone",
            "Student First Name",
            "Student Last Name",
            "Student Birth Date",
            "If Under 14 First Name",
            "If Under 14 Last Name",
            "If Under 14 Date",
            "Subscription Types",
            "Timeslots",
            "PDF Generated",
            "Email Sent"
        ]
        
        # Check if headers exist
        try:
            existing_headers = worksheet.row_values(1)
            if not existing_headers or existing_headers[0] != "Timestamp":
                worksheet.insert_row(headers, 1)
        except:
            worksheet.insert_row(headers, 1)
    
    def append_submission(self, data: Dict[str, Any]) -> bool:
        """Append a new contract submission to the spreadsheet.
        
        Args:
            data: Dictionary containing form data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.spreadsheet:
            print("❌ Spreadsheet not connected - cannot save to Google Sheets")
            print("   Run: ./setup_sheets.sh to fix this issue")
            return False
        
        try:
            worksheet = self.spreadsheet.worksheet("Sheet1")
            
            # Prepare row data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            row = [
                timestamp,
                data.get("no", ""),
                data.get("date", ""),
                data.get("contact_first_name", ""),
                data.get("contact_last_name", ""),
                data.get("contact_address", ""),
                data.get("contact_phone", ""),
                data.get("contact_email", ""),
                data.get("contact_id_series", ""),
                data.get("contact_id_no", ""),
                data.get("contact_personal_no", ""),
                data.get("contact_emergency_first_name", ""),
                data.get("contact_emergency_last_name", ""),
                data.get("contact_emergency_phone_no", ""),
                data.get("student_first_name", ""),
                data.get("student_last_name", ""),
                data.get("student_birth_date", ""),
                data.get("if_14_student_first_name", ""),
                data.get("if_14_student_last_name", ""),
                data.get("if_14_date", ""),
                data.get("subscriptions_types", ""),
                data.get("timeslots", ""),
                "Yes",
                "Pending"
            ]
            
            worksheet.append_row(row)
            print(f"✅ Saved to Google Sheets: {data.get('student_first_name')} {data.get('student_last_name')}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving to Google Sheets: {e}")
            return False
    
    def update_email_status(self, row_number: int, status: str = "Sent"):
        """Update the email status for a specific row.
        
        Args:
            row_number: Row number in the spreadsheet
            status: Email status (Sent, Failed, etc.)
        """
        if not self.spreadsheet:
            return
        
        try:
            worksheet = self.spreadsheet.worksheet("Sheet1")
            worksheet.update_cell(row_number, 24, status)  # Column 24 is "Email Sent"
        except Exception as e:
            print(f"Error updating email status: {e}")
    
    def get_next_contract_number(self) -> str:
        """Get the next contract number based on last entry in spreadsheet.
        
        Returns:
            Next contract number in format XXX/YYYY (e.g., "001/2025")
        """
        if not self.spreadsheet:
            # If not connected, return default
            from datetime import datetime
            year = datetime.now().year
            return f"001/{year}"
        
        try:
            worksheet = self.spreadsheet.worksheet("Sheet1")
            
            # Get all contract numbers (column 2 - "Contract No")
            contract_numbers = worksheet.col_values(2)
            
            # Remove header
            if contract_numbers and contract_numbers[0] == "Contract No":
                contract_numbers = contract_numbers[1:]
            
            # Get current year
            from datetime import datetime
            current_year = datetime.now().year
            
            # Filter contracts from current year and extract numbers
            current_year_numbers = []
            for contract_no in contract_numbers:
                if contract_no and '/' in contract_no:
                    try:
                        num_part, year_part = contract_no.split('/')
                        if int(year_part) == current_year:
                            # Extract numeric part (handle formats like 001, 1, etc.)
                            num = int(num_part)
                            current_year_numbers.append(num)
                    except (ValueError, IndexError):
                        continue
            
            # Get the highest number and add 1
            if current_year_numbers:
                next_number = max(current_year_numbers) + 1
            else:
                next_number = 1
            
            # Format as XXX/YYYY
            return f"{next_number:03d}/{current_year}"
            
        except Exception as e:
            print(f"Error getting next contract number: {e}")
            from datetime import datetime
            year = datetime.now().year
            return f"001/{year}"

