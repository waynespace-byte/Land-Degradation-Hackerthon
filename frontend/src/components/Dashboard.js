import React, { useState, useEffect } from 'react';
import MapView from './MapView';
import Charts from './Charts';
import Alerts from './Alerts';
import { landsAPI, alertsAPI } from '../services/api';

const Dashboard = ({ token }) => {
  const [lands, setLands] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
  if (props && props.token) {
    fetch('http://localhost:8000/api/lands', {
      headers: {
        'accept': 'application/json',
        'Authorization': `Bearer ${props.token}`
      }
    }).then(res => res.json()).then(data => setLands(data)).catch(err => console.error(err));
  }
}, [props.token]);

  const fetchLands = async () => {
    try {
      const { data } = await landsAPI.getAll();
      setLands(data);
    } catch (error) {
      console.error('Error fetching lands:', error);
    }
  };

  const fetchAlerts = async () => {
    try {
      const { data } = await alertsAPI.getAll();
      setAlerts(data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  const handleAnalyze = async (landId) => {
    try {
      await landsAPI.analyze(landId);
      fetchLands(); // Refresh
    } catch (error) {
      console.error('Analysis error:', error);
    }
  };

  return (
    <div className="dashboard">
      <div className="map-container">
        <h2>Land Map</h2>
        <MapView lands={lands} onAnalyze={handleAnalyze} />
      </div>
      <div className="charts-container">
        <h2>Trends</h2>
        <Charts lands={lands} />
      </div>
      <div className="alerts-container">
        <h2>Alerts</h2>
        <Alerts alerts={alerts} onResolve={async (id) => {
          await alertsAPI.resolve(id);
          fetchAlerts();
        }} />
      </div>
    </div>
  );
};

export default Dashboard;