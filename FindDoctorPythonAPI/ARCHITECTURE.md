# 🏗️ Arquitetura do Sistema FindDoctor

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                        CAMADA DE APRESENTAÇÃO                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │ FindDoctorNewFrontEnd│      │ FrontEndAgendamento  │        │
│  │  (React + TypeScript)│      │  (React + TypeScript)│        │
│  │                      │      │                      │        │
│  │  • Busca Estabelec.  │      │  • Agendar Consultas │        │
│  │  • Sugestões Edição  │      │  • Dashboard Médico  │        │
│  │  • Mapa Interativo   │      │  • Gestão Horários   │        │
│  └──────────┬───────────┘      └──────────┬───────────┘        │
│             │                              │                     │
└─────────────┼──────────────────────────────┼─────────────────────┘
              │                              │
              │  HTTP/REST                   │  HTTP/REST
              │                              │
┌─────────────┼──────────────────────────────┼─────────────────────┐
│             │     CAMADA DE APLICAÇÃO      │                     │
├─────────────┴──────────────────────────────┴─────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │          FindDoctor Python API (FastAPI)                   │ │
│  │                  http://localhost:8000                     │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                            │ │
│  │  ┌──────────────────┐  ┌──────────────────┐              │ │
│  │  │  Edit Suggestions│  │   Appointments   │              │ │
│  │  │    /api/edit-    │  │  /api/appoint-   │              │ │
│  │  │   suggestions    │  │     ments        │              │ │
│  │  └──────────────────┘  └──────────────────┘              │ │
│  │                                                            │ │
│  │  ┌──────────────────┐  ┌──────────────────┐              │ │
│  │  │     Doctors      │  │   C# API Proxy   │              │ │
│  │  │   /api/doctors   │  │   /api/csharp    │◄─────────────┼─┐
│  │  └──────────────────┘  └──────────────────┘              │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            │  SQLAlchemy ORM
                            │
┌───────────────────────────┼───────────────────────────────────────┐
│                           │       CAMADA DE DADOS                 │
├───────────────────────────┴───────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │   PostgreSQL (porta 6025) - agendamento_db                 │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                            │ │
│  │  📋 edit_suggestions      📅 appointments                 │ │
│  │  👨‍⚕️ doctors                  ⏰ doctor_availabilities      │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────┐
│                    API EXTERNA (C# Backend)                       │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │   FindDoctor C# API (.NET 8)                              │ │
│  │   http://localhost:5210                                    │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                            │ │
│  │  • /api/Address/buscar         (Photon Geocoding)        │ │
│  │  • /api/Estabelecimento/*      (Busca Estabelecimentos)  │ │
│  │  • /api/Especialidade          (Lista Especialidades)    │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │                                        │
│                          │  EF Core + PostGIS                     │
│                          │                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │   PostgreSQL (Supabase) - finddoctor                      │ │
│  │   • Estabelecimentos (CNES)                               │ │
│  │   • Profissionais                                         │ │
│  │   • Especialidades                                        │ │
│  │   • Dados Geoespaciais (PostGIS)                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Dados

### 1️⃣ Busca de Estabelecimentos

```
Frontend → Python API → C# API → Supabase DB → C# API → Python API → Frontend
   │          /api/csharp/         /api/Estabelecimento/
   │          establishments/       proximos
   │          search
   │
   └→ Exibe resultados no mapa e tabela
```

### 2️⃣ Sugestão de Edição

```
Frontend → Python API → PostgreSQL (6025)
   │          /api/edit-            edit_suggestions
   │          suggestions           table
   │
   └→ Confirmação de salvamento
```

### 3️⃣ Agendamento de Consulta

```
Frontend → Python API → PostgreSQL (6025)
   │          /api/appointments     appointments table
   │                 ↓
   │          /api/doctors          doctors table
   │                 ↓
   │          doctor_availabilities doctor_availabilities
   │                                table
   │
   └→ Confirmação de agendamento
```

---

## 📊 Modelo de Dados - Python API

### Tabela: edit_suggestions
```sql
CREATE TABLE edit_suggestions (
    id SERIAL PRIMARY KEY,
    establishment_id VARCHAR(50) NOT NULL,
    establishment_name VARCHAR(255) NOT NULL,
    field VARCHAR(100) NOT NULL,
    current_value TEXT,
    suggested_value TEXT NOT NULL,
    submitted_by VARCHAR(255) NOT NULL,
    submitted_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending'
);
```

### Tabela: doctors
```sql
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    co_profissional VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255),
    establishment_id VARCHAR(50) NOT NULL,
    establishment_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Tabela: doctor_availabilities
```sql
CREATE TABLE doctor_availabilities (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL,  -- 0=Monday, 6=Sunday
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);
```

### Tabela: appointments
```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    patient_name VARCHAR(255) NOT NULL,
    patient_email VARCHAR(255) NOT NULL,
    patient_phone VARCHAR(50) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🛠️ Tecnologias Utilizadas

### Backend Python
- **FastAPI** 0.115.5 - Framework web moderno e rápido
- **SQLAlchemy** 2.0.44 - ORM para banco de dados
- **Pydantic** 2.10.3 - Validação de dados
- **psycopg2** 2.9.10 - Driver PostgreSQL
- **httpx** 0.28.1 - Cliente HTTP assíncrono
- **uvicorn** 0.34.0 - Servidor ASGI

### Backend C# (Existente)
- **.NET 8** - Framework web
- **Entity Framework Core** 9.0.3 - ORM
- **PostgreSQL + PostGIS** - Banco de dados geoespacial
- **NetTopologySuite** - Manipulação de dados geográficos

### Frontend
- **React 18+** - Biblioteca UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool
- **Radix UI** - Componentes acessíveis

---

## 📡 Endpoints Principais

### Python API (porta 8000)

#### Sugestões de Edição
- `POST /api/edit-suggestions/` - Criar
- `GET /api/edit-suggestions/` - Listar
- `GET /api/edit-suggestions/{id}` - Buscar
- `DELETE /api/edit-suggestions/{id}` - Deletar

#### Médicos
- `POST /api/doctors/` - Cadastrar
- `GET /api/doctors/` - Listar
- `GET /api/doctors/{id}` - Buscar
- `DELETE /api/doctors/{id}` - Deletar
- `POST /api/doctors/{id}/availability` - Adicionar horário
- `GET /api/doctors/{id}/availability` - Listar horários

#### Agendamentos
- `POST /api/appointments/` - Criar
- `GET /api/appointments/` - Listar
- `GET /api/appointments/{id}` - Buscar
- `PATCH /api/appointments/{id}` - Atualizar status
- `DELETE /api/appointments/{id}` - Cancelar
- `GET /api/appointments/doctor/{id}/dashboard` - Dashboard

#### Proxy C# API
- `GET /api/csharp/address/search` - Buscar endereços
- `GET /api/csharp/establishments/search` - Buscar estabelecimentos
- `GET /api/csharp/establishments/{cnes}` - Detalhes
- `GET /api/csharp/specialties` - Especialidades

### C# API (porta 5210)

- `GET /api/Address/buscar` - Geocoding
- `GET /api/Estabelecimento/proximos` - Busca geoespacial
- `GET /api/Estabelecimento/{cnes}` - Detalhes
- `GET /api/Especialidade` - Lista especialidades

---

## 🔐 Segurança

### Implementado
✅ CORS configurado para frontends locais
✅ Validação de dados com Pydantic
✅ Queries SQL seguras (SQLAlchemy ORM)
✅ Validação de tipos com TypeScript

### Não Implementado (Futuro)
❌ Autenticação JWT
❌ Rate limiting
❌ HTTPS/TLS
❌ Sanitização avançada de inputs

---

## 📈 Escalabilidade

### Implementado
✅ Separação de concerns (camadas)
✅ ORM para abstração do banco
✅ API stateless
✅ Async I/O (FastAPI + httpx)

### Futuras Melhorias
⏭️ Cache (Redis)
⏭️ Filas de mensagens (RabbitMQ)
⏭️ Load balancing
⏭️ Container Docker
⏭️ CI/CD pipeline

---

## 🧪 Como Testar

```bash
# 1. Iniciar PostgreSQL (porta 6025)
docker run -d --name finddoctor-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=agendamento_db \
  -p 6025:5432 postgres:14

# 2. Iniciar API Python
cd FindDoctorPythonAPI
pip install -r requirements.txt
python main.py

# 3. Popular banco de dados
python populate_db.py

# 4. Testar endpoints
python test_api.py

# 5. Acessar documentação
# http://localhost:8000/docs
```

---

## 📝 Notas de Desenvolvimento

1. **Bancos Separados**: Um para dados CNES (C#), outro para agendamentos (Python)
2. **API C# Intacta**: Não mexemos no backend C# existente
3. **Simplicidade**: Projeto focado em demonstração acadêmica
4. **Sem Autenticação**: Por enquanto, para facilitar desenvolvimento
5. **Mock Data**: Frontends devem migrar de dados mock para API real

---

## 🎯 Próximos Passos

1. ✅ Integrar FindDoctorNewFrontEnd com API
2. ✅ Integrar FrontEndAgendamento com API
3. ⏭️ Adicionar autenticação básica
4. ⏭️ Implementar notificações (email/SMS)
5. ⏭️ Deploy em ambiente de produção
6. ⏭️ Testes automatizados (pytest)
7. ⏭️ Documentação de usuário
