import { FiSettings } from 'react-icons/fi';
import princetonLogo from '../assets/princeton.png';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="header-tiggy-avatar">
            <img src={princetonLogo} alt="Princeton" />
          </div>
          <span className="header-badge">Tiggy</span>
        </div>
        <button className="header-button">
          <FiSettings />
        </button>
      </div>
    </header>
  );
}

export default Header; 