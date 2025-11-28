"""
Exemplos de uso da API FindDoctor Python
Execute a API antes de rodar este script: python main.py
"""
import requests
import json
from datetime import date, time

API_BASE_URL = "http://localhost:8000/api"

def print_response(title, response):
    """Helper para printar respostas"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_health_check():
    """Testa health check"""
    response = requests.get("http://localhost:8000/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_edit_suggestions():
    """Testa sistema de sugestões de edição"""
    print("\n" + "="*60)
    print("  TESTANDO SISTEMA DE SUGESTÕES DE EDIÇÃO")
    print("="*60)
    
    # Criar sugestão
    suggestion_data = {
        "establishment_id": "2345678",
        "establishment_name": "Clínica São Lucas",
        "field": "telefone",
        "current_value": "(11) 3000-0000",
        "suggested_value": "(11) 3000-0001",
        "submitted_by": "usuario@email.com"
    }
    
    response = requests.post(f"{API_BASE_URL}/edit-suggestions/", json=suggestion_data)
    print_response("1. Criar Sugestão", response)
    
    if response.status_code == 201:
        suggestion_id = response.json()["id"]
        
        # Listar sugestões
        response = requests.get(f"{API_BASE_URL}/edit-suggestions/")
        print_response("2. Listar Todas as Sugestões", response)
        
        # Buscar por ID
        response = requests.get(f"{API_BASE_URL}/edit-suggestions/{suggestion_id}")
        print_response(f"3. Buscar Sugestão ID {suggestion_id}", response)
        
        # Filtrar por status
        response = requests.get(f"{API_BASE_URL}/edit-suggestions/?status=pending")
        print_response("4. Filtrar por Status 'pending'", response)

def test_doctors():
    """Testa sistema de médicos"""
    print("\n" + "="*60)
    print("  TESTANDO SISTEMA DE MÉDICOS")
    print("="*60)
    
    # Cadastrar médico
    doctor_data = {
        "co_profissional": "123456",
        "name": "Dr. João Silva",
        "specialty": "Cardiologia",
        "establishment_id": "2345678",
        "establishment_name": "Clínica São Lucas",
        "email": "joao@clinica.com",
        "phone": "(11) 99999-9999"
    }
    
    response = requests.post(f"{API_BASE_URL}/doctors/", json=doctor_data)
    print_response("1. Cadastrar Médico", response)
    
    if response.status_code == 201:
        doctor_id = response.json()["id"]
        
        # Adicionar disponibilidade
        availability_data = {
            "doctor_id": doctor_id,
            "day_of_week": 1,  # Segunda-feira
            "start_time": "08:00:00",
            "end_time": "12:00:00",
            "is_available": True
        }
        
        response = requests.post(f"{API_BASE_URL}/doctors/{doctor_id}/availability", json=availability_data)
        print_response("2. Adicionar Disponibilidade", response)
        
        # Listar médicos
        response = requests.get(f"{API_BASE_URL}/doctors/")
        print_response("3. Listar Todos os Médicos", response)
        
        # Listar disponibilidade
        response = requests.get(f"{API_BASE_URL}/doctors/{doctor_id}/availability")
        print_response(f"4. Listar Disponibilidade do Médico {doctor_id}", response)
        
        return doctor_id
    
    return None

def test_appointments(doctor_id):
    """Testa sistema de agendamentos"""
    print("\n" + "="*60)
    print("  TESTANDO SISTEMA DE AGENDAMENTOS")
    print("="*60)
    
    if not doctor_id:
        print("❌ Pule este teste - Nenhum médico cadastrado")
        return
    
    # Criar agendamento
    appointment_data = {
        "doctor_id": doctor_id,
        "patient_name": "Maria Santos",
        "patient_email": "maria@email.com",
        "patient_phone": "(11) 98888-8888",
        "appointment_date": "2025-12-01",
        "appointment_time": "09:30:00",
        "notes": "Primeira consulta - Check-up"
    }
    
    response = requests.post(f"{API_BASE_URL}/appointments/", json=appointment_data)
    print_response("1. Criar Agendamento", response)
    
    if response.status_code == 201:
        appointment_id = response.json()["id"]
        
        # Listar agendamentos
        response = requests.get(f"{API_BASE_URL}/appointments/")
        print_response("2. Listar Todos os Agendamentos", response)
        
        # Dashboard do médico
        response = requests.get(f"{API_BASE_URL}/appointments/doctor/{doctor_id}/dashboard")
        print_response(f"3. Dashboard do Médico {doctor_id}", response)
        
        # Atualizar status
        update_data = {"status": "confirmed"}
        response = requests.patch(f"{API_BASE_URL}/appointments/{appointment_id}", json=update_data)
        print_response(f"4. Confirmar Agendamento {appointment_id}", response)
        
        # Filtrar por data
        response = requests.get(f"{API_BASE_URL}/appointments/?appointment_date=2025-12-01")
        print_response("5. Filtrar Agendamentos por Data", response)

def test_csharp_proxy():
    """Testa proxy para API C#"""
    print("\n" + "="*60)
    print("  TESTANDO INTEGRAÇÃO COM API C#")
    print("="*60)
    
    # Buscar especialidades
    response = requests.get(f"{API_BASE_URL}/csharp/specialties")
    print_response("1. Listar Especialidades (C# API)", response)
    
    # Buscar endereço
    response = requests.get(f"{API_BASE_URL}/csharp/address/search?address=Avenida Paulista, São Paulo")
    print_response("2. Buscar Endereço (C# API)", response)

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("  TESTANDO API FindDoctor Python")
    print("  Certifique-se que a API está rodando!")
    print("="*60)
    
    # Health check
    if not test_health_check():
        print("\n❌ API não está respondendo! Inicie com: python main.py")
        return
    
    # Testes
    test_edit_suggestions()
    doctor_id = test_doctors()
    test_appointments(doctor_id)
    
    # Teste de integração (requer API C# rodando)
    try:
        test_csharp_proxy()
    except Exception as e:
        print(f"\n⚠️  Integração C# falhou (API C# pode não estar rodando): {e}")
    
    print("\n" + "="*60)
    print("  ✅ TESTES CONCLUÍDOS!")
    print("  📚 Acesse http://localhost:8000/docs para mais detalhes")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
