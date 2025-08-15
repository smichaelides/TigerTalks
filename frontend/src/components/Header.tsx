import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiUser, FiSettings, FiLogOut, FiDownload } from 'react-icons/fi';
import princetonLogo from '../assets/princeton.png';

interface HeaderProps {
  onLogout: () => void;
  onDownloadChat?: () => void;
  hasMessages?: boolean;
}

function Header({ onLogout, onDownloadChat, hasMessages = false }: HeaderProps) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSettingsClick = () => {
    navigate('/settings');
    setIsDropdownOpen(false);
  };

  const handleLogoutClick = () => {
    onLogout();
    navigate('/login');
    setIsDropdownOpen(false);
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="header-tiggy-avatar">
            <img src={princetonLogo} alt="Princeton" />
          </div>
          <span className="header-badge">Tiggy</span>
        </div>
        <div className="header-right">
          {/* Download Button */}
          {hasMessages && onDownloadChat && (
            <button 
              className="header-download-button"
              onClick={onDownloadChat}
              title="Download Chat"
            >
              <FiDownload />
            </button>
          )}
          
          {/* Profile Dropdown */}
          <div className="header-profile-container" ref={dropdownRef}>
            <button 
              className="header-button"
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            >
              <FiUser />
            </button>
            {isDropdownOpen && (
              <div className="header-dropdown">
                <button className="dropdown-item" onClick={handleSettingsClick}>
                  <FiSettings />
                  <span>Settings</span>
                </button>
                <button className="dropdown-item" onClick={handleLogoutClick}>
                  <FiLogOut />
                  <span>Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header; 