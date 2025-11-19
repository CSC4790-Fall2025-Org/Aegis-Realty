import { FiUser, FiLogIn, FiLogOut } from 'react-icons/fi';
import ThemeToggle from "../ThemeToggle";

const MobileMenu = ({
  isOpen,
  isAuthenticated,
  currentUser,
  onNavigate,
  onDashboard,
  onLogout,
  onLogin
}) => {
  if (!isOpen) return null;

  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Properties', path: '/properties' },
    { label: 'Analyze', path: '/analyze' },
  ];

  return (
    <div className="md:hidden mt-4 space-y-2">
      {navItems.map(({ label, path }) => (
        <button
          key={path}
          onClick={() => onNavigate(path)}
          className="block w-full text-left px-4 py-2 text-text hover:bg-background rounded cursor-pointer"
        >
          {label}
        </button>
      ))}

      <div className="border-t border-gray-300 pt-2 mt-2">
        {isAuthenticated ? (
          <>
            <button
              onClick={onDashboard}
              className="flex items-center space-x-2 w-full px-4 py-2 text-text hover:bg-background rounded cursor-pointer"
            >
              <FiUser size={20} />
              <span>{currentUser?.username || currentUser?.email}</span>
            </button>
            <button
              onClick={onLogout}
              className="flex items-center space-x-2 w-full px-4 py-2 text-text hover:bg-background rounded cursor-pointer"
            >
              <FiLogOut size={20} />
              <span>Logout</span>
            </button>
          </>
        ) : (
          <button
            onClick={onLogin}
            className="flex items-center space-x-2 w-full px-4 py-2 bg-primary text-white rounded hover:bg-opacity-90 cursor-pointer"
          >
            <FiLogIn size={20} />
            <span>Login</span>
          </button>
        )}
        <div className="px-4 py-2">
          <ThemeToggle />
        </div>
      </div>
    </div>
  );
};

export default MobileMenu;