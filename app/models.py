"""Pydantic models for contract form data."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class ContractFormData(BaseModel):
    """Model for contract form submission data."""
    
    # Contract metadata
    no: str = Field(..., description="Contract number")
    date: str = Field(..., description="Contract date")
    
    # Contact person (parent/guardian/student)
    contact_first_name: str = Field(..., min_length=1, description="Contact first name")
    contact_last_name: str = Field(..., min_length=1, description="Contact last name")
    contact_address: str = Field(..., min_length=1, description="Contact address")
    contact_phone: str = Field(..., min_length=1, description="Contact phone number")
    contact_email: EmailStr = Field(..., description="Contact email")
    contact_id_series: str = Field(..., description="ID series (CI/BI/Passport)")
    contact_id_no: str = Field(..., description="ID number")
    contact_personal_no: str = Field(..., description="CNP (Personal numeric code)")
    
    # Emergency contact
    contact_emergency_first_name: str = Field(..., description="Emergency contact first name")
    contact_emergency_last_name: str = Field(..., description="Emergency contact last name")
    contact_emergency_phone_no: str = Field(..., description="Emergency contact phone")
    
    # Student information
    student_first_name: str = Field(..., description="Student first name")
    student_last_name: str = Field(..., description="Student last name")
    student_birth_date: str = Field(..., description="Student birth date")
    
    # For students under 14 years old
    if_14_student_first_name: Optional[str] = Field(default="", description="Student first name if under 14")
    if_14_student_last_name: Optional[str] = Field(default="", description="Student last name if under 14")
    if_14_date: Optional[str] = Field(default="", description="Date for under 14 clause")
    
    # Course details
    subscriptions_types: str = Field(..., description="Subscription types/modules")
    timeslots: str = Field(..., description="Course timeslots")
    
    class Config:
        json_schema_extra = {
            "example": {
                "no": "001",
                "date": "2024-01-15",
                "contact_first_name": "Ion",
                "contact_last_name": "Popescu",
                "contact_address": "Str. Exemplu nr. 10, București",
                "contact_phone": "0721234567",
                "contact_email": "ion.popescu@example.com",
                "contact_id_series": "AB",
                "contact_id_no": "123456",
                "contact_personal_no": "1234567890123",
                "contact_emergency_first_name": "Maria",
                "contact_emergency_last_name": "Popescu",
                "contact_emergency_phone_no": "0721234568",
                "student_first_name": "Andrei",
                "student_last_name": "Popescu",
                "student_birth_date": "2015-05-20",
                "subscriptions_types": "Robotică nivel 1",
                "timeslots": "Luni 16:00-18:00"
            }
        }

