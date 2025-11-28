# FindDoctor Python API

API FastAPI para sistema de edições sugeridas e agendamentos do FindDoctor.

## 🚀 Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

## ⚙️ Configuração

As configurações estão em `config.py`. Valores padrão:

- **Banco de Dados**: PostgreSQL na porta 6025
- **API C#**: http://localhost:5210
- **Porta da API**: 8000

## 🏃 Como Executar

```bash
# Executar a API
python main.py

# Ou com uvicorn direto
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **Documentação Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 Endpoints Principais

### Edit Suggestions (Sugestões de Edição)
- `POST /api/edit-suggestions/` - Criar sugestão
- `GET /api/edit-suggestions/` - Listar sugestões
- `GET /api/edit-suggestions/{id}` - Buscar por ID
- `DELETE /api/edit-suggestions/{id}` - Deletar sugestão

### Doctors (Médicos)
- `POST /api/doctors/` - Cadastrar médico
- `GET /api/doctors/` - Listar médicos
- `GET /api/doctors/{id}` - Buscar por ID
- `POST /api/doctors/{id}/availability` - Adicionar disponibilidade
- `GET /api/doctors/{id}/availability` - Listar disponibilidade

### Appointments (Agendamentos)
- `POST /api/appointments/` - Criar agendamento
- `GET /api/appointments/` - Listar agendamentos
- `GET /api/appointments/{id}` - Buscar por ID
- `PATCH /api/appointments/{id}` - Atualizar status
- `DELETE /api/appointments/{id}` - Cancelar agendamento
- `GET /api/appointments/doctor/{id}/dashboard` - Dashboard do médico

### C# API Proxy (Integração)
- `GET /api/csharp/address/search` - Buscar endereços
- `GET /api/csharp/establishments/search` - Buscar estabelecimentos
- `GET /api/csharp/establishments/{cnes}` - Detalhes do estabelecimento
- `GET /api/csharp/specialties` - Listar especialidades (**fonte: arquivo JSON local**)

> **Nota:** O endpoint de especialidades agora usa o arquivo `medical_specialties.json` local devido a problemas no endpoint C# `/api/Especialidade`.

## 🗄️ Banco de Dados

O banco é criado automaticamente na inicialização. Tabelas:

1. **edit_suggestions** - Sugestões de edição de estabelecimentos
2. **doctors** - Médicos cadastrados para agendamento
3. **doctor_availabilities** - Disponibilidade de horários
4. **appointments** - Agendamentos de consultas

## 🔧 Tecnologias

- FastAPI 0.115.5
- SQLAlchemy 2.0.44
- PostgreSQL
- Pydantic
- HTTPX (cliente HTTP)
- Uvicorn

## 📝 Exemplos de Uso

### Criar Sugestão de Edição
```bash
curl -X POST "http://localhost:8000/api/edit-suggestions/" \
  -H "Content-Type: application/json" \
  -d '{
    "establishment_id": "2345678",
    "establishment_name": "Clínica São Lucas",
    "field": "telefone",
    "current_value": "(11) 3000-0000",
    "suggested_value": "(11) 3000-0001",
    "submitted_by": "usuario@email.com"
  }'
```

### Cadastrar Médico
```bash
curl -X POST "http://localhost:8000/api/doctors/" \
  -H "Content-Type: application/json" \
  -d '{
    "co_profissional": "123456",
    "name": "Dr. João Silva",
    "specialty": "Cardiologia",
    "establishment_id": "2345678",
    "establishment_name": "Clínica São Lucas",
    "email": "joao@clinica.com",
    "phone": "(11) 99999-9999"
  }'
```

### Criar Agendamento
```bash
curl -X POST "http://localhost:8000/api/appointments/" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": 1,
    "patient_name": "Maria Santos",
    "patient_email": "maria@email.com",
    "patient_phone": "(11) 98888-8888",
    "appointment_date": "2025-12-01",
    "appointment_time": "14:30:00",
    "notes": "Primeira consulta"
  }'
```

## 🎯 Integração com Frontend

### FindDoctorNewFrontEnd
Use os endpoints de **edit-suggestions** e **csharp proxy**.

### FrontEndAgendamento
Use os endpoints de **doctors**, **appointments** e **csharp proxy**.

## 📦 Estrutura do Projeto

```
FindDoctorPythonAPI/
├── main.py                      # Aplicação principal
├── config.py                    # Configurações
├── database.py                  # Conexão com banco
├── models.py                    # Modelos SQLAlchemy
├── schemas.py                   # Schemas Pydantic
├── csharp_client.py             # Cliente para API C#
├── medical_specialties.json     # Lista de especialidades médicas (81 itens)
├── routers/                     # Routers da API
│   ├── edit_suggestions.py
│   ├── doctors.py
│   ├── appointments.py
│   └── csharp_proxy.py
├── requirements.txt             # Dependências
├── test_api.py                  # Testes da API
├── test_specialties.py          # Teste de especialidades
└── README.md
```

## 🐛 Troubleshooting

### Endpoint de Especialidades
Se o endpoint C# `/api/Especialidade` estiver retornando 500:
- A API Python usa automaticamente o arquivo `medical_specialties.json` local
- O arquivo contém 81 especialidades médicas do CNES
- Nenhuma configuração adicional necessária

### Erro de Conexão com Banco
- Verifique se o Docker do PostgreSQL está rodando na porta 6025
- Execute: `docker ps` para confirmar

### API C# Inacessível
- Apenas os endpoints de **especialidades** têm fallback local
- Para outros endpoints, certifique-se que a API C# está rodando em http://localhost:5210
