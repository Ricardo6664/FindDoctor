import { Star, Phone, Clock, Eye } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { MedicalEstablishment } from '../App';

interface ResultsTableProps {
  establishments: MedicalEstablishment[];
  onViewDetails: (establishment: MedicalEstablishment) => void;
}

export function ResultsTable({ establishments, onViewDetails }: ResultsTableProps) {
  if (establishments.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        <p>Nenhum estabelecimento encontrado com os filtros aplicados.</p>
        <p className="text-sm mt-2">Tente ajustar os filtros de busca.</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Estabelecimento</TableHead>
            <TableHead>Endereço</TableHead>
            <TableHead>Especialidades</TableHead>
            <TableHead>Convênios</TableHead>
            <TableHead>Avaliação</TableHead>
            <TableHead>Contato</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {establishments.map((est) => (
            <TableRow key={est.id}>
              <TableCell>
                <div>
                  <div className="mb-1">{est.name}</div>
                  <div className="text-sm text-muted-foreground">
                    {est.doctors.length} médico(s)
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <div className="text-sm max-w-xs text-muted-foreground">{est.address}</div>
              </TableCell>
              <TableCell>
                <div className="flex flex-wrap gap-1">
                  {est.specialties.slice(0, 2).map((spec) => (
                    <Badge key={spec} variant="secondary" className="text-xs">
                      {spec}
                    </Badge>
                  ))}
                  {est.specialties.length > 2 && (
                    <Badge variant="outline" className="text-xs">
                      +{est.specialties.length - 2}
                    </Badge>
                  )}
                </div>
              </TableCell>
              <TableCell>
                <div className="flex flex-wrap gap-1">
                  {est.insurances.slice(0, 2).map((ins) => (
                    <Badge key={ins} variant="outline" className="text-xs">
                      {ins}
                    </Badge>
                  ))}
                  {est.insurances.length > 2 && (
                    <Badge variant="outline" className="text-xs">
                      +{est.insurances.length - 2}
                    </Badge>
                  )}
                </div>
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                  <span>{est.rating.toFixed(1)}</span>
                  <span className="text-sm text-muted-foreground">({est.reviewCount})</span>
                </div>
              </TableCell>
              <TableCell>
                <div className="space-y-1 text-sm">
                  <div className="flex items-center gap-1">
                    <Phone className="w-3 h-3" />
                    {est.phone}
                  </div>
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <Clock className="w-3 h-3" />
                    {est.hours}
                  </div>
                </div>
              </TableCell>
              <TableCell className="text-right">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => onViewDetails(est)}
                  className="gap-1"
                >
                  <Eye className="w-4 h-4" />
                  Ver Detalhes
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
