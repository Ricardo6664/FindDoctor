import { useEffect, useRef, useState } from 'react';
import { MapPin } from 'lucide-react';
import { MedicalEstablishment } from '../App';

interface MapViewProps {
  establishments: MedicalEstablishment[];
  onSelectEstablishment: (establishment: MedicalEstablishment) => void;
}

export function MapView({ establishments, onSelectEstablishment }: MapViewProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // Calculate center of all establishments
  const center = establishments.length > 0
    ? {
        lat: establishments.reduce((sum, e) => sum + e.latitude, 0) / establishments.length,
        lng: establishments.reduce((sum, e) => sum + e.longitude, 0) / establishments.length,
      }
    : { lat: -23.561684, lng: -46.655981 }; // Default to São Paulo

  return (
    <div className="relative w-full h-[500px] bg-secondary/30">
      {/* Map visualization using CSS and HTML (simplified version) */}
      <div className="absolute inset-0 overflow-hidden">
        <div 
          className="relative w-full h-full"
          style={{
            backgroundImage: `
              linear-gradient(rgba(17, 108, 194, 0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(17, 108, 194, 0.1) 1px, transparent 1px)
            `,
            backgroundSize: '50px 50px',
            backgroundColor: '#e3f2fd'
          }}
        >
          {/* Map markers */}
          {establishments.map((est, index) => {
            // Simple positioning based on lat/lng relative to center
            const offsetX = (est.longitude - center.lng) * 8000 + 50;
            const offsetY = (center.lat - est.latitude) * 8000 + 50;
            
            return (
              <div
                key={est.id}
                className="absolute transform -translate-x-1/2 -translate-y-full cursor-pointer transition-all hover:scale-110"
                style={{
                  left: `calc(50% + ${offsetX}%)`,
                  top: `calc(50% + ${offsetY}%)`,
                }}
                onClick={() => {
                  setSelectedId(est.id);
                  onSelectEstablishment(est);
                }}
              >
                <div className="relative">
                  <MapPin 
                    className={`w-8 h-8 ${selectedId === est.id ? 'text-destructive' : 'text-primary'} drop-shadow-lg`}
                    fill={selectedId === est.id ? '#dc2626' : '#116cc2'}
                  />
                  <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap bg-white px-2 py-1 rounded shadow-lg text-sm opacity-0 hover:opacity-100 transition-opacity border border-border">
                    {est.name}
                  </div>
                </div>
              </div>
            );
          })}
          
          {/* Legend */}
          <div className="absolute bottom-4 left-4 bg-white p-3 rounded-lg shadow-lg border border-border">
            <div className="flex items-center gap-2 mb-1">
              <MapPin className="w-4 h-4 text-primary" fill="#116cc2" />
              <span className="text-sm">Estabelecimento</span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-destructive" fill="#dc2626" />
              <span className="text-sm">Selecionado</span>
            </div>
          </div>

          {/* Info box */}
          <div className="absolute top-4 left-4 bg-white p-3 rounded-lg shadow-lg border border-border">
            <p className="text-sm">
              {establishments.length} estabelecimento(s) no mapa
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
