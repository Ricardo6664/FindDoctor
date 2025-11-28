# 🚀 Guia Rápido - FindDoctor Python API

## ✅ Pré-requisitos

1. ✅ Python 3.8 ou superior instalado
2. ✅ PostgreSQL rodando na porta **6025**
3. ✅ API C# rodando em **http://localhost:5210** (opcional para integração)

## 📦 Instalação e Execução

### Opção 1: Script automático (Windows)
```bash
# Execute o arquivo start.bat
start.bat
```

### Opção 2: Comandos manuais
```bash
# 1. Entre na pasta
cd FindDoctorPythonAPI

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a API
python main.py
```

## 🌐 Acessar a API

Após iniciar, acesse:

- **API Base**: http://localhost:8000
- **Documentação Interativa (Swagger)**: http://localhost:8000/docs
- **Documentação Alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Testar a API

```bash
# Execute o script de testes
python test_api.py
```

## 📋 Principais Endpoints

### 1. Sugestões de Edição
- `POST /api/edit-suggestions/` - Criar sugestão
- `GET /api/edit-suggestions/` - Listar sugestões
- `GET /api/edit-suggestions/{id}` - Buscar por ID

### 2. Médicos
- `POST /api/doctors/` - Cadastrar médico
- `GET /api/doctors/` - Listar médicos
- `POST /api/doctors/{id}/availability` - Adicionar horários
- `GET /api/doctors/{id}/availability` - Ver disponibilidade

### 3. Agendamentos
- `POST /api/appointments/` - Criar agendamento
- `GET /api/appointments/` - Listar agendamentos
- `GET /api/appointments/doctor/{id}/dashboard` - Dashboard médico
- `PATCH /api/appointments/{id}` - Atualizar status

### 4. Integração C# (Proxy)
- `GET /api/csharp/address/search` - Buscar endereços
- `GET /api/csharp/establishments/search` - Buscar estabelecimentos
- `GET /api/csharp/establishments/{cnes}` - Detalhes estabelecimento
- `GET /api/csharp/specialties` - Listar especialidades

## 🔧 Configuração

Edite `config.py` para alterar configurações:

```python
DATABASE_HOST = "localhost"
DATABASE_PORT = 6025
DATABASE_NAME = "agendamento_db"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "postgres"

CSHARP_API_URL = "http://localhost:5210"

API_HOST = "0.0.0.0"
API_PORT = 8000
```

## 🗄️ Banco de Dados

As tabelas são criadas automaticamente na primeira execução:

1. **edit_suggestions** - Sugestões de edição
2. **doctors** - Médicos cadastrados
3. **doctor_availabilities** - Horários disponíveis
4. **appointments** - Agendamentos

## 📝 Exemplo de Uso (Python)

```python
import requests

# Criar sugestão de edição
response = requests.post("http://localhost:8000/api/edit-suggestions/", json={
    "establishment_id": "2345678",
    "establishment_name": "Clínica São Lucas",
    "field": "telefone",
    "current_value": "(11) 3000-0000",
    "suggested_value": "(11) 3000-0001",
    "submitted_by": "usuario@email.com"
})

print(response.json())

# Cadastrar médico
response = requests.post("http://localhost:8000/api/doctors/", json={
    "co_profissional": "123456",
    "name": "Dr. João Silva",
    "specialty": "Cardiologia",
    "establishment_id": "2345678",
    "establishment_name": "Clínica São Lucas"
})

doctor_id = response.json()["id"]

# Criar agendamento
response = requests.post("http://localhost:8000/api/appointments/", json={
    "doctor_id": doctor_id,
    "patient_name": "Maria Santos",
    "patient_email": "maria@email.com",
    "patient_phone": "(11) 98888-8888",
    "appointment_date": "2025-12-01",
    "appointment_time": "09:30:00"
})

print(response.json())
```

## ❓ Troubleshooting

### Erro: "Connection refused" no banco
- ✅ Verifique se PostgreSQL está rodando
- ✅ Confirme que está na porta 6025
- ✅ Verifique usuário/senha em `config.py`

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### API C# não responde
- ✅ Certifique-se que está rodando em http://localhost:5210
- ✅ Os endpoints de proxy funcionarão apenas se a API C# estiver ativa

## 🎯 Próximos Passos

1. ✅ Integrar com **FindDoctorNewFrontEnd**
2. ✅ Integrar com **FrontEndAgendamento**
3. ✅ Testar todos os fluxos
4. ⏭️ Adicionar autenticação (futuramente)
5. ⏭️ Adicionar notificações (futuramente)

## 📞 Suporte

- Documentação completa: http://localhost:8000/docs
- README: `README.md`
- Testes: `test_api.py`
