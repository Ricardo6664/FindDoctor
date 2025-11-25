import { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Badge } from './ui/badge';
import { ArrowLeft, Calendar, Users, TrendingUp, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
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
    case 'pending':
      return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">Pendente</Badge>;
    case 'cancelled':
      return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Cancelada</Badge>;
    default:
      return <Badge>{status}</Badge>;
  }
};

export function DoctorDashboard({ establishment, onBack }: DoctorDashboardProps) {
  const [filterDoctor, setFilterDoctor] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');

  const filteredAppointments = mockAppointments.filter((apt) => {
    const matchesDoctor = filterDoctor === 'all' || apt.doctor === filterDoctor;
    const matchesStatus = filterStatus === 'all' || apt.status === filterStatus;
    return matchesDoctor && matchesStatus;
  });

  const stats = {
    total: mockAppointments.length,
    confirmed: mockAppointments.filter((a) => a.status === 'confirmed').length,
    pending: mockAppointments.filter((a) => a.status === 'pending').length,
    cancelled: mockAppointments.filter((a) => a.status === 'cancelled').length,
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
                  <div className="text-2xl">{stats.total}</div>
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
                  <CardTitle className="text-sm">Pendentes</CardTitle>
                  <AlertCircle className="h-4 w-4 text-yellow-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl">{stats.pending}</div>
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
                        {establishment.doctors.map((doctor) => (
                          <SelectItem key={doctor} value={doctor}>
                            {doctor}
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
                        <SelectItem value="confirmed">Confirmadas</SelectItem>
                        <SelectItem value="pending">Pendentes</SelectItem>
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
                    {filteredAppointments.map((appointment) => (
                      <TableRow key={appointment.id}>
                        <TableCell>
                          <div>
                            <div>{appointment.patientName}</div>
                            <div className="text-sm text-gray-500">{appointment.email}</div>
                          </div>
                        </TableCell>
                        <TableCell>{appointment.doctor}</TableCell>
                        <TableCell>
                          {new Date(appointment.date).toLocaleDateString('pt-BR')}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {appointment.time}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">{appointment.phone}</div>
                        </TableCell>
                        <TableCell>{getStatusBadge(appointment.status)}</TableCell>
                        <TableCell>
                          <div className="flex gap-2">
                            {appointment.status === 'pending' && (
                              <Button size="sm" variant="outline">
                                Confirmar
                              </Button>
                            )}
                            {appointment.status !== 'cancelled' && (
                              <Button size="sm" variant="ghost">
                                Cancelar
                              </Button>
                            )}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
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
