
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import './App.css';
import MainPage from './pages/MainPage';
import LoginPage from './pages/Login';
import SettingsPage from './pages/Settings';
import Welcome from './pages/Welcome';
import Callback from './pages/Callback';
import { Auth0Provider } from '@auth0/auth0-react';

function App() {
  const { isAuthenticated, isLoading, logout } = useAuth0();

  const handleWelcomeComplete = () => {
    localStorage.setItem('hasCompletedWelcome', 'true');
    // Force a re-render to show the main page
    window.location.href = '/';
  };

  const handleLogout = () => {
    localStorage.removeItem('userProfile');
    localStorage.removeItem('userId');
    localStorage.removeItem('hasCompletedWelcome');
    logout({ logoutParams: { returnTo: `${window.location.origin}/login` } });
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route path="/callback" element={<Callback />} />
        <Route 
          path="/login" 
          element={
            !isAuthenticated ? (
              <LoginPage />
            ) : (
              <Navigate to="/" replace />
            )
          } 
        />
        <Route 
          path="/settings" 
          element={
            isAuthenticated ? (
              <SettingsPage onLogout={handleLogout} />
            ) : (
              <Navigate to="/login" replace />
            )
          } 
        />
        <Route 
          path="/" 
          element={
            isAuthenticated ? (
              localStorage.getItem('hasCompletedWelcome') ? (
                <MainPage onLogout={handleLogout} />
              ) : (
                <Welcome onComplete={handleWelcomeComplete} />
              )
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
