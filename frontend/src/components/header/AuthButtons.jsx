import { FiLogIn } from 'react-icons/fi';
import UserMenu from './UserMenu';

const AuthButtons = ({ isAuthenticated, currentUser, onLogout, onLogin, onProfile }) => {
  if (isAuthenticated) {
    return <UserMenu currentUser={currentUser} onProfile={onProfile} onLogout={onLogout} />;
  }

  return (
    <button
      onClick={onLogin}
      className="flex items-center space-x-2 bg-primary text-white px-4 py-2 rounded-md hover:bg-opacity-90 transition-colors cursor-pointer"
    >
      <FiLogIn size={20} />
      <span>Login</span>
    </button>
  );
};

export default AuthButtons;