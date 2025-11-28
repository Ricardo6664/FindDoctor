import { useState, useMemo, useEffect } from 'react';
import { Search } from 'lucide-react';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Card } from './ui/card';
import { MapView } from './MapView';
import { ResultsTable } from './ResultsTable';
import { MedicalEstablishment } from '../App';
import * as api from '../services/api';

// Mock data (removido em produção)
const mockEstablishments: MedicalEstablishment[] = [
  {
    id: '1',
    name: 'Clínica São Lucas',
    address: 'Av. Paulista, 1000 - São Paulo, SP',
    latitude: -23.561684,
    longitude: -46.655981,
    doctors: ['Dr. João Silva', 'Dra. Maria Santos', 'Dr. Pedro Oliveira'],
    specialties: ['Cardiologia', 'Clínica Geral', 'Pediatria'],
    insurances: ['Unimed', 'Bradesco Saúde', 'SulAmérica'],
    phone: '(11) 3000-0001',
    hours: 'Seg-Sex: 8h-18h',
    rating: 4.5,
    reviewCount: 128,
  },
  {
    id: '2',
    name: 'Hospital Santa Maria',
    address: 'Rua Augusta, 500 - São Paulo, SP',
    latitude: -23.556858,
    longitude: -46.662042,
    doctors: ['Dra. Ana Costa', 'Dr. Carlos Mendes'],
    specialties: ['Ortopedia', 'Neurologia', 'Cardiologia'],
    insurances: ['Unimed', 'Porto Seguro', 'Amil'],
    phone: '(11) 3000-0002',
    hours: '24 horas',
    rating: 4.8,
    reviewCount: 256,
  },
  {
    id: '3',
    name: 'Centro Médico Vitória',
    address: 'Av. Faria Lima, 2000 - São Paulo, SP',
    latitude: -23.578499,
    longitude: -46.687356,
    doctors: ['Dr. Roberto Alves', 'Dra. Juliana Ramos', 'Dr. Fernando Castro'],
    specialties: ['Dermatologia', 'Oftalmologia', 'Clínica Geral'],
    insurances: ['Bradesco Saúde', 'SulAmérica', 'Golden Cross'],
    phone: '(11) 3000-0003',
    hours: 'Seg-Sex: 7h-20h, Sáb: 8h-14h',
    rating: 4.3,
    reviewCount: 89,
  },
  {
    id: '4',
    name: 'Clínica Boa Saúde',
    address: 'Av. Ibirapuera, 3000 - São Paulo, SP',
    latitude: -23.595805,
    longitude: -46.673031,
    doctors: ['Dra. Patricia Lima', 'Dr. Marcos Souza'],
    specialties: ['Pediatria', 'Ginecologia', 'Clínica Geral'],
    insurances: ['Unimed', 'Bradesco Saúde', 'Amil', 'Porto Seguro'],
    phone: '(11) 3000-0004',
    hours: 'Seg-Sex: 8h-19h',
    rating: 4.6,
    reviewCount: 174,
  },
  {
    id: '5',
    name: 'Instituto Cardio Life',
    address: 'Rua dos Pinheiros, 800 - São Paulo, SP',
    latitude: -23.565000,
    longitude: -46.690000,
    doctors: ['Dr. Eduardo Martins', 'Dra. Beatriz Ferreira'],
    specialties: ['Cardiologia', 'Cirurgia Cardíaca'],
    insurances: ['SulAmérica', 'Amil', 'Golden Cross'],
    phone: '(11) 3000-0005',
    hours: 'Seg-Sex: 7h-18h',
    rating: 4.9,
    reviewCount: 312,
  },
];

interface SearchViewProps {
  onViewDetails: (establishment: MedicalEstablishment) => void;
}

export function SearchView({ onViewDetails }: SearchViewProps) {
  const [address, setAddress] = useState('');
  const [doctorName, setDoctorName] = useState('');
  const [specialty, setSpecialty] = useState('all');
  const [insurance, setInsurance] = useState('all');
  const [establishments, setEstablishments] = useState<MedicalEstablishment[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [specialtiesList, setSpecialtiesList] = useState<api.Specialty[]>([]);

  // Carregar especialidades
  useEffect(() => {
    const loadSpecialties = async () => {
      try {
        const specs = await api.getSpecialties();
        setSpecialtiesList(specs);
      } catch (err) {
        console.error('Erro ao carregar especialidades:', err);
      }
    };
    
    loadSpecialties();
  }, []);

  // Get unique specialties and insurances for filters
  const allSpecialties = useMemo(() => {
    const specialties = new Set<string>();
    mockEstablishments.forEach(est => est.specialties.forEach(s => specialties.add(s)));
    return Array.from(specialties).sort();
  }, []);

  const allInsurances = useMemo(() => {
    const insurances = new Set<string>();
    mockEstablishments.forEach(est => est.insurances.forEach(i => insurances.add(i)));
    return Array.from(insurances).sort();
  }, []);

  // Buscar estabelecimentos
  const handleSearch = async () => {
    if (!address.trim()) {
      setError('Por favor, digite um endereço');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 1. Buscar coordenadas do endereço
      const addressResults = await api.searchAddress(address);
      
      if (addressResults.length === 0) {
        setError('Endereço não encontrado');
        setEstablishments([]);
        return;
      }

      const { latitude, longitude } = addressResults[0].location;

      // 2. Buscar estabelecimentos próximos
      const specialtyId = specialty !== 'all' ? specialty : undefined;
      const results = await api.searchEstablishments(
        latitude,
        longitude,
        2, // 1km de raio
        specialtyId,
        doctorName || undefined
      );

      // 3. Transformar para o formato esperado
      const transformed: MedicalEstablishment[] = results.map((est) => ({
        id: est.codigoCNES,
        name: est.nome,
        address: `${est.endereco || ''}, ${est.numero || ''} - ${est.bairro || ''}, ${est.cidade || ''} - ${est.uf || ''}`.trim(),
        latitude: est.latitude,
        longitude: est.longitude,
        doctors: est.profissionais?.map(p => p.nome) || [],
        specialties: [...new Set(est.profissionais?.map(p => p.especialidadeNome).filter(Boolean) || [])],
        insurances: [], // TODO: Adicionar quando disponível
        phone: est.telefone || 'Não informado',
        hours: 'Consulte o estabelecimento',
        rating: 0,
        reviewCount: 0,
      }));

      setEstablishments(transformed);
    } catch (err) {
      console.error('Erro na busca:', err);
      setError('Erro ao buscar estabelecimentos. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Filter establishments
  const filteredEstablishments = useMemo(() => {
    const dataSource = establishments.length > 0 ? establishments : mockEstablishments;
    
    return dataSource.filter(est => {
      // Filter by doctor name (se já não foi aplicado na busca)
      if (doctorName && establishments.length === 0) {
        if (!est.doctors.some(doc => doc.toLowerCase().includes(doctorName.toLowerCase()))) {
          return false;
        }
      }
      // Filter by insurance
      if (insurance !== 'all' && !est.insurances.includes(insurance)) {
        return false;
      }
      return true;
    });
  }, [establishments, doctorName, insurance]);

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <Card className="p-6 shadow-sm border-border">
        <div className="space-y-4">
          <div>
            <Label htmlFor="address">Buscar por Endereço</Label>
            <div className="flex gap-2 mt-2">
              <Input
                id="address"
                placeholder="Digite o endereço, bairro ou cidade..."
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                className="flex-1 border-border"
                disabled={loading}
              />
              <Button 
                className="gap-2 bg-primary hover:bg-accent"
                onClick={handleSearch}
                disabled={loading}
              >
                <Search className="w-4 h-4" />
                {loading ? 'Buscando...' : 'Buscar'}
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="doctor">Nome do Médico</Label>
              <Input
                id="doctor"
                placeholder="Digite o nome do médico..."
                value={doctorName}
                onChange={(e) => setDoctorName(e.target.value)}
                className="mt-2 border border-black"
              />
            </div>

            <div>
              <Label htmlFor="specialty">Especialidade</Label>
              <Select value={specialty} onValueChange={setSpecialty}>
                <SelectTrigger id="specialty" className="mt-2 border border-black">
                  <SelectValue placeholder="Selecione uma especialidade" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todas as Especialidades</SelectItem>
                  {specialtiesList.length > 0 ? (
                    specialtiesList.map(spec => (
                      <SelectItem key={spec.id} value={spec.id}>{spec.nome}</SelectItem>
                    ))
                  ) : (
                    allSpecialties.map(spec => (
                      <SelectItem key={spec} value={spec}>{spec}</SelectItem>
                    ))
                  )}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="insurance">Convênio</Label>
              <Select value={insurance} onValueChange={setInsurance}>
                <SelectTrigger id="insurance" className="mt-2 border border-black">
                  <SelectValue placeholder="Selecione um convênio" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos os Convênios</SelectItem>
                  {allInsurances.map(ins => (
                    <SelectItem key={ins} value={ins}>{ins}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </Card>

      {/* Map */}
      <Card className="p-0 overflow-hidden shadow-sm border-border">
        <MapView establishments={filteredEstablishments} onSelectEstablishment={onViewDetails} />
      </Card>

      {/* Results Table */}
      <Card className="p-6 shadow-sm border-border">
        <div className="mb-4">
          <h2 className="text-primary">Resultados da Busca</h2>
          {error && (
            <p className="text-destructive mb-2">{error}</p>
          )}
          <p className="text-muted-foreground">
            {filteredEstablishments.length} estabelecimento(s) encontrado(s)
          </p>
        </div>
        {loading ? (
          <div className="text-center py-8">
            <p className="text-muted-foreground">Buscando estabelecimentos...</p>
          </div>
        ) : (
          <ResultsTable establishments={filteredEstablishments} onViewDetails={onViewDetails} />
        )}
      </Card>
    </div>
  );
}
