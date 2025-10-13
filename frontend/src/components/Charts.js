import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

// Register Chart.js components (from your original)
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Charts = ({ lands }) => {
  const [sensorData, setSensorData] = useState({});  // Real sensor data per land { landId: [sensors] }
  const [ndviData, setNdviData] = useState({});     // Real NDVI per land { landId: ndvi }
  const [loading, setLoading] = useState(true);     // Loading state for fetches
  const [error, setError] = useState(null);         // Error state

  // Fetch real data on mount or lands change
  useEffect(() => {
    if (!lands || lands.length === 0) {
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    const token = localStorage.getItem('token');  // From login (/users/login)
    if (!token) {
      console.warn('No token found—using mock data');
      setLoading(false);
      return;
    }

    // Fetch sensors and NDVI for each land (parallel fetches for efficiency)
    const fetches = lands.map(land => 
      Promise.all([
        fetch(`http://localhost:8000/sensors/?land_id=${land.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(res => {
          if (!res.ok) throw new Error(`Sensors fetch failed: ${res.status}`);
          return res.json();
        }).catch(err => {
          console.error(`Error fetching sensors for land ${land.id}:`, err);
          return [];  // Fallback to empty
        }),
        fetch(`http://localhost:8000/lands/${land.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(res => {
          if (!res.ok) throw new Error(`Land fetch failed: ${res.status}`);
          return res.json();
        }).then(land => land.ndvi || 0.5).catch(err => {
          console.error(`Error fetching land ${land.id}:`, err);
          return 0.5;  // Fallback NDVI
        })
      ]).then(([sensors, ndvi]) => ({
        landId: land.id,
        sensors,
        ndvi
      }))
    );

    Promise.all(fetches)
      .then(results => {
        results.forEach(({ landId, sensors, ndvi }) => {
          setSensorData(prev => ({ ...prev, [landId]: sensors }));
          setNdviData(prev => ({ ...prev, [landId]: ndvi }));
        });
        setLoading(false);
      })
      .catch(err => {
        console.error('Charts fetch error:', err);
        setError('Failed to load chart data—using mock');
        setLoading(false);
      });
  }, [lands]);  // Re-fetch if lands change

  // Fallback mock data (your original logic if no real data)
  const getMockData = (land) => ({
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: land.name,
      data: [Math.random() * 50, Math.random() * 50, Math.random() * 50, Math.random() * 50, land.ndvi * 100 || 50],
      borderColor: land.is_degraded ? 'red' : 'green',
      backgroundColor: land.is_degraded ? 'rgba(255,0,0,0.2)' : 'rgba(0,255,0,0.2)',
    }]
  });

  // Build sensor trends chart data (real or mock)
  const sensorChartData = lands.length > 0 ? {
    labels: lands[0] ? (sensorData[lands[0].id] || []).map(s => new Date(s.timestamp).toLocaleDateString()) : ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: lands.map(land => {
      const realSensors = sensorData[land.id] || [];
      const data = realSensors.length > 0 
        ? realSensors.map(s => s.moisture)  // Real moisture over time
        : getMockData(land).data;  // Fallback mock
      return {
        label: `${land.name} Moisture (%)`,
        data,
        borderColor: land.is_degraded ? 'red' : 'green',
        backgroundColor: land.is_degraded ? 'rgba(255,0,0,0.2)' : 'rgba(0,255,0,0.2)',
        tension: 0.1,
      };
    })
  } : { labels: [], datasets: [] };

  // Build NDVI health chart data (real or mock)
  const ndviChartData = lands.length > 0 ? {
    labels: lands.map(land => land.name),
    datasets: [{
      label: 'NDVI Value',
      data: lands.map(land => ndviData[land.id] || land.ndvi || 0.5),  // Real NDVI or fallback
      backgroundColor: lands.map(land => (ndviData[land.id] || land.ndvi || 0.5) < 0.3 ? 'rgba(255, 99, 132, 0.5)' : 'rgba(75, 192, 192, 0.5)'),
      borderColor: lands.map(land => (ndviData[land.id] || land.ndvi || 0.5) < 0.3 ? 'rgb(255, 99, 132)' : 'rgb(75, 192, 192)'),
      borderWidth: 1,
    }]
  } : { labels: [], datasets: [] };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Land Health Metrics' },
    },
    scales: {
      y: { beginAtZero: true, title: { display: true, text: 'Value (Moisture % / NDVI)' } },
    },
  };

  if (loading) return <div>Loading charts...</div>;
  if (error) return <div>Error: {error} (Check console for details)</div>;
  if (lands.length === 0) return <div>No lands to chart</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <h3>Sensor Trends (Moisture over Time)</h3>
      <Line data={sensorChartData} options={options} />
      <h3>NDVI Health per Land</h3>
      <Bar data={ndviChartData} options={options} />
    </div>
  );
};

export default Charts;