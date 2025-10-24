"""FastAPI application for contract automation."""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime
import json

from .config import settings
from .models import ContractFormData
from .pdf_handler import PDFHandler
from .email_service import EmailService
from .sheets_service import SheetsService


# Initialize FastAPI app
app = FastAPI(
    title="Contract Automation System",
    description="Automated contract generation and management",
    version="1.0.0"
)

# Mount static files
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Setup templates
templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))

# Initialize services
pdf_handler = PDFHandler(settings.contract_pdf_path)
email_service = EmailService(
    settings.gmail_client_id,
    settings.gmail_client_secret,
    settings.gmail_refresh_token
)
sheets_service = SheetsService(
    settings.google_sheets_credentials_file,
    settings.google_sheets_spreadsheet_id
)

# Ensure Google Sheets has headers
try:
    sheets_service.ensure_headers()
except Exception as e:
    print(f"Warning: Could not initialize Google Sheets headers: {e}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the contract form page."""
    # Load placeholders
    placeholders_file = Path("placeholders.json")
    if placeholders_file.exists():
        with open(placeholders_file, 'r', encoding='utf-8') as f:
            placeholders = json.load(f)
    else:
        placeholders = PDFHandler.get_placeholders_from_pdf(settings.contract_pdf_path)
    
    return templates.TemplateResponse(
        "form.html",
        {
            "request": request,
            "placeholders": placeholders
        }
    )


@app.post("/submit-contract")
async def submit_contract(
    no: str = Form(...),
    date: str = Form(...),
    contact_first_name: str = Form(...),
    contact_last_name: str = Form(...),
    contact_address: str = Form(...),
    contact_phone: str = Form(...),
    contact_email: str = Form(...),
    contact_id_series: str = Form(...),
    contact_id_no: str = Form(...),
    contact_personal_no: str = Form(...),
    contact_emergency_first_name: str = Form(...),
    contact_emergency_last_name: str = Form(...),
    contact_emergency_phone_no: str = Form(...),
    student_first_name: str = Form(...),
    student_last_name: str = Form(...),
    student_birth_date: str = Form(...),
    if_14_student_first_name: str = Form(""),
    if_14_student_last_name: str = Form(""),
    if_14_date: str = Form(""),
    subscriptions_types: str = Form(...),
    timeslots: str = Form(...),
):
    """Handle contract form submission."""
    try:
        # Create form data model
        form_data = ContractFormData(
            no=no,
            date=date,
            contact_first_name=contact_first_name,
            contact_last_name=contact_last_name,
            contact_address=contact_address,
            contact_phone=contact_phone,
            contact_email=contact_email,
            contact_id_series=contact_id_series,
            contact_id_no=contact_id_no,
            contact_personal_no=contact_personal_no,
            contact_emergency_first_name=contact_emergency_first_name,
            contact_emergency_last_name=contact_emergency_last_name,
            contact_emergency_phone_no=contact_emergency_phone_no,
            student_first_name=student_first_name,
            student_last_name=student_last_name,
            student_birth_date=student_birth_date,
            if_14_student_first_name=if_14_student_first_name,
            if_14_student_last_name=if_14_student_last_name,
            if_14_date=if_14_date,
            subscriptions_types=subscriptions_types,
            timeslots=timeslots,
        )
        
        # Convert to dict for processing
        data_dict = form_data.model_dump()
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"contract_{student_last_name}_{student_first_name}_{timestamp}.pdf"
        output_path = Path(settings.output_folder) / output_filename
        
        # Generate PDF
        pdf_path = pdf_handler.generate_pdf(data_dict, str(output_path))
        
        # Save to Google Sheets
        sheets_success = sheets_service.append_submission(data_dict)
        
        # Send email
        email_success = email_service.send_contract_email(
            client_email=contact_email,
            client_name=f"{contact_first_name} {contact_last_name}",
            student_name=f"{student_first_name} {student_last_name}",
            contract_pdf_path=pdf_path,
            admin_email=settings.admin_email
        )
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Contract generat și trimis cu succes!",
                "pdf_generated": True,
                "sheets_saved": sheets_success,
                "email_sent": email_success,
                "pdf_path": str(output_path)
            },
            status_code=200
        )
        
    except Exception as e:
        print(f"Error processing contract: {e}")
        return JSONResponse(
            content={
                "success": False,
                "message": f"Eroare la procesarea contractului: {str(e)}"
            },
            status_code=500
        )


@app.get("/api/next-contract-number")
async def get_next_contract_number():
    """Get the next contract number based on Google Sheets."""
    try:
        next_number = sheets_service.get_next_contract_number()
        return {
            "success": True,
            "contract_number": next_number
        }
    except Exception as e:
        # Fallback to default if error
        from datetime import datetime
        year = datetime.now().year
        return {
            "success": False,
            "contract_number": f"001/{year}",
            "message": f"Using default number: {str(e)}"
        }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "gmail_configured": bool(settings.gmail_client_id and settings.gmail_refresh_token),
        "sheets_configured": bool(settings.google_sheets_spreadsheet_id),
        "pdf_template_exists": Path(settings.contract_pdf_path).exists()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True
    )

