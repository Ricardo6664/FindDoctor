# 🔗 Guia de Integração - Frontends

Este guia mostra como integrar os frontends com a nova API Python.

## 📦 API Python Endpoints

**Base URL**: `http://localhost:8000/api`

---

## 🎨 FindDoctorNewFrontEnd

### Endpoints Necessários

#### 1. Buscar Endereços
```typescript
// GET /api/csharp/address/search?address={endereco}
const searchAddress = async (address: string) => {
  const response = await fetch(
    `http://localhost:8000/api/csharp/address/search?address=${encodeURIComponent(address)}`
  );
  return response.json();
};
```

#### 2. Buscar Estabelecimentos
```typescript
// GET /api/csharp/establishments/search
const searchEstablishments = async (
  latitude: number,
  longitude: number,
  radiusKm: number = 5,
  specialtyId?: string,
  doctorName?: string
) => {
  const params = new URLSearchParams({
    latitude: latitude.toString(),
    longitude: longitude.toString(),
    radius_km: radiusKm.toString(),
  });
  
  if (specialtyId) params.append('specialty_id', specialtyId);
  if (doctorName) params.append('doctor_name', doctorName);
  
  const response = await fetch(
    `http://localhost:8000/api/csharp/establishments/search?${params}`
  );
  return response.json();
};
```

#### 3. Detalhes do Estabelecimento
```typescript
// GET /api/csharp/establishments/{cnes}
const getEstablishmentDetails = async (cnesCode: string) => {
  const response = await fetch(
    `http://localhost:8000/api/csharp/establishments/${cnesCode}`
  );
  return response.json();
};
```

#### 4. Criar Sugestão de Edição
```typescript
// POST /api/edit-suggestions/
interface EditSuggestion {
  establishment_id: string;
  establishment_name: string;
  field: string;
  current_value?: string;
  suggested_value: string;
  submitted_by: string;
}

const createEditSuggestion = async (suggestion: EditSuggestion) => {
  const response = await fetch('http://localhost:8000/api/edit-suggestions/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(suggestion),
  });
  return response.json();
};
```

#### 5. Listar Sugestões
```typescript
// GET /api/edit-suggestions/?status=pending
const listEditSuggestions = async (status?: string) => {
  const url = status 
    ? `http://localhost:8000/api/edit-suggestions/?status=${status}`
    : 'http://localhost:8000/api/edit-suggestions/';
  
  const response = await fetch(url);
  return response.json();
};
```

### Exemplo de Uso no Componente

```typescript
// SearchView.tsx
import { useState, useEffect } from 'react';

export function SearchView() {
  const [establishments, setEstablishments] = useState([]);
  
  const handleSearch = async (address: string) => {
    try {
      // 1. Buscar endereço
      const addressResults = await fetch(
        `http://localhost:8000/api/csharp/address/search?address=${encodeURIComponent(address)}`
      );
      const addresses = await addressResults.json();
      
      if (addresses.length > 0) {
        const { latitude, longitude } = addresses[0].location;
        
        // 2. Buscar estabelecimentos próximos
        const params = new URLSearchParams({
          latitude: latitude.toString(),
          longitude: longitude.toString(),
          radius_km: '5'
        });
        
        const estabResults = await fetch(
          `http://localhost:8000/api/csharp/establishments/search?${params}`
        );
        const establishments = await estabResults.json();
        
        setEstablishments(establishments);
      }
    } catch (error) {
      console.error('Erro na busca:', error);
    }
  };
  
  return (
    // ... seu componente
  );
}
```

---

## 📅 FrontEndAgendamento

### Endpoints Necessários

#### 1. Listar Médicos
```typescript
// GET /api/doctors/?establishment_id={cnes}
const listDoctors = async (establishmentId?: string) => {
  const url = establishmentId
    ? `http://localhost:8000/api/doctors/?establishment_id=${establishmentId}`
    : 'http://localhost:8000/api/doctors/';
  
  const response = await fetch(url);
  return response.json();
};
```

#### 2. Buscar Disponibilidade do Médico
```typescript
// GET /api/doctors/{id}/availability
const getDoctorAvailability = async (doctorId: number, dayOfWeek?: number) => {
  const url = dayOfWeek !== undefined
    ? `http://localhost:8000/api/doctors/${doctorId}/availability?day_of_week=${dayOfWeek}`
    : `http://localhost:8000/api/doctors/${doctorId}/availability`;
  
  const response = await fetch(url);
  return response.json();
};
```

#### 3. Criar Agendamento
```typescript
// POST /api/appointments/
interface AppointmentCreate {
  doctor_id: number;
  patient_name: string;
  patient_email: string;
  patient_phone: string;
  appointment_date: string; // "YYYY-MM-DD"
  appointment_time: string; // "HH:MM:SS"
  notes?: string;
}

const createAppointment = async (appointment: AppointmentCreate) => {
  const response = await fetch('http://localhost:8000/api/appointments/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(appointment),
  });
  
  if (!response.ok) {
    throw new Error('Erro ao criar agendamento');
  }
  
  return response.json();
};
```

#### 4. Listar Agendamentos
```typescript
// GET /api/appointments/?doctor_id={id}&appointment_date={date}
const listAppointments = async (
  doctorId?: number,
  appointmentDate?: string
) => {
  const params = new URLSearchParams();
  if (doctorId) params.append('doctor_id', doctorId.toString());
  if (appointmentDate) params.append('appointment_date', appointmentDate);
  
  const response = await fetch(
    `http://localhost:8000/api/appointments/?${params}`
  );
  return response.json();
};
```

#### 5. Dashboard do Médico
```typescript
// GET /api/appointments/doctor/{id}/dashboard
const getDoctorDashboard = async (
  doctorId: number,
  startDate?: string,
  endDate?: string
) => {
  const params = new URLSearchParams();
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  
  const response = await fetch(
    `http://localhost:8000/api/appointments/doctor/${doctorId}/dashboard?${params}`
  );
  return response.json();
};
```

#### 6. Atualizar Status do Agendamento
```typescript
// PATCH /api/appointments/{id}
const updateAppointmentStatus = async (
  appointmentId: number,
  status: 'scheduled' | 'confirmed' | 'cancelled' | 'completed'
) => {
  const response = await fetch(
    `http://localhost:8000/api/appointments/${appointmentId}`,
    {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    }
  );
  return response.json();
};
```

### Exemplo de Uso no Componente

```typescript
// PublicBooking.tsx
import { useState, useEffect } from 'react';

export function PublicBooking({ establishment }) {
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [availability, setAvailability] = useState([]);
  
  // Carregar médicos do estabelecimento
  useEffect(() => {
    const loadDoctors = async () => {
      const response = await fetch(
        `http://localhost:8000/api/doctors/?establishment_id=${establishment.id}`
      );
      const data = await response.json();
      setDoctors(data);
    };
    
    loadDoctors();
  }, [establishment.id]);
  
  // Carregar disponibilidade quando selecionar médico
  useEffect(() => {
    if (selectedDoctor) {
      const loadAvailability = async () => {
        const response = await fetch(
          `http://localhost:8000/api/doctors/${selectedDoctor}/availability`
        );
        const data = await response.json();
        setAvailability(data);
      };
      
      loadAvailability();
    }
  }, [selectedDoctor]);
  
  const handleSubmit = async (formData) => {
    try {
      const appointment = {
        doctor_id: selectedDoctor,
        patient_name: formData.name,
        patient_email: formData.email,
        patient_phone: formData.phone,
        appointment_date: formData.date.toISOString().split('T')[0],
        appointment_time: formData.time,
        notes: formData.notes,
      };
      
      const response = await fetch('http://localhost:8000/api/appointments/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(appointment),
      });
      
      if (response.ok) {
        alert('Agendamento criado com sucesso!');
      }
    } catch (error) {
      console.error('Erro ao criar agendamento:', error);
    }
  };
  
  return (
    // ... seu componente
  );
}
```

---

## 🔧 Configuração do CORS

A API já está configurada para aceitar requisições dos frontends:

```python
# main.py (já configurado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Se seu frontend rodar em outra porta, adicione em `main.py`.

---

## 📝 Formato de Dados

### Datas e Horários
```typescript
// Data: formato ISO "YYYY-MM-DD"
appointment_date: "2025-12-01"

// Horário: formato "HH:MM:SS"
appointment_time: "14:30:00"

// Dia da semana: 0-6 (0 = Segunda, 6 = Domingo)
day_of_week: 1
```

### Status de Agendamento
```typescript
type AppointmentStatus = 
  | "scheduled"   // Agendado
  | "confirmed"   // Confirmado
  | "cancelled"   // Cancelado
  | "completed"   // Concluído
```

---

## 🧪 Testar Integração

1. **Inicie a API Python**:
```bash
cd FindDoctorPythonAPI
python main.py
```

2. **Popule o banco com dados de exemplo**:
```bash
python populate_db.py
```

3. **Teste os endpoints**:
```bash
python test_api.py
```

4. **Inicie seu frontend**:
```bash
cd FindDoctorNewFrontEnd
npm run dev
```

---

## 📚 Documentação Completa

Acesse a documentação interativa da API:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Lá você pode testar todos os endpoints diretamente pelo navegador!

---

## ⚠️ Checklist de Integração

### FindDoctorNewFrontEnd
- [ ] Substituir dados mock por chamadas à API
- [ ] Implementar busca de endereços
- [ ] Implementar busca de estabelecimentos
- [ ] Implementar sugestões de edição
- [ ] Testar visualização no mapa
- [ ] Testar filtros (especialidade, médico)

### FrontEndAgendamento
- [ ] Substituir dados mock por chamadas à API
- [ ] Carregar lista de médicos
- [ ] Exibir disponibilidade dos médicos
- [ ] Implementar criação de agendamentos
- [ ] Implementar dashboard do médico
- [ ] Implementar atualização de status
- [ ] Testar cancelamento de consultas

---

## 🚀 Exemplo Completo

Veja o arquivo `test_api.py` para exemplos completos de todas as operações!
