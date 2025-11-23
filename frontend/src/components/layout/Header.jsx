import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { signOut } from 'firebase/auth';
import { FiMenu, FiX } from 'react-icons/fi';
import { useToast } from "../../contexts/ToastContext.jsx";
import { useAuth } from "../../contexts/AuthContext.jsx";
import { auth } from '../../services/firebase.js';
import ThemeToggle from "../ThemeToggle";
import Logo from "../header/Logo";
import DesktopNav from "../header/DesktopNav";
import AuthButtons from "../header/AuthButtons";
import MobileMenu from "../header/MobileMenu";
import LogoutModal from "../header/LogoutModal";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();
  const { currentUser, isAuthenticated } = useAuth();

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  const handleNavigate = (path) => {
    navigate(path);
    setIsMenuOpen(false);
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      toast.success('Successfully logged out');
      navigate('/');
      setShowLogoutModal(false);
    } catch (error) {
      toast.error('Error logging out');
    }
  };

  return (
    <header className="bg-secondary shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Logo onClick={() => navigate('/')} />

          <DesktopNav onNavigate={navigate} />

          <div className="hidden md:flex items-center space-x-4">
            <ThemeToggle />
            <AuthButtons
              isAuthenticated={isAuthenticated}
              currentUser={currentUser}
              onProfile={() => navigate('/profile')}
              onLogout={() => setShowLogoutModal(true)}
              onLogin={() => navigate('/login')}
            />
          </div>

          <button onClick={toggleMenu} className="md:hidden text-text cursor-pointer">
            {isMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>
        </div>

        <MobileMenu
          isOpen={isMenuOpen}
          isAuthenticated={isAuthenticated}
          currentUser={currentUser}
          onNavigate={handleNavigate}
          onDashboard={() => handleNavigate('/profile')}
          onLogout={() => { setShowLogoutModal(true); setIsMenuOpen(false); }}
          onLogin={() => handleNavigate('/login')}
        />
      </div>

      <LogoutModal
        isOpen={showLogoutModal}
        onConfirm={handleLogout}
        onCancel={() => setShowLogoutModal(false)}
      />
    </header>
  );
};

export default Header;