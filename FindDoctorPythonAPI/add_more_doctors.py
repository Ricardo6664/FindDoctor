"""
Script para adicionar mais médicos para agendamento
Execute com a API rodando: python add_more_doctors.py
"""
import requests
import json

API_URL = "http://localhost:8000/api"

# Lista expandida de médicos com diversas especialidades
doctors = [
    # Cardiologia
    {
        "co_profissional": "CARD001",
        "name": "Dr. Roberto Almeida",
        "specialty": "Cardiologia",
        "crm": "123456-SP",
        "establishment_id": "2000001",
        "establishment_name": "Hospital do Coração",
        "email": "roberto.almeida@hospitalcoracao.com.br",
        "phone": "(11) 98765-1001",
        "is_active": True
    },
    {
        "co_profissional": "CARD002",
        "name": "Dra. Fernanda Lima",
        "specialty": "Cardiologia",
        "crm": "234567-SP",
        "establishment_id": "2000001",
        "establishment_name": "Hospital do Coração",
        "email": "fernanda.lima@hospitalcoracao.com.br",
        "phone": "(11) 98765-1002",
        "is_active": True
    },
    
    # Pediatria
    {
        "co_profissional": "PED001",
        "name": "Dra. Juliana Mendes",
        "specialty": "Pediatria",
        "crm": "345678-SP",
        "establishment_id": "2000002",
        "establishment_name": "Clínica Pediátrica Crescer",
        "email": "juliana.mendes@crescer.com.br",
        "phone": "(11) 98765-2001",
        "is_active": True
    },
    {
        "co_profissional": "PED002",
        "name": "Dr. Marcos Oliveira",
        "specialty": "Pediatria",
        "crm": "456789-SP",
        "establishment_id": "2000002",
        "establishment_name": "Clínica Pediátrica Crescer",
        "email": "marcos.oliveira@crescer.com.br",
        "phone": "(11) 98765-2002",
        "is_active": True
    },
    {
        "co_profissional": "PED003",
        "name": "Dra. Beatriz Santos",
        "specialty": "Pediatria",
        "crm": "567890-SP",
        "establishment_id": "2000003",
        "establishment_name": "Hospital Infantil São Paulo",
        "email": "beatriz.santos@hisp.com.br",
        "phone": "(11) 98765-2003",
        "is_active": True
    },
    
    # Ortopedia
    {
        "co_profissional": "ORT001",
        "name": "Dr. Eduardo Costa",
        "specialty": "Ortopedia",
        "crm": "678901-SP",
        "establishment_id": "2000004",
        "establishment_name": "Centro Ortopédico SP",
        "email": "eduardo.costa@ortosp.com.br",
        "phone": "(11) 98765-3001",
        "is_active": True
    },
    {
        "co_profissional": "ORT002",
        "name": "Dr. Rafael Barbosa",
        "specialty": "Ortopedia",
        "crm": "789012-SP",
        "establishment_id": "2000004",
        "establishment_name": "Centro Ortopédico SP",
        "email": "rafael.barbosa@ortosp.com.br",
        "phone": "(11) 98765-3002",
        "is_active": True
    },
    
    # Dermatologia
    {
        "co_profissional": "DERM001",
        "name": "Dra. Carolina Rocha",
        "specialty": "Dermatologia",
        "crm": "890123-SP",
        "establishment_id": "2000005",
        "establishment_name": "Clínica de Dermatologia Pele Saudável",
        "email": "carolina.rocha@pelesaudavel.com.br",
        "phone": "(11) 98765-4001",
        "is_active": True
    },
    {
        "co_profissional": "DERM002",
        "name": "Dra. Amanda Ferreira",
        "specialty": "Dermatologia",
        "crm": "901234-SP",
        "establishment_id": "2000005",
        "establishment_name": "Clínica de Dermatologia Pele Saudável",
        "email": "amanda.ferreira@pelesaudavel.com.br",
        "phone": "(11) 98765-4002",
        "is_active": True
    },
    
    # Oftalmologia
    {
        "co_profissional": "OFT001",
        "name": "Dr. Paulo Martins",
        "specialty": "Oftalmologia",
        "crm": "112233-SP",
        "establishment_id": "2000006",
        "establishment_name": "Centro de Oftalmologia Visão Clara",
        "email": "paulo.martins@visaoclara.com.br",
        "phone": "(11) 98765-5001",
        "is_active": True
    },
    {
        "co_profissional": "OFT002",
        "name": "Dra. Patrícia Cunha",
        "specialty": "Oftalmologia",
        "crm": "223344-SP",
        "establishment_id": "2000006",
        "establishment_name": "Centro de Oftalmologia Visão Clara",
        "email": "patricia.cunha@visaoclara.com.br",
        "phone": "(11) 98765-5002",
        "is_active": True
    },
    
    # Ginecologia e Obstetrícia
    {
        "co_profissional": "GINE001",
        "name": "Dra. Mariana Souza",
        "specialty": "Ginecologia e Obstetrícia",
        "crm": "334455-SP",
        "establishment_id": "2000007",
        "establishment_name": "Maternidade Santa Luzia",
        "email": "mariana.souza@santaluzia.com.br",
        "phone": "(11) 98765-6001",
        "is_active": True
    },
    {
        "co_profissional": "GINE002",
        "name": "Dra. Luciana Dias",
        "specialty": "Ginecologia e Obstetrícia",
        "crm": "445566-SP",
        "establishment_id": "2000007",
        "establishment_name": "Maternidade Santa Luzia",
        "email": "luciana.dias@santaluzia.com.br",
        "phone": "(11) 98765-6002",
        "is_active": True
    },
    
    # Psiquiatria
    {
        "co_profissional": "PSI001",
        "name": "Dr. André Campos",
        "specialty": "Psiquiatria",
        "crm": "556677-SP",
        "establishment_id": "2000008",
        "establishment_name": "Clínica de Saúde Mental Equilíbrio",
        "email": "andre.campos@equilibrio.com.br",
        "phone": "(11) 98765-7001",
        "is_active": True
    },
    {
        "co_profissional": "PSI002",
        "name": "Dra. Mônica Aragão",
        "specialty": "Psiquiatria",
        "crm": "667788-SP",
        "establishment_id": "2000008",
        "establishment_name": "Clínica de Saúde Mental Equilíbrio",
        "email": "monica.aragao@equilibrio.com.br",
        "phone": "(11) 98765-7002",
        "is_active": True
    },
    
    # Neurologia
    {
        "co_profissional": "NEURO001",
        "name": "Dr. Felipe Andrade",
        "specialty": "Neurologia",
        "crm": "778899-SP",
        "establishment_id": "2000009",
        "establishment_name": "Instituto Neurológico de São Paulo",
        "email": "felipe.andrade@insp.com.br",
        "phone": "(11) 98765-8001",
        "is_active": True
    },
    {
        "co_profissional": "NEURO002",
        "name": "Dra. Gabriela Moreira",
        "specialty": "Neurologia",
        "crm": "889900-SP",
        "establishment_id": "2000009",
        "establishment_name": "Instituto Neurológico de São Paulo",
        "email": "gabriela.moreira@insp.com.br",
        "phone": "(11) 98765-8002",
        "is_active": True
    },
    
    # Endocrinologia
    {
        "co_profissional": "ENDO001",
        "name": "Dra. Renata Carvalho",
        "specialty": "Endocrinologia",
        "crm": "990011-SP",
        "establishment_id": "2000010",
        "establishment_name": "Centro de Endocrinologia e Diabetes",
        "email": "renata.carvalho@centroendo.com.br",
        "phone": "(11) 98765-9001",
        "is_active": True
    },
    {
        "co_profissional": "ENDO002",
        "name": "Dr. Rodrigo Tavares",
        "specialty": "Endocrinologia",
        "crm": "101112-SP",
        "establishment_id": "2000010",
        "establishment_name": "Centro de Endocrinologia e Diabetes",
        "email": "rodrigo.tavares@centroendo.com.br",
        "phone": "(11) 98765-9002",
        "is_active": True
    },
    
    # Gastroenterologia
    {
        "co_profissional": "GASTRO001",
        "name": "Dr. Bruno Farias",
        "specialty": "Gastroenterologia",
        "crm": "121314-SP",
        "establishment_id": "2000011",
        "establishment_name": "Clínica de Gastroenterologia",
        "email": "bruno.farias@gastroclinica.com.br",
        "phone": "(11) 98765-0001",
        "is_active": True
    },
    {
        "co_profissional": "GASTRO002",
        "name": "Dra. Camila Rezende",
        "specialty": "Gastroenterologia",
        "crm": "131415-SP",
        "establishment_id": "2000011",
        "establishment_name": "Clínica de Gastroenterologia",
        "email": "camila.rezende@gastroclinica.com.br",
        "phone": "(11) 98765-0002",
        "is_active": True
    },
    
    # Urologia
    {
        "co_profissional": "URO001",
        "name": "Dr. Daniel Pires",
        "specialty": "Urologia",
        "crm": "141516-SP",
        "establishment_id": "2000012",
        "establishment_name": "Centro Urológico Avançado",
        "email": "daniel.pires@uroavancado.com.br",
        "phone": "(11) 98765-1111",
        "is_active": True
    },
    {
        "co_profissional": "URO002",
        "name": "Dr. Gustavo Nunes",
        "specialty": "Urologia",
        "crm": "151617-SP",
        "establishment_id": "2000012",
        "establishment_name": "Centro Urológico Avançado",
        "email": "gustavo.nunes@uroavancado.com.br",
        "phone": "(11) 98765-1112",
        "is_active": True
    },
    
    # Otorrinolaringologia
    {
        "co_profissional": "ORL001",
        "name": "Dra. Helena Machado",
        "specialty": "Otorrinolaringologia",
        "crm": "161718-SP",
        "establishment_id": "2000013",
        "establishment_name": "Centro de ORL",
        "email": "helena.machado@centroorl.com.br",
        "phone": "(11) 98765-2222",
        "is_active": True
    },
    {
        "co_profissional": "ORL002",
        "name": "Dr. Igor Monteiro",
        "specialty": "Otorrinolaringologia",
        "crm": "171819-SP",
        "establishment_id": "2000013",
        "establishment_name": "Centro de ORL",
        "email": "igor.monteiro@centroorl.com.br",
        "phone": "(11) 98765-2223",
        "is_active": True
    },
    
    # Clínica Geral
    {
        "co_profissional": "CG001",
        "name": "Dr. Leonardo Silva",
        "specialty": "Clínica Geral",
        "crm": "181920-SP",
        "establishment_id": "2000014",
        "establishment_name": "UBS Central",
        "email": "leonardo.silva@ubscentral.sp.gov.br",
        "phone": "(11) 98765-3333",
        "is_active": True
    },
    {
        "co_profissional": "CG002",
        "name": "Dra. Marisa Costa",
        "specialty": "Clínica Geral",
        "crm": "192021-SP",
        "establishment_id": "2000014",
        "establishment_name": "UBS Central",
        "email": "marisa.costa@ubscentral.sp.gov.br",
        "phone": "(11) 98765-3334",
        "is_active": True
    },
    {
        "co_profissional": "CG003",
        "name": "Dr. Nicolas Ferreira",
        "specialty": "Clínica Geral",
        "crm": "202122-SP",
        "establishment_id": "2000015",
        "establishment_name": "Pronto Socorro Municipal",
        "email": "nicolas.ferreira@psm.sp.gov.br",
        "phone": "(11) 98765-4444",
        "is_active": True
    },
    
    # Geriatria
    {
        "co_profissional": "GERIA001",
        "name": "Dra. Olívia Ramos",
        "specialty": "Geriatria",
        "crm": "212223-SP",
        "establishment_id": "2000016",
        "establishment_name": "Centro Geriátrico Viver Bem",
        "email": "olivia.ramos@viverbem.com.br",
        "phone": "(11) 98765-5555",
        "is_active": True
    },
    {
        "co_profissional": "GERIA002",
        "name": "Dr. Pedro Henrique Lopes",
        "specialty": "Geriatria",
        "crm": "222324-SP",
        "establishment_id": "2000016",
        "establishment_name": "Centro Geriátrico Viver Bem",
        "email": "pedro.lopes@viverbem.com.br",
        "phone": "(11) 98765-5556",
        "is_active": True
    },
    
    # Oncologia
    {
        "co_profissional": "ONCO001",
        "name": "Dr. Quintino Azevedo",
        "specialty": "Oncologia",
        "crm": "232425-SP",
        "establishment_id": "2000017",
        "establishment_name": "Hospital de Oncologia",
        "email": "quintino.azevedo@hosp-onco.com.br",
        "phone": "(11) 98765-6666",
        "is_active": True
    },
    {
        "co_profissional": "ONCO002",
        "name": "Dra. Rita Gomes",
        "specialty": "Oncologia",
        "crm": "242526-SP",
        "establishment_id": "2000017",
        "establishment_name": "Hospital de Oncologia",
        "email": "rita.gomes@hosp-onco.com.br",
        "phone": "(11) 98765-6667",
        "is_active": True
    }
]

def add_doctors():
    """Adiciona médicos via API"""
    print("=" * 70)
    print("👨‍⚕️  SISTEMA DE CADASTRO DE MÉDICOS")
    print("=" * 70)
    print(f"\n📡 API: {API_URL}")
    print(f"📊 Total de médicos a cadastrar: {len(doctors)}\n")
    
    success_count = 0
    already_exists = 0
    error_count = 0
    
    try:
        # Testa conexão com a API
        response = requests.get(f"{API_URL}/doctors/", timeout=5)
        existing_doctors = response.json()
        print(f"✅ API está rodando! ({len(existing_doctors)} médicos já cadastrados)\n")
    except requests.exceptions.ConnectionError:
        print(f"❌ ERRO: API não está rodando em {API_URL}")
        print("\n📝 Para iniciar a API, execute:")
        print("   cd FindDoctorPythonAPI")
        print("   python main.py\n")
        return
    except Exception as e:
        print(f"❌ Erro ao conectar na API: {e}\n")
        return
    
    print("🚀 Iniciando cadastro...\n")
    
    for i, doc in enumerate(doctors, 1):
        try:
            response = requests.post(f"{API_URL}/doctors/", json=doc, timeout=10)
            
            if response.status_code == 201:
                data = response.json()
                success_count += 1
                print(f"✅ [{i:02d}/{len(doctors):02d}] {doc['name']:<30} | {doc['specialty']:<25} | ID: {data['id']}")
            
            elif response.status_code == 400:
                already_exists += 1
                error_msg = response.json().get('detail', 'Erro de validação')
                if 'já cadastrado' in error_msg.lower() or 'already exists' in error_msg.lower():
                    print(f"⚠️  [{i:02d}/{len(doctors):02d}] {doc['name']:<30} | Já cadastrado")
                else:
                    print(f"⚠️  [{i:02d}/{len(doctors):02d}] {doc['name']:<30} | {error_msg}")
            
            else:
                error_count += 1
                print(f"❌ [{i:02d}/{len(doctors):02d}] {doc['name']:<30} | Erro {response.status_code}: {response.text[:50]}")
                
        except requests.exceptions.Timeout:
            error_count += 1
            print(f"❌ [{i:02d}/{len(doctors):02d}] {doc['name']:<30} | Timeout")
        
        except Exception as e:
            error_count += 1
            print(f"❌ [{i:02d}/{len(doctors):02d}] {doc['name']:<30} | Erro: {str(e)[:50]}")
    
    # Resumo final
    print("\n" + "=" * 70)
    print("📊 RESUMO DO CADASTRO")
    print("=" * 70)
    print(f"✅ Cadastrados com sucesso: {success_count}")
    print(f"⚠️  Já existentes:          {already_exists}")
    print(f"❌ Erros:                   {error_count}")
    print(f"📋 Total processado:        {len(doctors)}")
    print("=" * 70)
    
    if success_count > 0:
        print(f"\n🎉 {success_count} médico(s) adicionado(s) com sucesso!")
    
    print(f"\n🔗 Verifique todos os médicos em: {API_URL}/doctors/")
    print(f"📖 Documentação da API: {API_URL.replace('/api', '')}/docs\n")

if __name__ == "__main__":
    add_doctors()
