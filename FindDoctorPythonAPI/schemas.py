from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date, time
from typing import Optional, List

# ==================== EDIT SUGGESTIONS ====================

class EditSuggestionCreate(BaseModel):
    establishment_id: str
    establishment_name: str
    field: str
    current_value: Optional[str] = None
    suggested_value: str
    submitted_by: str

class EditSuggestionResponse(BaseModel):
    id: int
    establishment_id: str
    establishment_name: str
    field: str
    current_value: Optional[str]
    suggested_value: str
    submitted_by: str
    submitted_at: datetime
    status: str
    
    class Config:
        from_attributes = True

# ==================== DOCTORS ====================

class DoctorCreate(BaseModel):
    co_profissional: str
    name: str
    specialty: Optional[str] = None
    crm: Optional[str] = None
    establishment_id: str
    establishment_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True

class DoctorResponse(BaseModel):
    id: int
    co_profissional: str
    name: str
    specialty: Optional[str]
    crm: Optional[str]
    establishment_id: str
    establishment_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== DOCTOR AVAILABILITY ====================

class DoctorAvailabilityCreate(BaseModel):
    doctor_id: int
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    start_time: time
    end_time: time
    is_available: bool = True

class DoctorAvailabilityResponse(BaseModel):
    id: int
    doctor_id: int
    day_of_week: int
    start_time: time
    end_time: time
    is_available: bool
    
    class Config:
        from_attributes = True

# ==================== APPOINTMENTS ====================

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_name: str
    patient_email: EmailStr
    patient_phone: str
    appointment_date: date
    appointment_time: time
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    status: str = Field(..., pattern="^(scheduled|confirmed|cancelled|completed)$")

class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_name: str
    patient_email: str
    patient_phone: str
    appointment_date: date
    appointment_time: time
    notes: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AppointmentWithDoctorResponse(AppointmentResponse):
    doctor: DoctorResponse

# ==================== EXTERNAL API RESPONSES ====================

class EstablishmentFromCSharp(BaseModel):
    """Response do backend C# para estabelecimentos"""
    codigoCNES: str
    nome: str
    cnpj: Optional[str] = None
    endereco: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    latitude: float
    longitude: float
    telefone: Optional[str] = None
    profissionais: Optional[List[dict]] = []

class SpecialtyFromCSharp(BaseModel):
    """Response do backend C# para especialidades"""
    id: str
    nome: str
