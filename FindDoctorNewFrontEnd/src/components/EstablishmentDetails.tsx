import { useState } from 'react';
import { ArrowLeft, Star, Phone, Clock, MapPin, Users, Building, FileText, Edit } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { MedicalEstablishment } from '../App';
import { EditEstablishmentDialog } from './EditEstablishmentDialog';

interface EstablishmentDetailsProps {
  establishment: MedicalEstablishment;
  onBack: () => void;
}

export function EstablishmentDetails({ establishment, onBack }: EstablishmentDetailsProps) {
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="outline" onClick={onBack} className="gap-2 border-border">
          <ArrowLeft className="w-4 h-4" />
          Voltar
        </Button>
        <div className="flex-1">
          <h1 className="text-primary">{establishment.name}</h1>
          <div className="flex items-center gap-2 mt-1">
            <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
            <span>{establishment.rating.toFixed(1)}</span>
            <span className="text-muted-foreground">
              ({establishment.reviewCount} avaliações)
            </span>
          </div>
        </div>
        <Button onClick={() => setIsEditDialogOpen(true)} className="gap-2 bg-primary hover:bg-accent">
          <Edit className="w-4 h-4" />
          Sugerir Edição
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Info */}
          <Card className="p-6 shadow-sm border-border">
            <h2 className="mb-4 text-primary">Informações Básicas</h2>
            
            <div className="space-y-4">
              <div className="flex gap-3">
                <MapPin className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Endereço</div>
                  <div>{establishment.address}</div>
                </div>
              </div>

              <Separator />

              <div className="flex gap-3">
                <Phone className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Telefone</div>
                  <div>{establishment.phone}</div>
                </div>
              </div>

              <Separator />

              <div className="flex gap-3">
                <Clock className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Horário de Funcionamento</div>
                  <div>{establishment.hours}</div>
                </div>
              </div>
            </div>
          </Card>

          {/* Doctors */}
          <Card className="p-6 shadow-sm border-border">
            <div className="flex items-center gap-2 mb-4">
              <Users className="w-5 h-5 text-primary" />
              <h2 className="text-primary">Médicos</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {establishment.doctors.map((doctor, index) => (
                <div key={index} className="flex items-center gap-2 p-3 bg-secondary/30 rounded-lg border border-border">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <Users className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <div>{doctor}</div>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Map */}
          <Card className="p-0 overflow-hidden shadow-sm border-border">
            <div className="relative w-full h-[300px] bg-secondary/30">
              <div 
                className="absolute inset-0"
                style={{
                  backgroundImage: `
                    linear-gradient(rgba(17, 108, 194, 0.1) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(17, 108, 194, 0.1) 1px, transparent 1px)
                  `,
                  backgroundSize: '50px 50px',
                  backgroundColor: '#e3f2fd'
                }}
              >
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-full">
                  <MapPin className="w-12 h-12 text-destructive drop-shadow-lg" fill="#dc2626" />
                </div>
                <div className="absolute bottom-4 left-4 bg-white p-3 rounded-lg shadow-lg border border-border">
                  <p className="text-sm">{establishment.address}</p>
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Specialties */}
          <Card className="p-6 shadow-sm border-border">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-primary" />
              <h3 className="text-primary">Especialidades</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {establishment.specialties.map((spec) => (
                <Badge key={spec} variant="secondary" className="bg-secondary text-secondary-foreground">
                  {spec}
                </Badge>
              ))}
            </div>
          </Card>

          {/* Insurances */}
          <Card className="p-6 shadow-sm border-border">
            <div className="flex items-center gap-2 mb-4">
              <Building className="w-5 h-5 text-primary" />
              <h3 className="text-primary">Convênios Aceitos</h3>
            </div>
            <div className="space-y-2">
              {establishment.insurances.map((insurance) => (
                <div key={insurance} className="flex items-center gap-2 p-2 bg-secondary/30 rounded-lg border border-border">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm">{insurance}</span>
                </div>
              ))}
            </div>
          </Card>

          {/* Quick Actions */}
          <Card className="p-6 bg-secondary/50 border-primary/20 shadow-sm">
            <h3 className="mb-2 text-primary">Informação Incorreta?</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Ajude a melhorar a precisão das informações sugerindo edições.
            </p>
            <Button 
              onClick={() => setIsEditDialogOpen(true)} 
              className="w-full gap-2 bg-primary hover:bg-accent"
            >
              <Edit className="w-4 h-4" />
              Sugerir Edição
            </Button>
          </Card>
        </div>
      </div>

      <EditEstablishmentDialog
        establishment={establishment}
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
      />
    </div>
  );
}
