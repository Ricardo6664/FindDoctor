// API Base URL
const API_BASE_URL = 'http://localhost:8000/api';

// ==================== ADDRESS API ====================

export interface AddressResult {
  street: string | null;
  district: string | null;
  city: string | null;
  postcode: string | null;
  country: string | null;
  county: string | null;
  state: string | null;
  name: string | null;
  location: {
    latitude: number;
    longitude: number;
  };
}

export async function searchAddress(address: string): Promise<AddressResult[]> {
  const response = await fetch(
    `${API_BASE_URL}/csharp/address/search?address=${encodeURIComponent(address)}`
  );
  
  if (!response.ok) {
    throw new Error('Erro ao buscar endereço');
  }
  
  return response.json();
}

// ==================== ESTABLISHMENTS API ====================

export interface Establishment {
  codigoCNES: string;
  nome: string;
  cnpj?: string;
  endereco?: string;
  numero?: string;
  bairro?: string;
  cidade?: string;
  uf?: string;
  latitude: number;
  longitude: number;
  telefone?: string;
  profissionais?: Professional[];
}

export interface Professional {
  co_Profissional: string;
  nome: string;
  cns: string;
  sus: boolean;
  especialidadeNome?: string;
}

export async function searchEstablishments(
  latitude: number,
  longitude: number,
  radiusKm: number = 5,
  specialtyId?: string,
  doctorName?: string
): Promise<Establishment[]> {
  const params = new URLSearchParams({
    latitude: latitude.toString(),
    longitude: longitude.toString(),
    radius_km: radiusKm.toString(),
  });
  
  if (specialtyId) params.append('specialty_id', specialtyId);
  if (doctorName) params.append('doctor_name', doctorName);
  
  const response = await fetch(
    `${API_BASE_URL}/csharp/establishments/search?${params}`
  );
  
  if (!response.ok) {
    throw new Error('Erro ao buscar estabelecimentos');
  }
  
  return response.json();
}

export async function getEstablishmentDetails(cnesCode: string): Promise<Establishment | null> {
  const response = await fetch(
    `${API_BASE_URL}/csharp/establishments/${cnesCode}`
  );
  
  if (!response.ok) {
    return null;
  }
  
  return response.json();
}

// ==================== SPECIALTIES API ====================

export interface Specialty {
  id: string;
  nome: string;
}

export async function getSpecialties(): Promise<Specialty[]> {
  const response = await fetch(`${API_BASE_URL}/csharp/specialties`);
  
  if (!response.ok) {
    throw new Error('Erro ao buscar especialidades');
  }
  
  return response.json();
}

// ==================== EDIT SUGGESTIONS API ====================

export interface EditSuggestion {
  id?: number;
  establishment_id: string;
  establishment_name: string;
  field: string;
  current_value?: string;
  suggested_value: string;
  submitted_by: string;
  submitted_at?: string;
  status?: string;
}

export async function createEditSuggestion(suggestion: EditSuggestion): Promise<EditSuggestion> {
  const response = await fetch(`${API_BASE_URL}/edit-suggestions/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(suggestion),
  });
  
  if (!response.ok) {
    throw new Error('Erro ao criar sugestão');
  }
  
  return response.json();
}

export async function listEditSuggestions(status?: string): Promise<EditSuggestion[]> {
  const url = status 
    ? `${API_BASE_URL}/edit-suggestions/?status=${status}`
    : `${API_BASE_URL}/edit-suggestions/`;
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error('Erro ao listar sugestões');
  }
  
  return response.json();
}

export async function deleteEditSuggestion(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/edit-suggestions/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error('Erro ao deletar sugestão');
  }
}

export async function updateEditSuggestionStatus(
  id: number,
  status: 'approved' | 'rejected'
): Promise<EditSuggestion> {
  const response = await fetch(
    `${API_BASE_URL}/edit-suggestions/${id}/status?status=${status}`,
    {
      method: 'PATCH',
    }
  );
  
  if (!response.ok) {
    throw new Error('Erro ao atualizar status');
  }
  
  return response.json();
}

// ==================== HELPER FUNCTIONS ====================

export function formatAddress(result: AddressResult): string {
  const parts = [
    result.name,
    result.street,
    result.district,
    result.city,
    result.state,
    result.postcode,
  ].filter(Boolean);
  
  return parts.join(', ');
}
