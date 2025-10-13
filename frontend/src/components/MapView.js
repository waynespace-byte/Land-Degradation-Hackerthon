import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css'; // Ensure CSS is imported

const MapView = ({ lands, onAnalyze }) => {
  const position = [0.5, 34.2]; // Default center (e.g., Kenya coords)

  return (
    <MapContainer center={position} zoom={6} style={{ height: '300px', width: '100%' }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {lands.map((land) => {
        const [lat, lon] = land.location.split(',').map(Number);
        const color = land.is_degraded ? 'red' : land.ndvi > 0.5 ? 'green' : 'yellow';
        return (
          <Marker key={land.id} position={[lat, lon]}>
            <Popup>
              <h3>{land.name}</h3>
              <p>NDVI: {land.ndvi.toFixed(2)} | Degraded: {land.is_degraded ? 'Yes' : 'No'}</p>
              <button onClick={() => onAnalyze(land.id)} style={{ background: color, color: 'white' }}>
                Analyze
              </button>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
};

export default MapView;