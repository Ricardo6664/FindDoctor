"""
Script para popular o banco de dados com dados de exemplo
Execute após iniciar a API pela primeira vez
"""
import requests
import json
from datetime import date, time, datetime, timedelta

API_BASE_URL = "http://localhost:8000/api"

def check_api():
    """Verifica se a API está rodando"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def populate_edit_suggestions():
    """Popula sugestões de edição"""
    print("\n📝 Criando sugestões de edição...")
    
    suggestions = [
        {
            "establishment_id": "2345678",
            "establishment_name": "Clínica São Lucas",
            "field": "telefone",
            "current_value": "(11) 3000-0000",
            "suggested_value": "(11) 3000-0001",
            "submitted_by": "usuario1@email.com"
        },
        {
            "establishment_id": "2345678",
            "establishment_name": "Clínica São Lucas",
            "field": "endereco",
            "current_value": "Rua A, 100",
            "suggested_value": "Rua A, 100 - Sala 5",
            "submitted_by": "usuario2@email.com"
        },
        {
            "establishment_id": "9876543",
            "establishment_name": "Hospital Santa Maria",
            "field": "horario",
            "current_value": "Seg-Sex: 8h-18h",
            "suggested_value": "Seg-Sex: 7h-19h, Sáb: 8h-12h",
            "submitted_by": "usuario3@email.com"
        }
    ]
    
    for suggestion in suggestions:
        response = requests.post(f"{API_BASE_URL}/edit-suggestions/", json=suggestion)
        if response.status_code == 201:
            print(f"  ✅ Sugestão criada: {suggestion['field']} - {suggestion['establishment_name']}")
        else:
            print(f"  ❌ Erro ao criar sugestão: {response.status_code}")

def populate_doctors():
    """Popula médicos e retorna seus IDs"""
    print("\n👨‍⚕️ Criando médicos...")
    
    doctors = [
        {
            "co_profissional": "123456",
            "name": "Dr. João Silva",
            "specialty": "Cardiologia",
            "establishment_id": "2345678",
            "establishment_name": "Clínica São Lucas",
            "email": "joao.silva@clinica.com",
            "phone": "(11) 99999-1111"
        },
        {
            "co_profissional": "234567",
            "name": "Dra. Maria Santos",
            "specialty": "Pediatria",
            "establishment_id": "2345678",
            "establishment_name": "Clínica São Lucas",
            "email": "maria.santos@clinica.com",
            "phone": "(11) 99999-2222"
        },
        {
            "co_profissional": "345678",
            "name": "Dr. Pedro Costa",
            "specialty": "Ortopedia",
            "establishment_id": "9876543",
            "establishment_name": "Hospital Santa Maria",
            "email": "pedro.costa@hospital.com",
            "phone": "(11) 99999-3333"
        },
        {
            "co_profissional": "456789",
            "name": "Dra. Ana Oliveira",
            "specialty": "Dermatologia",
            "establishment_id": "9876543",
            "establishment_name": "Hospital Santa Maria",
            "email": "ana.oliveira@hospital.com",
            "phone": "(11) 99999-4444"
        }
    ]
    
    doctor_ids = []
    for doctor in doctors:
        response = requests.post(f"{API_BASE_URL}/doctors/", json=doctor)
        if response.status_code == 201:
            doctor_id = response.json()["id"]
            doctor_ids.append(doctor_id)
            print(f"  ✅ Médico criado: {doctor['name']} - ID: {doctor_id}")
        else:
            print(f"  ❌ Erro ao criar médico: {response.status_code}")
    
    return doctor_ids

def populate_availabilities(doctor_ids):
    """Popula disponibilidades dos médicos"""
    print("\n📅 Criando disponibilidades...")
    
    # Disponibilidade para cada médico
    # Segunda a Sexta, manhã e tarde
    days = [0, 1, 2, 3, 4]  # Segunda a Sexta
    
    for doctor_id in doctor_ids:
        for day in days:
            # Manhã: 8h às 12h
            availability_morning = {
                "doctor_id": doctor_id,
                "day_of_week": day,
                "start_time": "08:00:00",
                "end_time": "12:00:00",
                "is_available": True
            }
            
            response = requests.post(
                f"{API_BASE_URL}/doctors/{doctor_id}/availability",
                json=availability_morning
            )
            
            if response.status_code == 201:
                print(f"  ✅ Disponibilidade criada: Médico {doctor_id} - Dia {day} (Manhã)")
            
            # Tarde: 14h às 18h
            availability_afternoon = {
                "doctor_id": doctor_id,
                "day_of_week": day,
                "start_time": "14:00:00",
                "end_time": "18:00:00",
                "is_available": True
            }
            
            response = requests.post(
                f"{API_BASE_URL}/doctors/{doctor_id}/availability",
                json=availability_afternoon
            )
            
            if response.status_code == 201:
                print(f"  ✅ Disponibilidade criada: Médico {doctor_id} - Dia {day} (Tarde)")

def populate_appointments(doctor_ids):
    """Popula agendamentos"""
    print("\n📋 Criando agendamentos...")
    
    # Criar agendamentos para os próximos dias
    base_date = date.today()
    
    appointments = [
        {
            "doctor_id": doctor_ids[0],
            "patient_name": "Carlos Mendes",
            "patient_email": "carlos.mendes@email.com",
            "patient_phone": "(11) 98888-1111",
            "appointment_date": str(base_date + timedelta(days=1)),
            "appointment_time": "09:00:00",
            "notes": "Consulta de rotina - Cardiologia"
        },
        {
            "doctor_id": doctor_ids[0],
            "patient_name": "Juliana Ferreira",
            "patient_email": "juliana.ferreira@email.com",
            "patient_phone": "(11) 98888-2222",
            "appointment_date": str(base_date + timedelta(days=2)),
            "appointment_time": "10:30:00",
            "notes": "Retorno - Exames cardiológicos"
        },
        {
            "doctor_id": doctor_ids[1] if len(doctor_ids) > 1 else doctor_ids[0],
            "patient_name": "Roberto Lima",
            "patient_email": "roberto.lima@email.com",
            "patient_phone": "(11) 98888-3333",
            "appointment_date": str(base_date + timedelta(days=1)),
            "appointment_time": "14:00:00",
            "notes": "Consulta pediátrica - Criança de 5 anos"
        },
        {
            "doctor_id": doctor_ids[2] if len(doctor_ids) > 2 else doctor_ids[0],
            "patient_name": "Patrícia Souza",
            "patient_email": "patricia.souza@email.com",
            "patient_phone": "(11) 98888-4444",
            "appointment_date": str(base_date + timedelta(days=3)),
            "appointment_time": "15:30:00",
            "notes": "Dor no joelho - Ortopedia"
        },
        {
            "doctor_id": doctor_ids[3] if len(doctor_ids) > 3 else doctor_ids[0],
            "patient_name": "Fernando Alves",
            "patient_email": "fernando.alves@email.com",
            "patient_phone": "(11) 98888-5555",
            "appointment_date": str(base_date + timedelta(days=2)),
            "appointment_time": "11:00:00",
            "notes": "Avaliação dermatológica"
        }
    ]
    
    for appointment in appointments:
        response = requests.post(f"{API_BASE_URL}/appointments/", json=appointment)
        if response.status_code == 201:
            print(f"  ✅ Agendamento criado: {appointment['patient_name']} - {appointment['appointment_date']}")
        else:
            print(f"  ❌ Erro ao criar agendamento: {response.status_code}")

def main():
    """Popula todo o banco de dados"""
    print("=" * 60)
    print("  POPULANDO BANCO DE DADOS - FindDoctor Python API")
    print("=" * 60)
    
    # Verifica se API está rodando
    print("\n🔍 Verificando se API está rodando...")
    if not check_api():
        print("❌ API não está rodando! Inicie com: python main.py")
        return
    
    print("✅ API está online!")
    
    # Popular dados
    populate_edit_suggestions()
    doctor_ids = populate_doctors()
    
    if doctor_ids:
        populate_availabilities(doctor_ids)
        populate_appointments(doctor_ids)
    
    # Resumo
    print("\n" + "=" * 60)
    print("  ✅ BANCO POPULADO COM SUCESSO!")
    print("=" * 60)
    print("\n📊 Resumo:")
    print("  • Sugestões de edição: 3")
    print(f"  • Médicos cadastrados: {len(doctor_ids)}")
    print(f"  • Horários disponíveis: {len(doctor_ids) * 10} (5 dias x 2 períodos)")
    print("  • Agendamentos: 5")
    print("\n📚 Acesse http://localhost:8000/docs para ver os dados!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
