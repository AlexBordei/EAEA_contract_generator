#!/usr/bin/env python3
"""
Local testing script for PDF placeholder replacement.
This script tests the PDF generation with sample data.
"""

from app.pdf_handler import PDFHandler
from datetime import datetime
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    """Print formatted header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    """Print info message."""
    print(f"{YELLOW}ℹ {text}{RESET}")

# Test data
test_data = {
    "no": "TEST-001/2025",
    "date": "24.10.2025",
    "contact_first_name": "Ion",
    "contact_last_name": "Popescu",
    "contact_address": "Str. Exemplu nr. 123, Sector 1, București",
    "contact_phone": "+40 712 345 678",
    "contact_email": "ion.popescu@example.com",
    "contact_id_series": "RO",
    "contact_id_no": "123456",
    "contact_personal_no": "1234567890123",
    "contact_emergency_first_name": "Maria",
    "contact_emergency_last_name": "Popescu",
    "contact_emergency_phone_no": "+40 712 345 679",
    "student_first_name": "Mihai",
    "student_last_name": "Popescu",
    "student_birth_date": "15.03.2015",
    "if_14_student_first_name": "",
    "if_14_student_last_name": "",
    "if_14_date": "",
    "subscriptions_types": "Robotică Avansată\nProgramare Python\nElectronică și IoT",
    "timeslots": "Marți: 17:00-18:30\nJoi: 17:00-18:30\nSâmbătă: 10:00-12:00"
}

def main():
    """Main testing function."""
    print_header("PDF REPLACEMENT TEST")
    
    # Step 1: Check if template exists
    template_path = "crm.eaea.ro Draft - Contract prestari servicii Early Alpha.docx (1).pdf"
    
    if not Path(template_path).exists():
        print_error(f"Template PDF not found: {template_path}")
        return False
    
    print_success(f"Template PDF found: {template_path}")
    
    # Step 2: Initialize PDF handler
    print_info("Initializing PDF handler...")
    try:
        pdf_handler = PDFHandler(template_path)
        print_success("PDF handler initialized")
    except Exception as e:
        print_error(f"Failed to initialize PDF handler: {e}")
        return False
    
    # Step 3: Extract placeholders from template
    print_info("Extracting placeholders from template...")
    try:
        placeholders = pdf_handler.get_placeholders_from_pdf(template_path)
        print_success(f"Found {len(placeholders)} placeholders in template")
        print("\nPlaceholders found:")
        for i, placeholder in enumerate(placeholders, 1):
            print(f"  {i:2d}. {{{placeholder}}}")
    except Exception as e:
        print_error(f"Failed to extract placeholders: {e}")
        return False
    
    # Step 4: Generate test PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"output/TEST_contract_{timestamp}.pdf"
    
    print_header("GENERATING PDF")
    print_info(f"Output path: {output_path}")
    print_info(f"Data fields: {len(test_data)}")
    
    try:
        result_path = pdf_handler.generate_pdf(test_data, output_path)
        print_success(f"PDF generated successfully!")
        print_success(f"Output file: {result_path}")
    except Exception as e:
        print_error(f"Failed to generate PDF: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 5: Verify output exists
    if Path(result_path).exists():
        file_size = Path(result_path).stat().st_size
        print_success(f"Output file exists ({file_size:,} bytes)")
    else:
        print_error("Output file was not created!")
        return False
    
    # Step 6: Check for remaining placeholders in output
    print_header("VERIFICATION")
    print_info("Checking for remaining placeholders in generated PDF...")
    
    try:
        remaining = pdf_handler.get_placeholders_from_pdf(result_path)
        
        if remaining:
            print_error(f"Found {len(remaining)} unreplaced placeholders:")
            for placeholder in remaining:
                print(f"  - {{{placeholder}}}")
            return False
        else:
            print_success("No placeholders remain - all were replaced!")
    except Exception as e:
        print_error(f"Could not verify output: {e}")
        return False
    
    # Success!
    print_header("TEST COMPLETE")
    print_success("All tests passed! ✓")
    print_success(f"Open the PDF to verify: {result_path}")
    print(f"\n{YELLOW}Next steps:{RESET}")
    print(f"  1. Open: {result_path}")
    print(f"  2. Search for '{{' to verify no placeholders remain")
    print(f"  3. Verify all data is visible and correct")
    print(f"  4. Check formatting is preserved\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test interrupted by user{RESET}")
        exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

