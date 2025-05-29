import { useState, useEffect, useRef } from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';
import '../CSS/mapa.css';

const containerStyle = {
  width: '1106px',
  height: '600px'
};

const defaultCenter = {
  lat: -22.236353920628613,
  lng: -49.96302752734856
};

function Mapa() {
  const [pontos, setPontos] = useState([]);
  const mapRef = useRef(null);

  useEffect(() => {
    function handleEstabelecimentosAtualizados(event) {
      const novosPontos = event.detail;
      setPontos(novosPontos);

      if (novosPontos.length && mapRef.current) {
        const bounds = new window.google.maps.LatLngBounds();
        novosPontos.forEach(ponto => {
          bounds.extend({ lat: ponto.latitude, lng: ponto.longitude });
        });
        mapRef.current.fitBounds(bounds);
      }
    }

    window.addEventListener('estabelecimentosAtualizados', handleEstabelecimentosAtualizados);
    return () => {
      window.removeEventListener('estabelecimentosAtualizados', handleEstabelecimentosAtualizados);
    };
  }, []);

  return (
    <div className="mapa_container">
      <div className="mapa_content">
        <LoadScript googleMapsApiKey="AIzaSyAbyVQ7-Ps7svcNGKw43a_BvbZqLM7IXaU">
          <GoogleMap
            mapContainerStyle={containerStyle}
            center={defaultCenter}
            zoom={14}
            onLoad={map => (mapRef.current = map)}
          >
            {pontos.map((ponto, i) => (
              <Marker
                key={i}
                position={{ lat: ponto.latitude, lng: ponto.longitude }}
                title={ponto.nome}
              />
            ))}
          </GoogleMap>
        </LoadScript>
      </div>
    </div>
  );
}

export default Mapa;
