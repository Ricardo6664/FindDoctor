from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Doctor, DoctorAvailability
from schemas import (
    DoctorCreate, 
    DoctorResponse, 
    DoctorAvailabilityCreate,
    DoctorAvailabilityResponse
)

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# ==================== DOCTORS ====================

@router.post("/", response_model=DoctorResponse, status_code=201)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    """Cadastra um novo médico"""
    # Verifica se já existe
    existing = db.query(Doctor).filter(Doctor.co_profissional == doctor.co_profissional).first()
    if existing:
        raise HTTPException(status_code=400, detail="Médico já cadastrado")
    
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.get("/", response_model=List[DoctorResponse])
def list_doctors(
    establishment_id: Optional[str] = Query(None, description="Filtrar por CNES do estabelecimento"),
    specialty: Optional[str] = Query(None, description="Filtrar por especialidade"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos os médicos cadastrados"""
    query = db.query(Doctor)
    
    if establishment_id:
        query = query.filter(Doctor.establishment_id == establishment_id)
    if specialty:
        query = query.filter(Doctor.specialty.ilike(f"%{specialty}%"))
    
    doctors = query.offset(skip).limit(limit).all()
    return doctors

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """Busca um médico por ID"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return doctor

@router.delete("/{doctor_id}", status_code=204)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """Remove um médico"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db.delete(doctor)
    db.commit()
    return None

# ==================== DOCTOR AVAILABILITY ====================

@router.post("/{doctor_id}/availability", response_model=DoctorAvailabilityResponse, status_code=201)
def create_doctor_availability(
    doctor_id: int,
    availability: DoctorAvailabilityCreate,
    db: Session = Depends(get_db)
):
    """Adiciona disponibilidade de horário para um médico"""
    # Verifica se o médico existe
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    # Verifica se já existe disponibilidade para esse dia/horário
    existing = db.query(DoctorAvailability).filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.day_of_week == availability.day_of_week,
        DoctorAvailability.start_time == availability.start_time
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Já existe disponibilidade para este horário")
    
    db_availability = DoctorAvailability(doctor_id=doctor_id, **availability.model_dump(exclude={"doctor_id"}))
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

@router.get("/{doctor_id}/availability", response_model=List[DoctorAvailabilityResponse])
def list_doctor_availability(
    doctor_id: int,
    day_of_week: Optional[int] = Query(None, ge=0, le=6, description="0=Monday, 6=Sunday"),
    db: Session = Depends(get_db)
):
    """Lista disponibilidade de um médico"""
    query = db.query(DoctorAvailability).filter(DoctorAvailability.doctor_id == doctor_id)
    
    if day_of_week is not None:
        query = query.filter(DoctorAvailability.day_of_week == day_of_week)
    
    availabilities = query.order_by(DoctorAvailability.day_of_week, DoctorAvailability.start_time).all()
    return availabilities

@router.delete("/availability/{availability_id}", status_code=204)
def delete_doctor_availability(
    availability_id: int,
    db: Session = Depends(get_db)
):
    """Remove uma disponibilidade"""
    availability = db.query(DoctorAvailability).filter(DoctorAvailability.id == availability_id).first()
    if not availability:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada")
    
    db.delete(availability)
    db.commit()
    return None
