const API_BASE_URL = 'http://localhost:8000/api';

// ========== Doctor Endpoints ==========

export interface Doctor {
  id: number;
  name: string;
  specialty: string;
  crm: string;
  establishment_id: string;
  establishment_name?: string;
  is_active: boolean;
  created_at: string;
}

export interface DoctorAvailability {
  id: number;
  doctor_id: number;
  day_of_week: number; // 0 = Domingo, 1 = Segunda, ..., 6 = Sábado
  start_time: string; // "09:00"
  end_time: string; // "18:00"
  is_active: boolean;
}

export interface CreateDoctorRequest {
  name: string;
  specialty: string;
  co_profissional: string;  // ID do CNES
  crm?: string;  // Opcional
  establishment_id: string;
  establishment_name?: string;
  is_active?: boolean;
}

export interface CreateAvailabilityRequest {
  day_of_week: number;
  start_time: string;
  end_time: string;
  is_active?: boolean;
}

/**
 * Listar todos os médicos
 */
export async function listDoctors(): Promise<Doctor[]> {
  const response = await fetch(`${API_BASE_URL}/doctors/`);
  if (!response.ok) throw new Error('Erro ao carregar médicos');
  return response.json();
}

/**
 * Buscar médico por ID
 */
export async function getDoctor(id: number): Promise<Doctor> {
  const response = await fetch(`${API_BASE_URL}/doctors/${id}`);
  if (!response.ok) throw new Error('Erro ao carregar médico');
  return response.json();
}

/**
 * Criar novo médico
 */
export async function createDoctor(data: CreateDoctorRequest): Promise<Doctor> {
  const response = await fetch(`${API_BASE_URL}/doctors/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Erro ao criar médico');
  return response.json();
}

/**
 * Listar disponibilidades de um médico
 */
export async function getDoctorAvailability(doctorId: number): Promise<DoctorAvailability[]> {
  const response = await fetch(`${API_BASE_URL}/doctors/${doctorId}/availability`);
  if (!response.ok) throw new Error('Erro ao carregar disponibilidade');
  return response.json();
}

/**
 * Adicionar disponibilidade para um médico
 */
export async function addDoctorAvailability(
  doctorId: number,
  data: CreateAvailabilityRequest
): Promise<DoctorAvailability> {
  const response = await fetch(`${API_BASE_URL}/doctors/${doctorId}/availability`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Erro ao adicionar disponibilidade');
  return response.json();
}

// ========== Appointment Endpoints ==========

export interface Appointment {
  id: number;
  doctor_id: number;
  doctor?: Doctor;  // Nested doctor object from API
  patient_name: string;
  patient_email: string;
  patient_phone: string;
  appointment_date: string; // ISO 8601
  appointment_time: string; // "14:30"
  status: 'scheduled' | 'confirmed' | 'completed' | 'cancelled';
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface CreateAppointmentRequest {
  doctor_id: number;
  patient_name: string;
  patient_email: string;
  patient_phone: string;
  appointment_date: string; // "YYYY-MM-DD"
  appointment_time: string; // "14:30"
  notes?: string;
}

export interface UpdateAppointmentStatusRequest {
  status: 'scheduled' | 'confirmed' | 'completed' | 'cancelled';
}

export interface DashboardStats {
  total_appointments: number;
  scheduled: number;
  confirmed: number;
  completed: number;
  cancelled: number;
  appointments_by_doctor: Array<{
    doctor_id: number;
    doctor_name: string;
    count: number;
  }>;
}

/**
 * Listar consultas (com filtros opcionais)
 */
export async function listAppointments(params?: {
  doctor_id?: number;
  status?: string;
  date?: string;
}): Promise<Appointment[]> {
  const query = new URLSearchParams();
  if (params?.doctor_id) query.set('doctor_id', params.doctor_id.toString());
  if (params?.status) query.set('status', params.status);
  if (params?.date) query.set('date', params.date);

  const url = `${API_BASE_URL}/appointments/?${query.toString()}`;
  const response = await fetch(url);
  if (!response.ok) throw new Error('Erro ao carregar consultas');
  return response.json();
}

/**
 * Buscar consulta por ID
 */
export async function getAppointment(id: number): Promise<Appointment> {
  const response = await fetch(`${API_BASE_URL}/appointments/${id}`);
  if (!response.ok) throw new Error('Erro ao carregar consulta');
  return response.json();
}

/**
 * Criar nova consulta
 */
export async function createAppointment(data: CreateAppointmentRequest): Promise<Appointment> {
  const response = await fetch(`${API_BASE_URL}/appointments/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Erro ao agendar consulta');
  return response.json();
}

/**
 * Atualizar status de uma consulta
 */
export async function updateAppointmentStatus(
  id: number,
  data: UpdateAppointmentStatusRequest
): Promise<Appointment> {
  const response = await fetch(`${API_BASE_URL}/appointments/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Erro ao atualizar status');
  return response.json();
}

/**
 * Deletar consulta
 */
export async function deleteAppointment(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/appointments/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Erro ao deletar consulta');
}

/**
 * Obter estatísticas do dashboard
 */
export async function getDashboardStats(): Promise<DashboardStats> {
  const response = await fetch(`${API_BASE_URL}/appointments/dashboard/stats`);
  if (!response.ok) throw new Error('Erro ao carregar estatísticas');
  return response.json();
}

// ========== Utility Functions ==========

/**
 * Formatar data ISO para formato brasileiro
 */
export function formatDate(isoDate: string): string {
  const date = new Date(isoDate);
  return date.toLocaleDateString('pt-BR');
}

/**
 * Formatar data e hora juntos
 */
export function formatDateTime(date: string, time: string): string {
  return `${formatDate(date)} às ${time}`;
}

/**
 * Converter dia da semana (número) para texto
 */
export function getDayName(dayOfWeek: number): string {
  const days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
  return days[dayOfWeek] || '';
}

/**
 * Traduzir status
 */
export function getStatusLabel(status: string): string {
  const labels: Record<string, string> = {
    scheduled: 'Agendada',
    confirmed: 'Confirmada',
    completed: 'Realizada',
    cancelled: 'Cancelada',
  };
  return labels[status] || status;
}
