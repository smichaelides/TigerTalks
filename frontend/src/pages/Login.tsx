import { useNavigate } from 'react-router-dom';
import princetonLogo from '../assets/princeton.png';
import tigerAvatar from '../assets/tiggy.png';

interface LoginProps {
  onLogin: () => void;
  isLoading?: boolean;
}

function Login({ onLogin, isLoading = false }: LoginProps) {
  const navigate = useNavigate();

  const handleLogin = async () => {
    await onLogin();
    navigate('/');
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
          <button
            onClick={handleLogin}
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Login with CAS'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login; 