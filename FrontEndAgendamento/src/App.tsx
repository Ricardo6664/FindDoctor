import { useState } from 'react';
import { PublicBooking } from './components/PublicBooking';
import { DoctorDashboard } from './components/DoctorDashboard';

// Mock data for the establishment
export const establishment = {
  id: 'clinica-saude',
  name: 'Clínica Saúde Total',
  logo: '🏥',
  specialty: 'Clínica Geral',
  doctors: ['Dr. João Silva', 'Dra. Maria Santos', 'Dr. Pedro Costa'],
  address: 'Rua das Flores, 123 - São Paulo, SP',
  phone: '(11) 98765-4321',
};

function App() {
  const [currentView, setCurrentView] = useState<'public' | 'admin'>('public');

  return (
    <>
      {currentView === 'public' ? (
        <PublicBooking 
          establishment={establishment} 
          onNavigateToDashboard={() => setCurrentView('admin')}
        />
      ) : (
        <DoctorDashboard 
          establishment={establishment}
          onBack={() => setCurrentView('public')}
        />
      )}
    </>
  );
}

export default App;
