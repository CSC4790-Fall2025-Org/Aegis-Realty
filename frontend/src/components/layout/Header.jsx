import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { FiMenu, FiX, FiUser, FiLogIn, FiLogOut } from 'react-icons/fi';
import AegisLogo from "../../assets/images/Aegis_Realty_Logo_Transparent.png";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <header className="bg-white/95 backdrop-blur-sm shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <button
            onClick={() => navigate('/')}
            className="flex items-center space-x-3 hover:opacity-80 transition-opacity"
          >
            <img
              src={AegisLogo}
              alt="Aegis Realty Logo"
              className="h-10 w-auto"
            />
            <span className="text-xl font-bold text-text">Aegis Realty</span>
          </button>

          <div className="hidden md:flex items-center space-x-8">
            <nav className="flex space-x-8">
              <button onClick={() => navigate("/properties")} className="text-text hover:text-primary transition-colors cursor-pointer">Properties</button>
              <button onClick={() => navigate("/services")} className="text-text hover:text-primary transition-colors cursor-pointer">Services</button>
              <button onClick={() => navigate("/contact")} className="text-text hover:text-primary transition-colors cursor-pointer">Contact</button>
            </nav>

            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center space-x-1 text-text hover:text-primary transition-colors cursor-pointer"
              >
                <FiUser className="w-5 h-5" />
                <span>Account</span>
              </button>

              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                  <button onClick={() => navigate("/login")} className="flex items-center px-4 py-2 text-sm text-text hover:bg-gray-100 w-full text-left cursor-pointer">
                    <FiLogIn className="w-4 h-4 mr-2" />
                    Login
                  </button>
                  <button onClick={() => navigate("/profile")} className="flex items-center px-4 py-2 text-sm text-text hover:bg-gray-100 w-full text-left cursor-pointer">
                    <FiUser className="w-4 h-4 mr-2" />
                    Profile
                  </button>
                  <button onClick={() => navigate("/logout")} className="flex items-center px-4 py-2 text-sm text-text hover:bg-gray-100 w-full text-left cursor-pointer">
                    <FiLogOut className="w-4 h-4 mr-2" />
                    Logout
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-text hover:text-primary"
            >
              {isMenuOpen ? <FiX className="w-6 h-6" /> : <FiMenu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <button onClick={() => navigate("/properties")} className="block px-3 py-2 text-text hover:text-primary w-full text-left">Properties</button>
              <button onClick={() => navigate("/services")} className="block px-3 py-2 text-text hover:text-primary w-full text-left">Services</button>
              <button onClick={() => navigate("/contact")} className="block px-3 py-2 text-text hover:text-primary w-full text-left">Contact</button>
              <div className="border-t border-gray-200 pt-2">
                <button onClick={() => navigate("/login")} className="block px-3 py-2 text-text hover:text-primary w-full text-left">Login</button>
                <button onClick={() => navigate("/profile")} className="block px-3 py-2 text-text hover:text-primary w-full text-left">Profile</button>
                <button onClick={() => navigate("/logout")} className="block px-3 py-2 text-text hover:text-primary w-full text-left">Logout</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;