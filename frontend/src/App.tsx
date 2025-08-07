
import { useState } from 'react';
import './App.css';
import MainPage from './pages/MainPage';
import LoginPage from './pages/Login';

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

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    return (
      <LoginPage 
        onLogin={handleLogin}
        isLoading={isLoading}
      />
    );
  }

  return <MainPage onLogout={handleLogout} />;
}

export default App;
