import { useState } from 'react';
import { Check } from 'lucide-react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Label } from './ui/label';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Alert, AlertDescription } from './ui/alert';
import { MedicalEstablishment } from '../App';
import * as api from '../services/api';

interface EditEstablishmentDialogProps {
  establishment: MedicalEstablishment;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function EditEstablishmentDialog({ establishment, open, onOpenChange }: EditEstablishmentDialogProps) {
  const [field, setField] = useState('');
  const [currentValue, setCurrentValue] = useState('');
  const [suggestedValue, setSuggestedValue] = useState('');
  const [submitterName, setSubmitterName] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fields = [
    { value: 'name', label: 'Nome do Estabelecimento' },
    { value: 'address', label: 'Endereço' },
    { value: 'phone', label: 'Telefone' },
    { value: 'hours', label: 'Horário de Funcionamento' },
    { value: 'doctors', label: 'Médicos' },
    { value: 'specialties', label: 'Especialidades' },
    { value: 'insurances', label: 'Convênios' },
  ];

  const handleFieldChange = (value: string) => {
    setField(value);
    
    // Set current value based on field
    switch (value) {
      case 'name':
        setCurrentValue(establishment.name);
        break;
      case 'address':
        setCurrentValue(establishment.address);
        break;
      case 'phone':
        setCurrentValue(establishment.phone);
        break;
      case 'hours':
        setCurrentValue(establishment.hours);
        break;
      case 'doctors':
        setCurrentValue(establishment.doctors.join(', '));
        break;
      case 'specialties':
        setCurrentValue(establishment.specialties.join(', '));
        break;
      case 'insurances':
        setCurrentValue(establishment.insurances.join(', '));
        break;
      default:
        setCurrentValue('');
    }
    
    setSuggestedValue('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    setSubmitting(true);
    setError(null);
    
    try {
      // Enviar para a API Python
      await api.createEditSuggestion({
        establishment_id: establishment.id,
        establishment_name: establishment.name,
        field: field,
        current_value: currentValue,
        suggested_value: suggestedValue,
        submitted_by: submitterName || 'Anônimo',
      });
      
      setSubmitted(true);
      
      // Reset form after 2 seconds
      setTimeout(() => {
        setSubmitted(false);
        setField('');
        setCurrentValue('');
        setSuggestedValue('');
        setSubmitterName('');
        setError(null);
        onOpenChange(false);
      }, 2000);
    } catch (err) {
      console.error('Erro ao enviar sugestão:', err);
      setError('Erro ao enviar sugestão. Tente novamente.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Sugerir Edição</DialogTitle>
          <DialogDescription>
            Ajude a manter as informações atualizadas. Sua sugestão será revisada antes de ser publicada.
          </DialogDescription>
        </DialogHeader>

        {submitted ? (
          <Alert className="bg-green-50 border-green-200">
            <Check className="w-4 h-4 text-green-600" />
            <AlertDescription className="text-green-800">
              Sua sugestão foi enviada com sucesso! Ela será revisada em breve.
            </AlertDescription>
          </Alert>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert className="bg-red-50 border-red-200">
                <AlertDescription className="text-red-800">
                  {error}
                </AlertDescription>
              </Alert>
            )}
            <div>
              <Label htmlFor="establishment">Estabelecimento</Label>
              <Input
                id="establishment"
                value={establishment.name}
                disabled
                className="mt-2 bg-gray-50"
              />
            </div>

            <div>
              <Label htmlFor="field">Campo a ser Editado</Label>
              <Select value={field} onValueChange={handleFieldChange}>
                <SelectTrigger id="field" className="mt-2">
                  <SelectValue placeholder="Selecione o campo que deseja editar" />
                </SelectTrigger>
                <SelectContent>
                  {fields.map((f) => (
                    <SelectItem key={f.value} value={f.value}>
                      {f.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {field && (
              <>
                <div>
                  <Label htmlFor="current">Valor Atual</Label>
                  <Textarea
                    id="current"
                    value={currentValue}
                    disabled
                    className="mt-2 bg-gray-50"
                    rows={3}
                  />
                </div>

                <div>
                  <Label htmlFor="suggested">Valor Sugerido</Label>
                  <Textarea
                    id="suggested"
                    value={suggestedValue}
                    onChange={(e) => setSuggestedValue(e.target.value)}
                    placeholder="Digite o novo valor correto..."
                    className="mt-2"
                    rows={3}
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="submitter">Seu Nome (opcional)</Label>
                  <Input
                    id="submitter"
                    value={submitterName}
                    onChange={(e) => setSubmitterName(e.target.value)}
                    placeholder="Digite seu nome..."
                    className="mt-2"
                  />
                  <p className="text-sm text-gray-600 mt-1">
                    Usado apenas para controle interno
                  </p>
                </div>

                <div className="flex justify-end gap-2 pt-4">
                  <Button type="button" variant="outline" onClick={() => onOpenChange(false)} disabled={submitting}>
                    Cancelar
                  </Button>
                  <Button type="submit" disabled={!suggestedValue || submitting}>
                    {submitting ? 'Enviando...' : 'Enviar Sugestão'}
                  </Button>
                </div>
              </>
            )}
          </form>
        )}
      </DialogContent>
    </Dialog>
  );
}
