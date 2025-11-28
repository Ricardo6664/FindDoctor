from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date, datetime
from database import get_db
from models import Appointment, Doctor
from schemas import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentWithDoctorResponse
)

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo agendamento"""
    # Verifica se o médico existe
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    # Verifica se já existe agendamento para este horário
    existing = db.query(Appointment).filter(
        and_(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_date == appointment.appointment_date,
            Appointment.appointment_time == appointment.appointment_time,
            Appointment.status.in_(["scheduled", "confirmed"])
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Já existe agendamento para este horário")
    
    # Verifica se a data não é no passado
    if appointment.appointment_date < date.today():
        raise HTTPException(status_code=400, detail="Não é possível agendar para datas passadas")
    
    db_appointment = Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/", response_model=List[AppointmentWithDoctorResponse])
def list_appointments(
    doctor_id: Optional[int] = Query(None, description="Filtrar por médico"),
    appointment_date: Optional[date] = Query(None, description="Filtrar por data"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    patient_email: Optional[str] = Query(None, description="Filtrar por email do paciente"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista agendamentos com filtros opcionais"""
    query = db.query(Appointment)
    
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if appointment_date:
        query = query.filter(Appointment.appointment_date == appointment_date)
    if status:
        query = query.filter(Appointment.status == status)
    if patient_email:
        query = query.filter(Appointment.patient_email == patient_email)
    
    appointments = query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).offset(skip).limit(limit).all()
    
    return appointments

@router.get("/{appointment_id}", response_model=AppointmentWithDoctorResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Busca um agendamento por ID"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return appointment

@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment_status(
    appointment_id: int,
    update: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza o status de um agendamento"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    appointment.status = update.status
    appointment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(appointment)
    return appointment

@router.delete("/{appointment_id}", status_code=204)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Cancela um agendamento (muda status para cancelled)"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    appointment.status = "cancelled"
    appointment.updated_at = datetime.utcnow()
    
    db.commit()
    return None

@router.get("/doctor/{doctor_id}/dashboard", response_model=List[AppointmentResponse])
def get_doctor_dashboard(
    doctor_id: int,
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final"),
    db: Session = Depends(get_db)
):
    """Dashboard do médico - Lista agendamentos do médico"""
    # Verifica se o médico existe
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    query = db.query(Appointment).filter(Appointment.doctor_id == doctor_id)
    
    if start_date:
        query = query.filter(Appointment.appointment_date >= start_date)
    if end_date:
        query = query.filter(Appointment.appointment_date <= end_date)
    
    appointments = query.order_by(
        Appointment.appointment_date,
        Appointment.appointment_time
    ).all()
    
    return appointments
