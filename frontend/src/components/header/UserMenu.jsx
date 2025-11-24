import { useState, useRef, useEffect } from 'react';
import { FiUser, FiLogOut, FiChevronDown } from 'react-icons/fi';

const UserMenu = ({ currentUser, onProfile, onLogout }) => {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-2 rounded-md hover:bg-background/40 transition-colors cursor-pointer"
      >
        <FiUser size={20} className="text-text" />
        <span className="text-text">{currentUser?.display_name || currentUser?.email}</span>
        <FiChevronDown size={16} className={`text-text transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-secondary rounded-md shadow-lg py-1 z-50">
          <button
            onClick={() => {
              onProfile();
              setIsOpen(false);
            }}
            className="flex items-center space-x-2 w-full px-4 py-2 text-text hover:bg-background/40 transition-colors cursor-pointer"
          >
            <FiUser size={18} />
            <span>Profile</span>
          </button>
          <button
            onClick={() => {
              onLogout();
              setIsOpen(false);
            }}
            className="flex items-center space-x-2 w-full px-4 py-2 text-text hover:bg-background/40 transition-colors cursor-pointer"
          >
            <FiLogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default UserMenu;