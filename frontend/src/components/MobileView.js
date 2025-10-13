import React, { useState, useEffect } from 'react';
import { landsAPI, alertsAPI } from '../services/api';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MobileView = ({ token }) => {
  const [lands, setLands] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [selectedLand, setSelectedLand] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [landsRes, alertsRes] = await Promise.all([landsAPI.getAll(), alertsAPI.getAll()]);
      setLands(landsRes.data || []);
      setAlerts(alertsRes.data || []);
    } catch (error) {
      console.error('Error fetching mobile data:', error);
    }
  };

  const handleAnalyze = async (landId) => {
    try {
      await landsAPI.analyze(landId);
      fetchData(); // Refresh data
      alert('Analysis complete! Check updated status.');
    } catch (error) {
      console.error('Mobile analysis error:', error);
      alert('Analysis failed. Try again.');
    }
  };

  const getHealthStatus = (land) => {
    if (land.is_degraded) return { text: 'Degraded - Action Needed', color: 'red' };
    if (land.ndvi > 0.5) return { text: 'Healthy', color: 'green' };
    return { text: 'Moderate - Monitor', color: 'yellow' };
  };

  const getRecommendations = (land) => {
    if (land.is_degraded) {
      return [
        '1. Plant cover crops to improve soil structure.',
        '2. Apply organic mulch to retain moisture.',
        '3. Test soil and add lime if pH is low.',
        '4. Schedule irrigation if moisture < 20%.'
      ];
    }
    return ['Continue current practices. Land is stable.'];
  };

  return (
    <div className="mobile-view">
      {/* Quick Land Health Cards */}
      <section className="mobile-section">
        <h2>Land Health Status</h2>
        {lands.length === 0 ? (
          <p>No lands registered. Create one via dashboard.</p>
        ) : (
          lands.map((land) => {
            const status = getHealthStatus(land);
            return (
              <div key={land.id} className="mobile-card" onClick={() => setSelectedLand(land.id === selectedLand ? null : land.id)}>
                <h3>{land.name}</h3>
                <p>NDVI: {land.ndvi.toFixed(2)}</p>
                <p style={{ color: status.color, fontWeight: 'bold' }}>{status.text}</p>
                <button onClick={(e) => { e.stopPropagation(); handleAnalyze(land.id); }} className="analyze-btn">
                  Analyze Now
                </button>
              </div>
            );
          })
        )}
      </section>

      {/* Mini Map for Selected Land */}
      {selectedLand && (
        <section className="mobile-section">
          <h2>Map View</h2>
          <MapContainer
            center={[0.5, 34.2]} // Default; use land.location in real
            zoom={10}
            style={{ height: '200px', width: '100%', borderRadius: '8px' }}
          >
            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {/* Marker for selected land */}
            <Marker position={[0.5, 34.2]}>
              <Popup>
                <p>Selected: {lands.find(l => l.id === selectedLand)?.name}</p>
              </Popup>
            </Marker>
          </MapContainer>
        </section>
      )}

      {/* Alerts & Recommendations */}
      <section className="mobile-section">
        <h2>Alerts ({alerts.length})</h2>
        {alerts.length > 0 ? (
          alerts.slice(0, 3).map((alert) => (  // Show top 3 for mobile
            <div key={alert.id} className={`alert ${alert.severity}`} style={{ fontSize: '14px' }}>
              <p>{alert.message}</p>
              <small>Severity: {alert.severity}</small>
            </div>
          ))
        ) : (
          <p>No active alerts.</p>
        )}

        {selectedLand && (
          <>
            <h3>AI Recommendations for {lands.find(l => l.id === selectedLand)?.name}</h3>
            <ul style={{ fontSize: '14px', paddingLeft: '20px' }}>
              {getRecommendations(lands.find(l => l.id === selectedLand)).map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ul>
          </>
        )}
      </section>

      {/* Refresh Button */}
      <button onClick={fetchData} className="refresh-btn" style={{ width: '100%', marginTop: '10px' }}>
        Refresh Data
      </button>
    </div>
  );
};

export default MobileView;