"""
Script simples para popular médicos no banco
Execute com a API rodando
"""
import requests

API_URL = "http://localhost:8000/api"

doctors = [
    {
        "co_profissional": "MD001",
        "name": "Dr. João Silva",
        "specialty": "Cardiologia",
        "crm": "123456-SP",
        "establishment_id": "2345678",
        "establishment_name": "Clínica São Lucas",
        "email": "joao@clinica.com",
        "phone": "(11) 99999-1111",
        "is_active": True
    },
    {
        "co_profissional": "MD002",
        "name": "Dra. Maria Santos",
        "specialty": "Pediatria",
        "crm": "234567-SP",
        "establishment_id": "2345678",
        "establishment_name": "Clínica São Lucas",
        "email": "maria@clinica.com",
        "phone": "(11) 99999-2222",
        "is_active": True
    },
    {
        "co_profissional": "MD003",
        "name": "Dr. Pedro Costa",
        "specialty": "Ortopedia",
        "crm": "345678-SP",
        "establishment_id": "9876543",
        "establishment_name": "Hospital Santa Maria",
        "email": "pedro@hospital.com",
        "phone": "(11) 99999-3333",
        "is_active": True
    },
    {
        "co_profissional": "MD004",
        "name": "Dra. Ana Oliveira",
        "specialty": "Dermatologia",
        "crm": "456789-SP",
        "establishment_id": "9876543",
        "establishment_name": "Hospital Santa Maria",
        "email": "ana@hospital.com",
        "phone": "(11) 99999-4444",
        "is_active": True
    },
    {
        "co_profissional": "MD005",
        "name": "Dr. Carlos Mendes",
        "specialty": "Oftalmologia",
        "crm": "567890-SP",
        "establishment_id": "1234567",
        "establishment_name": "Centro Médico Vitória",
        "email": "carlos@centro.com",
        "phone": "(11) 99999-5555",
        "is_active": True
    }
]

print("👨‍⚕️ Cadastrando médicos...\n")

for doc in doctors:
    try:
        response = requests.post(f"{API_URL}/doctors/", json=doc)
        if response.status_code == 201:
            print(f"✅ {doc['name']} - {doc['specialty']}")
        elif response.status_code == 400:
            print(f"⚠️  {doc['name']} - Já cadastrado")
        else:
            print(f"❌ {doc['name']} - Erro {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao cadastrar {doc['name']}: {e}")

print("\n✅ Concluído!")
print(f"🔗 Verifique em: {API_URL}/doctors/")
