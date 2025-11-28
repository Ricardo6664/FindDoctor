from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class EditSuggestion(Base):
    """Sugestões de edição para estabelecimentos"""
    __tablename__ = "edit_suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    establishment_id = Column(String(50), nullable=False, index=True)  # CNES do estabelecimento
    establishment_name = Column(String(255), nullable=False)
    field = Column(String(100), nullable=False)  # Campo que foi editado (ex: "telefone", "endereco")
    current_value = Column(Text)
    suggested_value = Column(Text, nullable=False)
    submitted_by = Column(String(255), nullable=False)  # Nome ou email de quem sugeriu
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(20), default="pending", nullable=False)  # pending, approved, rejected
    
    def __repr__(self):
        return f"<EditSuggestion {self.id} - {self.establishment_name}>"


class Doctor(Base):
    """Médicos cadastrados para agendamento"""
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    co_profissional = Column(String(50), unique=True, nullable=False, index=True)  # ID do profissional do CNES
    name = Column(String(255), nullable=False)
    specialty = Column(String(255))
    crm = Column(String(50))  # Número do CRM (opcional)
    establishment_id = Column(String(50), nullable=False)  # CNES do estabelecimento
    establishment_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    availabilities = relationship("DoctorAvailability", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Doctor {self.id} - {self.name}>"


class DoctorAvailability(Base):
    """Disponibilidade de horários dos médicos"""
    __tablename__ = "doctor_availabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0=Segunda, 6=Domingo
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Relacionamento
    doctor = relationship("Doctor", back_populates="availabilities")
    
    def __repr__(self):
        return f"<DoctorAvailability {self.id} - Doctor {self.doctor_id}>"


class Appointment(Base):
    """Agendamentos de consultas"""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    
    # Dados do paciente
    patient_name = Column(String(255), nullable=False)
    patient_email = Column(String(255), nullable=False)
    patient_phone = Column(String(50), nullable=False)
    
    # Dados da consulta
    appointment_date = Column(Date, nullable=False, index=True)
    appointment_time = Column(Time, nullable=False)
    notes = Column(Text)
    
    # Status
    status = Column(String(20), default="scheduled", nullable=False)  # scheduled, confirmed, cancelled, completed
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    doctor = relationship("Doctor", back_populates="appointments")
    
    def __repr__(self):
        return f"<Appointment {self.id} - {self.patient_name}>"
