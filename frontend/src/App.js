import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import MobileView from './components/MobileView';
import { useMediaQuery } from 'react-responsive'; // npm install react-responsive if needed
import './styles.css';

// Add this ErrorBoundary component at the top of your file or in a separate file
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught in boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong. Please refresh the page.</h1>;
    }
    return this.props.children;
  }
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState(null);
  const isMobile = useMediaQuery({ maxWidth: 768 });

  useEffect(() => {
    if (token) {
      // Fetch user profile (simplified)
      setUser({ role: 'farmer' }); // Mock; integrate with API
    }
  }, [token]);

  const handleLogin = (newToken) => {
    setToken(newToken);
    localStorage.setItem('token', newToken);
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    setUser(null);
  };

  if (!token) {
    // Simple login form (expand with full auth UI)
    return (
      <div className="login-container">
        <h1>TerraSync Login</h1>
        <form onSubmit={(e) => { e.preventDefault(); /* Call API */ handleLogin('mock-token'); }}>
          <input type="email" placeholder="Email" required />
          <input type="password" placeholder="Password" required />
          <button type="submit">Login</button>
        </form>
        <p>Demo: Use email &apos;farmer@example.com&apos; / pass &apos;password&apos; (register via API first)</p>
      </div>
    );
  }

  return (
    <ErrorBoundary>  {/* Wrap your app content with ErrorBoundary */}
      <div className="App">
        <header>
          <h1>TerraSync {user?.role ? ` - ${user.role.charAt(0).toUpperCase() + user.role.slice(1)} Dashboard` : ''}</h1>
          <button onClick={handleLogout}>Logout</button>
        </header>
        {isMobile ? <MobileView token={token} /> : <Dashboard token={token} />}
      </div>
    </ErrorBoundary>
  );
}

export default App;