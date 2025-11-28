import { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Badge } from './ui/badge';
import { ArrowLeft, Calendar, Users, TrendingUp, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import * as api from '../services/api';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

interface Establishment {
  id: string;
  name: string;
  logo: string;
  specialty: string;
  doctors: string[];
  address: string;
  phone: string;
}

interface DoctorDashboardProps {
  establishment: Establishment;
  onBack: () => void;
}

// Mock appointments data
const mockAppointments = [
  {
    id: 1,
    patientName: 'Ana Silva',
    doctor: 'Dr. João Silva',
    date: '2025-11-07',
    time: '09:00',
    status: 'confirmed',
    phone: '(11) 98765-4321',
    email: 'ana@email.com',
  },
  {
    id: 2,
    patientName: 'Carlos Santos',
    doctor: 'Dra. Maria Santos',
    date: '2025-11-07',
    time: '10:00',
    status: 'confirmed',
    phone: '(11) 91234-5678',
    email: 'carlos@email.com',
  },
  {
    id: 3,
    patientName: 'Julia Oliveira',
    doctor: 'Dr. Pedro Costa',
    date: '2025-11-07',
    time: '14:30',
    status: 'pending',
    phone: '(11) 99876-5432',
    email: 'julia@email.com',
  },
  {
    id: 4,
    patientName: 'Roberto Lima',
    doctor: 'Dr. João Silva',
    date: '2025-11-08',
    time: '09:30',
    status: 'confirmed',
    phone: '(11) 98888-7777',
    email: 'roberto@email.com',
  },
  {
    id: 5,
    patientName: 'Fernanda Costa',
    doctor: 'Dra. Maria Santos',
    date: '2025-11-08',
    time: '11:00',
    status: 'cancelled',
    phone: '(11) 97777-6666',
    email: 'fernanda@email.com',
  },
  {
    id: 6,
    patientName: 'Paulo Mendes',
    doctor: 'Dr. Pedro Costa',
    date: '2025-11-08',
    time: '15:00',
    status: 'confirmed',
    phone: '(11) 96666-5555',
    email: 'paulo@email.com',
  },
];

// Mock metrics data
const weeklyData = [
  { day: 'Seg', consultas: 12 },
  { day: 'Ter', consultas: 15 },
  { day: 'Qua', consultas: 18 },
  { day: 'Qui', consultas: 14 },
  { day: 'Sex', consultas: 16 },
];

const monthlyData = [
  { month: 'Jun', consultas: 45, receita: 4500 },
  { month: 'Jul', consultas: 52, receita: 5200 },
  { month: 'Ago', consultas: 48, receita: 4800 },
  { month: 'Set', consultas: 61, receita: 6100 },
  { month: 'Out', consultas: 58, receita: 5800 },
];

const statusData = [
  { name: 'Confirmadas', value: 68, color: '#10b981' },
  { name: 'Pendentes', value: 15, color: '#f59e0b' },
  { name: 'Canceladas', value: 7, color: '#ef4444' },
];

const getStatusBadge = (status: string) => {
  switch (status) {
    case 'confirmed':
      return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Confirmada</Badge>;
    case 'scheduled':
      return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-100">Agendada</Badge>;
    case 'completed':
      return <Badge className="bg-purple-100 text-purple-800 hover:bg-purple-100">Realizada</Badge>;
    case 'cancelled':
      return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Cancelada</Badge>;
    default:
      return <Badge>{status}</Badge>;
  }
};

export function DoctorDashboard({ establishment, onBack }: DoctorDashboardProps) {
  const [filterDoctor, setFilterDoctor] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [appointments, setAppointments] = useState<api.Appointment[]>([]);
  const [doctors, setDoctors] = useState<api.Doctor[]>([]);
  const [dashboardStats, setDashboardStats] = useState<api.DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  // Carregar dados da API
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const appointmentsData = await api.listAppointments();
        const doctorsData = await api.listDoctors();
        
        // Filtrar médicos do estabelecimento
        const establishmentDoctors = doctorsData.filter(d => d.establishment_id === establishment.id);
        const doctorIds = establishmentDoctors.map(d => d.id);
        
        // Filtrar agendamentos apenas dos médicos deste estabelecimento
        const establishmentAppointments = appointmentsData.filter(apt => 
          doctorIds.includes(apt.doctor_id)
        );
        
        setAppointments(establishmentAppointments);
        setDoctors(establishmentDoctors);
        setDashboardStats(null);
      } catch (err) {
        console.error('Erro ao carregar dados:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [establishment.id]);

  const handleStatusChange = async (appointmentId: number, newStatus: 'confirmed' | 'completed' | 'cancelled') => {
    try {
      await api.updateAppointmentStatus(appointmentId, { status: newStatus });
      // Atualizar localmente
      setAppointments(prev =>
        prev.map(apt => apt.id === appointmentId ? { ...apt, status: newStatus } : apt)
      );
    } catch (err) {
      console.error('Erro ao atualizar status:', err);
    }
  };

  const filteredAppointments = appointments.filter((apt) => {
    const matchesDoctor = filterDoctor === 'all' || apt.doctor_id.toString() === filterDoctor;
    const matchesStatus = filterStatus === 'all' || apt.status === filterStatus;
    return matchesDoctor && matchesStatus;
  });

  const stats = dashboardStats || {
    total_appointments: appointments.length,
    scheduled: appointments.filter(a => a.status === 'scheduled').length,
    confirmed: appointments.filter(a => a.status === 'confirmed').length,
    completed: appointments.filter(a => a.status === 'completed').length,
    cancelled: appointments.filter(a => a.status === 'cancelled').length,
    appointments_by_doctor: [],
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-[#116cc2] shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="secondary" size="icon" onClick={onBack}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div className="flex items-center gap-3">
                <div className="text-5xl">{establishment.logo}</div>
                <div className="text-white">
                  <h2 className="text-white">{establishment.name}</h2>
                  <p className="text-blue-100">Dashboard Administrativo</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Tabs defaultValue="appointments" className="space-y-6">
          <TabsList>
            <TabsTrigger value="appointments" className="flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              Consultas
            </TabsTrigger>
            <TabsTrigger value="metrics" className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              Métricas
            </TabsTrigger>
          </TabsList>

          {/* Appointments Tab */}
          <TabsContent value="appointments" className="space-y-6">
            {/* Stats Cards */}
            <div className="grid md:grid-cols-4 gap-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm">Total de Consultas</CardTitle>
                  <Calendar className="h-4 w-4 text-gray-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl">{stats.total_appointments}</div>
                  <p className="text-xs text-gray-500 mt-1">Todos os agendamentos</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm">Confirmadas</CardTitle>
                  <CheckCircle className="h-4 w-4 text-green-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl">{stats.confirmed}</div>
                  <p className="text-xs text-gray-500 mt-1">Prontas para atendimento</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm">Agendadas</CardTitle>
                  <AlertCircle className="h-4 w-4 text-yellow-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl">{stats.scheduled}</div>
                  <p className="text-xs text-gray-500 mt-1">Aguardando confirmação</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm">Canceladas</CardTitle>
                  <XCircle className="h-4 w-4 text-red-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl">{stats.cancelled}</div>
                  <p className="text-xs text-gray-500 mt-1">Não realizadas</p>
                </CardContent>
              </Card>
            </div>

            {/* Appointments Table */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Agenda de Consultas</CardTitle>
                    <CardDescription>Lista completa de agendamentos</CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Select value={filterDoctor} onValueChange={setFilterDoctor}>
                      <SelectTrigger className="w-[200px]">
                        <SelectValue placeholder="Filtrar por médico" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Todos os médicos</SelectItem>
                        {doctors.map((doctor) => (
                          <SelectItem key={doctor.id} value={doctor.id.toString()}>
                            {doctor.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>

                    <Select value={filterStatus} onValueChange={setFilterStatus}>
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Filtrar por status" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Todos os status</SelectItem>
                        <SelectItem value="scheduled">Agendadas</SelectItem>
                        <SelectItem value="confirmed">Confirmadas</SelectItem>
                        <SelectItem value="completed">Realizadas</SelectItem>
                        <SelectItem value="cancelled">Canceladas</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Paciente</TableHead>
                      <TableHead>Médico</TableHead>
                      <TableHead>Data</TableHead>
                      <TableHead>Horário</TableHead>
                      <TableHead>Contato</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Ações</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {loading ? (
                      <TableRow>
                        <TableCell colSpan={7} className="text-center text-gray-500">
                          Carregando consultas...
                        </TableCell>
                      </TableRow>
                    ) : filteredAppointments.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={7} className="text-center text-gray-500">
                          Nenhuma consulta encontrada
                        </TableCell>
                      </TableRow>
                    ) : (
                      filteredAppointments.map((appointment) => (
                        <TableRow key={appointment.id}>
                          <TableCell>
                            <div>
                              <div>{appointment.patient_name}</div>
                              <div className="text-sm text-gray-500">{appointment.patient_email}</div>
                            </div>
                          </TableCell>
                          <TableCell>
                            {appointment.doctor?.name || 'N/A'}
                          </TableCell>
                          <TableCell>
                            {new Date(appointment.appointment_date).toLocaleDateString('pt-BR')}
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {appointment.appointment_time}
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="text-sm">{appointment.patient_phone}</div>
                          </TableCell>
                          <TableCell>{getStatusBadge(appointment.status)}</TableCell>
                          <TableCell>
                            <div className="flex gap-2">
                              {appointment.status === 'scheduled' && (
                                <Button 
                                  size="sm" 
                                  variant="outline"
                                  onClick={() => handleStatusChange(appointment.id, 'confirmed')}
                                >
                                  Confirmar
                                </Button>
                              )}
                              {appointment.status === 'confirmed' && (
                                <Button 
                                  size="sm" 
                                  variant="outline"
                                  onClick={() => handleStatusChange(appointment.id, 'completed')}
                                >
                                  Concluir
                                </Button>
                              )}
                              {appointment.status !== 'cancelled' && appointment.status !== 'completed' && (
                                <Button 
                                  size="sm" 
                                  variant="ghost"
                                  onClick={() => handleStatusChange(appointment.id, 'cancelled')}
                                >
                                  Cancelar
                                </Button>
                              )}
                            </div>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Metrics Tab */}
          <TabsContent value="metrics" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Weekly Appointments */}
              <Card>
                <CardHeader>
                  <CardTitle>Consultas por Dia (Semana Atual)</CardTitle>
                  <CardDescription>Volume diário de atendimentos</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={weeklyData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="day" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="consultas" fill="#116cc2" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Status Distribution */}
              <Card>
                <CardHeader>
                  <CardTitle>Distribuição por Status</CardTitle>
                  <CardDescription>Visão geral dos agendamentos</CardDescription>
                </CardHeader>
                <CardContent className="flex justify-center">
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={statusData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) =>
                          `${name}: ${(percent * 100).toFixed(0)}%`
                        }
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {statusData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Monthly Trend */}
              <Card className="md:col-span-2">
                <CardHeader>
                  <CardTitle>Evolução Mensal</CardTitle>
                  <CardDescription>Número de consultas nos últimos meses</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={monthlyData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Line
                        type="monotone"
                        dataKey="consultas"
                        stroke="#116cc2"
                        strokeWidth={2}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Additional Stats */}
            <div className="grid md:grid-cols-3 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Média Diária</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl">15 consultas</div>
                  <p className="text-xs text-gray-500 mt-1">Por dia útil</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Taxa de Confirmação</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl">75.6%</div>
                  <p className="text-xs text-gray-500 mt-1">Consultas confirmadas</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Horário Mais Popular</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl">09:00 - 11:00</div>
                  <p className="text-xs text-gray-500 mt-1">Período da manhã</p>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
