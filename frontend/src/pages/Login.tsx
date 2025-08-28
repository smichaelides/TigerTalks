import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import princetonLogo from '../assets/princeton.png';
import tigerAvatar from '../assets/tiggy.png';
import { userAPI } from '../utils/api';


interface LoginProps {
  onLogin: (userId: string) => void;
  isLoading?: boolean;
}

function Login({ onLogin, isLoading = false }: LoginProps) {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      const user = await userAPI.createUser({
        email: 'test@test.com',
        name: 'Test User',
        grad_year: new Date().getFullYear(),
        concentration: 'Test Concentration',
        certificates: [],
      });
      console.log('User created:', user);
      
      // Store user ID and call onLogin with the user ID
      localStorage.setItem('userId', user._id);
      onLogin(user._id);
      navigate('/');
    } catch (error) {
      console.error('Failed to create user:', error);
      setError('Failed to create user. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <img src={princetonLogo} alt="Princeton" className="login-logo" />
          <div className="login-title-container">
            <h1 className="login-title">Meet Tiggy</h1>
            <img src={tigerAvatar} alt="Tiggy" className="login-tiggy" />
          </div>
          <p className="login-subtitle">Your Princeton AI assistant</p>
        </div>

        <div className="login-content">
          {error && <div className="error-message">{error}</div>}
          
          <button
            onClick={handleLogin}
            className="login-button"
            disabled={isSubmitting || isLoading}
          >
            {isSubmitting ? 'Creating account...' : 'Get Started'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login; 