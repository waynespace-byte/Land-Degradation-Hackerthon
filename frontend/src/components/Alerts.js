import React from 'react';

const Alerts = ({ alerts, onResolve }) => {
  return (
    <div>
      {alerts.length === 0 ? (
        <p>No alerts at the moment. All lands are healthy!</p>
      ) : (
        alerts.map((alert) => (
          <div key={alert.id} className={`alert ${alert.severity}`}>
            <h4>{alert.message}</h4>
            <p>Severity: {alert.severity.toUpperCase()} | Time: {new Date(alert.timestamp).toLocaleString()}</p>
            <button onClick={() => onResolve(alert.id)} style={{ background: '#dc3545', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '3px' }}>
              Resolve
            </button>
          </div>
        ))
      )}
    </div>
  );
};

export default Alerts;