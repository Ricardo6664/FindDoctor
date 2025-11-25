import { useState } from 'react';
import { Search, MapPin, ClipboardList } from 'lucide-react';
import { Button } from './components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { SearchView } from './components/SearchView';
import { EstablishmentDetails } from './components/EstablishmentDetails';
import { ReviewEdits } from './components/ReviewEdits';
import Logo from "@/assets/localmed_logo.jpg";

export type MedicalEstablishment = {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  doctors: string[];
  specialties: string[];
  insurances: string[];
  phone: string;
  hours: string;
  rating: number;
  reviewCount: number;
};

export type EditSuggestion = {
  id: string;
  establishmentId: string;
  establishmentName: string;
  field: string;
  currentValue: string;
  suggestedValue: string;
  submittedBy: string;
  submittedAt: string;
  status: 'pending' | 'approved' | 'rejected';
};

export default function App() {
  const [currentView, setCurrentView] = useState<'search' | 'details' | 'review'>('search');
  const [selectedEstablishment, setSelectedEstablishment] = useState<MedicalEstablishment | null>(null);

  const handleViewDetails = (establishment: MedicalEstablishment) => {
    setSelectedEstablishment(establishment);
    setCurrentView('details');
  };

  const handleBackToSearch = () => {
    setCurrentView('search');
    setSelectedEstablishment(null);
  };

  const handleGoToReview = () => {
    setCurrentView('review');
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-primary sticky top-0 z-50 shadow-md">
        <div className="mx-auto px-6 py-4" style={{ maxWidth: '90vw' }}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-white p-2 rounded-lg">
                 <img
                  src={Logo}
                  alt="FindDoctor logo"
                  className="w-10 h-10 object-contain"
                />
              </div>
              <h1 className="text-white">FindDoctor - Busca de Estabelecimentos Médicos</h1>
            </div>
            <Button
              variant="secondary"
              onClick={handleGoToReview}
              className="gap-2 bg-white text-primary hover:bg-white/90"
            >
              <ClipboardList className="w-4 h-4" />
              Revisar Alterações
            </Button>
          </div>
        </div>
      </header>

      <main className="mx-auto px-6 py-8" style={{ maxWidth: '90vw' }}>
        {currentView === 'search' && (
          <SearchView onViewDetails={handleViewDetails} />
        )}
        {currentView === 'details' && selectedEstablishment && (
          <EstablishmentDetails
            establishment={selectedEstablishment}
            onBack={handleBackToSearch}
          />
        )}
        {currentView === 'review' && (
          <ReviewEdits onBack={handleBackToSearch} />
        )}
      </main>
    </div>
  );
}
