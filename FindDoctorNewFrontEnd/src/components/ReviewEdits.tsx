import { useState, useEffect } from 'react';
import { ArrowLeft, Check, X, Clock, User } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Alert, AlertDescription } from './ui/alert';
import { Separator } from './ui/separator';
import { EditSuggestion } from '../App';
import * as api from '../services/api';

interface ReviewEditsProps {
  onBack: () => void;
}

export function ReviewEdits({ onBack }: ReviewEditsProps) {
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Carregar sugestões da API
  useEffect(() => {
    const loadSuggestions = async () => {
      try {
        const data = await api.listEditSuggestions();
        // Transformar para o formato esperado
        const transformed = data.map((s: any) => ({
          id: s.id.toString(),
          establishmentId: s.establishment_id,
          establishmentName: s.establishment_name,
          field: s.field,
          currentValue: s.current_value || '',
          suggestedValue: s.suggested_value,
          submittedBy: s.submitted_by,
          submittedAt: s.submitted_at,
          status: s.status as 'pending' | 'approved' | 'rejected',
        }));
        setSuggestions(transformed);
      } catch (err) {
        console.error('Erro ao carregar sugestões:', err);
        setActionMessage({ type: 'error', text: 'Erro ao carregar sugestões' });
      } finally {
        setLoading(false);
      }
    };

    loadSuggestions();
  }, []);

  const handleApprove = async (suggestionId: string) => {
    try {
      await api.updateEditSuggestionStatus(parseInt(suggestionId), 'approved');
      setSuggestions((prev) =>
        prev.map((s) => (s.id === suggestionId ? { ...s, status: 'approved' as const } : s))
      );
      setActionMessage({ type: 'success', text: 'Alteração aprovada com sucesso!' });
      setTimeout(() => setActionMessage(null), 3000);
    } catch (err) {
      console.error('Erro ao aprovar sugestão:', err);
      setActionMessage({ type: 'error', text: 'Erro ao aprovar sugestão' });
    }
  };

  const handleReject = async (suggestionId: string) => {
    try {
      await api.updateEditSuggestionStatus(parseInt(suggestionId), 'rejected');
      setSuggestions((prev) =>
        prev.map((s) => (s.id === suggestionId ? { ...s, status: 'rejected' as const } : s))
      );
      setActionMessage({ type: 'success', text: 'Sugestão rejeitada.' });
      setTimeout(() => setActionMessage(null), 3000);
    } catch (err) {
      console.error('Erro ao rejeitar sugestão:', err);
      setActionMessage({ type: 'error', text: 'Erro ao rejeitar sugestão' });
    }
  };

  const fieldLabels: Record<string, string> = {
    name: 'Nome',
    address: 'Endereço',
    phone: 'Telefone',
    telefone: 'Telefone',
    hours: 'Horário',
    horario: 'Horário',
    endereco: 'Endereço',
    doctors: 'Médicos',
    specialties: 'Especialidades',
    insurances: 'Convênios',
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={onBack} className="gap-2 border-border">
            <ArrowLeft className="w-4 h-4" />
            Voltar
          </Button>
          <h1 className="text-primary">Revisar Sugestões de Edição</h1>
        </div>
        <Card className="p-8 text-center">
          <p className="text-muted-foreground">Carregando sugestões...</p>
        </Card>
      </div>
    );
  }

  const pendingSuggestions = suggestions.filter((s) => s.status === 'pending');
  const approvedSuggestions = suggestions.filter((s) => s.status === 'approved');
  const rejectedSuggestions = suggestions.filter((s) => s.status === 'rejected');

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  const renderSuggestion = (suggestion: EditSuggestion, showActions: boolean = false) => (
    <Card key={suggestion.id} className="p-6 shadow-sm border-border">
      <div className="space-y-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-primary">{suggestion.establishmentName}</h3>
              <Badge variant="outline" className="border-primary/30">{fieldLabels[suggestion.field] || suggestion.field}</Badge>
              {suggestion.status === 'pending' && (
                <Badge variant="secondary" className="gap-1 bg-secondary text-secondary-foreground">
                  <Clock className="w-3 h-3" />
                  Pendente
                </Badge>
              )}
              {suggestion.status === 'approved' && (
                <Badge variant="default" className="gap-1 bg-green-600">
                  <Check className="w-3 h-3" />
                  Aprovada
                </Badge>
              )}
              {suggestion.status === 'rejected' && (
                <Badge variant="destructive" className="gap-1">
                  <X className="w-3 h-3" />
                  Rejeitada
                </Badge>
              )}
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <User className="w-4 h-4" />
              <span>{suggestion.submittedBy}</span>
              <span>•</span>
              <span>{formatDate(suggestion.submittedAt)}</span>
            </div>
          </div>
          {showActions && suggestion.status === 'pending' && (
            <div className="flex gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={() => handleReject(suggestion.id)}
                className="gap-1 border-border"
              >
                <X className="w-4 h-4" />
                Rejeitar
              </Button>
              <Button
                size="sm"
                onClick={() => handleApprove(suggestion.id)}
                className="gap-1 bg-primary hover:bg-accent"
              >
                <Check className="w-4 h-4" />
                Aprovar
              </Button>
            </div>
          )}
        </div>

        <Separator />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <div className="text-sm text-gray-600 mb-1">Valor Atual</div>
            <div className="p-3 bg-red-50 border border-red-200 rounded">
              {suggestion.currentValue}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600 mb-1">Valor Sugerido</div>
            <div className="p-3 bg-green-50 border border-green-200 rounded">
              {suggestion.suggestedValue}
            </div>
          </div>
        </div>
      </div>
    </Card>
  );

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="outline" onClick={onBack} className="gap-2 border-border">
          <ArrowLeft className="w-4 h-4" />
          Voltar
        </Button>
        <div>
          <h1 className="text-primary">Revisão de Alterações</h1>
          <p className="text-muted-foreground">
            Gerencie as sugestões de edição enviadas pela comunidade
          </p>
        </div>
      </div>

      {/* Action Message */}
      {actionMessage && (
        <Alert className={actionMessage.type === 'success' ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}>
          <AlertDescription className={actionMessage.type === 'success' ? 'text-green-800' : 'text-red-800'}>
            {actionMessage.text}
          </AlertDescription>
        </Alert>
      )}

      {/* Tabs */}
      <Tabs defaultValue="pending" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-3">
          <TabsTrigger value="pending" className="gap-2">
            Pendentes
            {pendingSuggestions.length > 0 && (
              <Badge variant="secondary" className="ml-1">
                {pendingSuggestions.length}
              </Badge>
            )}
          </TabsTrigger>
          <TabsTrigger value="approved">Aprovadas</TabsTrigger>
          <TabsTrigger value="rejected">Rejeitadas</TabsTrigger>
        </TabsList>

        <TabsContent value="pending" className="space-y-4 mt-6">
          {pendingSuggestions.length === 0 ? (
            <Card className="p-12 text-center shadow-sm border-border">
              <Clock className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-muted-foreground">Nenhuma sugestão pendente</h3>
              <p className="text-sm text-muted-foreground mt-2">
                Todas as sugestões foram revisadas.
              </p>
            </Card>
          ) : (
            pendingSuggestions.map((suggestion) => renderSuggestion(suggestion, true))
          )}
        </TabsContent>

        <TabsContent value="approved" className="space-y-4 mt-6">
          {approvedSuggestions.length === 0 ? (
            <Card className="p-12 text-center shadow-sm border-border">
              <Check className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-muted-foreground">Nenhuma sugestão aprovada</h3>
            </Card>
          ) : (
            approvedSuggestions.map((suggestion) => renderSuggestion(suggestion))
          )}
        </TabsContent>

        <TabsContent value="rejected" className="space-y-4 mt-6">
          {rejectedSuggestions.length === 0 ? (
            <Card className="p-12 text-center shadow-sm border-border">
              <X className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-muted-foreground">Nenhuma sugestão rejeitada</h3>
            </Card>
          ) : (
            rejectedSuggestions.map((suggestion) => renderSuggestion(suggestion))
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
