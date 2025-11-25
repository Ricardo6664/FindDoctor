import { useState } from 'react';
import { Calendar } from './ui/calendar';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Textarea } from './ui/textarea';
import { Calendar as CalendarIcon, Clock, User, Phone, Mail, LayoutDashboard } from 'lucide-react';
import { toast } from 'sonner@2.0.3';

interface Establishment {
  id: string;
  name: string;
  logo: string;
  specialty: string;
  doctors: string[];
  address: string;
  phone: string;
}

interface PublicBookingProps {
  establishment: Establishment;
  onNavigateToDashboard: () => void;
}

const timeSlots = [
  '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
  '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
];

export function PublicBooking({ establishment, onNavigateToDashboard }: PublicBookingProps) {
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [selectedTime, setSelectedTime] = useState<string>('');
  const [selectedDoctor, setSelectedDoctor] = useState<string>('');
  const [patientName, setPatientName] = useState('');
  const [patientEmail, setPatientEmail] = useState('');
  const [patientPhone, setPatientPhone] = useState('');
  const [notes, setNotes] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!date || !selectedTime || !selectedDoctor || !patientName || !patientEmail || !patientPhone) {
      toast.error('Por favor, preencha todos os campos obrigatórios');
      return;
    }

    // Mock booking submission
    toast.success('Consulta agendada com sucesso!', {
      description: `${patientName}, sua consulta está marcada para ${date.toLocaleDateString('pt-BR')} às ${selectedTime}`,
    });

    // Reset form
    setSelectedTime('');
    setSelectedDoctor('');
    setPatientName('');
    setPatientEmail('');
    setPatientPhone('');
    setNotes('');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-[#116cc2] shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="text-5xl">{establishment.logo}</div>
              <div className="text-white">
                <h2 className="text-white">{establishment.name}</h2>
                <p className="text-blue-100">{establishment.specialty}</p>
              </div>
            </div>
            <Button 
              variant="secondary" 
              onClick={onNavigateToDashboard}
              className="flex items-center gap-2"
            >
              <LayoutDashboard className="h-4 w-4" />
              Dashboard Médico
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Info and Calendar */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Informações</CardTitle>
                <CardDescription>Dados do estabelecimento</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-start gap-2">
                  <span className="text-gray-500">📍</span>
                  <p className="text-sm">{establishment.address}</p>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-gray-500">📞</span>
                  <p className="text-sm">{establishment.phone}</p>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-gray-500">👨‍⚕️</span>
                  <div>
                    <p className="text-sm">Médicos disponíveis:</p>
                    <ul className="text-sm text-gray-600 ml-4 mt-1">
                      {establishment.doctors.map((doctor) => (
                        <li key={doctor}>• {doctor}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <CalendarIcon className="h-5 w-5" />
                  Selecione a Data
                </CardTitle>
              </CardHeader>
              <CardContent className="flex justify-center">
                <Calendar
                  mode="single"
                  selected={date}
                  onSelect={setDate}
                  disabled={(date) => date < new Date() || date.getDay() === 0 || date.getDay() === 6}
                  className="rounded-md border"
                />
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Booking Form */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Agende sua Consulta</CardTitle>
                <CardDescription>
                  Preencha o formulário abaixo para agendar sua consulta
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="doctor">Médico *</Label>
                    <Select value={selectedDoctor} onValueChange={setSelectedDoctor}>
                      <SelectTrigger id="doctor">
                        <SelectValue placeholder="Selecione um médico" />
                      </SelectTrigger>
                      <SelectContent>
                        {establishment.doctors.map((doctor) => (
                          <SelectItem key={doctor} value={doctor}>
                            {doctor}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label className="flex items-center gap-2">
                      <Clock className="h-4 w-4" />
                      Horário *
                    </Label>
                    <div className="grid grid-cols-4 gap-2">
                      {timeSlots.map((time) => (
                        <Button
                          key={time}
                          type="button"
                          variant={selectedTime === time ? 'default' : 'outline'}
                          className="h-10"
                          onClick={() => setSelectedTime(time)}
                        >
                          {time}
                        </Button>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="name" className="flex items-center gap-2">
                      <User className="h-4 w-4" />
                      Nome Completo *
                    </Label>
                    <Input
                      id="name"
                      placeholder="Digite seu nome completo"
                      value={patientName}
                      onChange={(e) => setPatientName(e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="email" className="flex items-center gap-2">
                      <Mail className="h-4 w-4" />
                      E-mail *
                    </Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="seu@email.com"
                      value={patientEmail}
                      onChange={(e) => setPatientEmail(e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="phone" className="flex items-center gap-2">
                      <Phone className="h-4 w-4" />
                      Telefone *
                    </Label>
                    <Input
                      id="phone"
                      placeholder="(11) 98765-4321"
                      value={patientPhone}
                      onChange={(e) => setPatientPhone(e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="notes">Observações</Label>
                    <Textarea
                      id="notes"
                      placeholder="Alguma informação adicional (opcional)"
                      value={notes}
                      onChange={(e) => setNotes(e.target.value)}
                      rows={3}
                    />
                  </div>

                  {date && selectedTime && (
                    <div className="bg-blue-50 border-2 border-[#116cc2] rounded-lg p-4">
                      <p className="text-sm">
                        <strong className="text-[#116cc2]">Consulta selecionada:</strong>
                        <br />
                        {date.toLocaleDateString('pt-BR', { 
                          weekday: 'long', 
                          year: 'numeric', 
                          month: 'long', 
                          day: 'numeric' 
                        })} às {selectedTime}
                      </p>
                    </div>
                  )}

                  <Button type="submit" className="w-full">
                    Confirmar Agendamento
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
