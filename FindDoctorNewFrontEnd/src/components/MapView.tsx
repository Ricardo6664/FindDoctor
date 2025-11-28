import { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { MedicalEstablishment } from '../App';

// Fix for default marker icons in React-Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  iconRetinaUrl: iconRetina,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

// Custom icon for selected markers
const selectedIcon = L.icon({
  iconUrl: icon,
  iconRetinaUrl: iconRetina,
  shadowUrl: iconShadow,
  iconSize: [35, 57],
  iconAnchor: [17, 57],
  popupAnchor: [1, -44],
  shadowSize: [57, 57],
  className: 'selected-marker'
});

interface MapViewProps {
  establishments: MedicalEstablishment[];
  onSelectEstablishment: (establishment: MedicalEstablishment) => void;
}

// Component to handle map updates
function MapUpdater({ establishments }: { establishments: MedicalEstablishment[] }) {
  const map = useMap();

  useEffect(() => {
    if (establishments.length > 0) {
      const bounds = L.latLngBounds(
        establishments.map(est => [est.latitude, est.longitude] as [number, number])
      );
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 15 });
    }
  }, [establishments, map]);

  return null;
}

export function MapView({ establishments, onSelectEstablishment }: MapViewProps) {
  // Calculate center of all establishments
  const center: [number, number] = establishments.length > 0
    ? [
        establishments.reduce((sum, e) => sum + e.latitude, 0) / establishments.length,
        establishments.reduce((sum, e) => sum + e.longitude, 0) / establishments.length,
      ]
    : [-23.561684, -46.655981]; // Default to São Paulo

  return (
    <div className="relative w-full h-[500px] rounded-lg overflow-hidden shadow-lg border border-border">
      <MapContainer
        center={center}
        zoom={13}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        {/* OpenStreetMap tiles - Free and Open Source */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapUpdater establishments={establishments} />
        
        {/* Markers for each establishment */}
        {establishments.map((est) => (
          <Marker
            key={est.id}
            position={[est.latitude, est.longitude]}
            eventHandlers={{
              click: () => {
                onSelectEstablishment(est);
              },
            }}
          >
            <Popup>
              <div className="p-2">
                <h3 className="font-semibold text-sm mb-1">{est.name}</h3>
                <p className="text-xs text-muted-foreground mb-2">{est.address}</p>
                {est.phone && (
                  <p className="text-xs">
                    <strong>Tel:</strong> {est.phone}
                  </p>
                )}
                {est.rating && (
                  <p className="text-xs">
                    <strong>Avaliação:</strong> ⭐ {est.rating} ({est.reviewCount} avaliações)
                  </p>
                )}
              </div>
            </Popup>
          </Marker>
        ))}
        
        {/* Information about the count */}
        <div className="leaflet-bottom leaflet-left" style={{ marginLeft: '10px', marginBottom: '30px' }}>
          <div className="leaflet-control bg-white p-2 rounded shadow-md border border-border">
            <span className="text-sm font-medium">
              {establishments.length} estabelecimento(s) no mapa
            </span>
          </div>
        </div>
      </MapContainer>
    </div>
  );
}
