"""
Script para adicionar médicos para o frontend de agendamento
"""
import requests

API_URL = "http://localhost:8000/api"

doctors = [
    {
        "co_profissional": "PROF001",
        "name": "Dr. João Silva",
        "specialty": "Cardiologia",
        "crm": "123456-SP",
        "establishment_id": "clinica-saude",
        "establishment_name": "Clínica Saúde Total",
        "is_active": True
    },
    {
        "co_profissional": "PROF002",
        "name": "Dra. Maria Santos",
        "specialty": "Pediatria",
        "crm": "234567-SP",
        "establishment_id": "clinica-saude",
        "establishment_name": "Clínica Saúde Total",
        "is_active": True
    },
    {
        "co_profissional": "PROF003",
        "name": "Dr. Pedro Costa",
        "specialty": "Ortopedia",
        "crm": "345678-SP",
        "establishment_id": "clinica-saude",
        "establishment_name": "Clínica Saúde Total",
        "is_active": True
    }
]

print("👨‍⚕️ Cadastrando médicos para Clínica Saúde Total...\n")

for doc in doctors:
    try:
        response = requests.post(f"{API_URL}/doctors/", json=doc)
        if response.status_code == 201:
            data = response.json()
            print(f"✅ {doc['name']} - {doc['specialty']} (ID: {data['id']})")
        elif response.status_code == 400:
            print(f"⚠️  {doc['name']} - Já cadastrado ou erro de validação")
        else:
            print(f"❌ {doc['name']} - Erro {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Erro: API não está rodando em {API_URL}")
        print("   Execute: cd FindDoctorPythonAPI && python main.py")
        break
    except Exception as e:
        print(f"❌ Erro ao cadastrar {doc['name']}: {e}")

print("\n✅ Concluído!")
print(f"🔗 Verifique em: {API_URL}/doctors/")
