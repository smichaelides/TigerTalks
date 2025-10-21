
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import MainPage from './pages/MainPage';
import LoginPage from './pages/Login';
import SettingsPage from './pages/Settings';
import Welcome from './pages/Welcome';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    setIsLoading(true);
    
    try {
      setIsLoggedIn(true);
    } catch (err) {
      console.error('Login failed:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleWelcomeComplete = () => {
    localStorage.setItem('hasCompletedWelcome', 'true');
    // Force a re-render to show the main page
    window.location.href = '/';
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={
            !isLoggedIn ? (
              <LoginPage 
                onLogin={handleLogin}
                isLoading={isLoading}
              />
            ) : (
              <Navigate to="/" replace />
            )
          } 
        />
        <Route 
          path="/settings" 
          element={
            isLoggedIn ? (
              <SettingsPage onLogout={handleLogout} />
            ) : (
              <Navigate to="/" replace />
            )
          } 
        />
        <Route 
          path="/" 
          element={
            isLoggedIn ? (
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
