import { FiUser, FiLogIn, FiLogOut } from 'react-icons/fi';

const AuthButtons = ({ isAuthenticated, currentUser, onDashboard, onLogout, onLogin }) => {
  if (isAuthenticated) {
    return (
      <div className="flex items-center space-x-3">
        <button
          onClick={onDashboard}
          className="flex items-center space-x-2 text-text hover:text-primary transition-colors cursor-pointer"
        >
          <FiUser size={20} />
          <span>{currentUser?.username || currentUser?.email}</span>
        </button>
        <button
          onClick={onLogout}
          className="flex items-center space-x-2 text-text hover:text-red-500 transition-colors cursor-pointer"
        >
          <FiLogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={onLogin}
      className="flex items-center space-x-2 bg-primary text-white px-4 py-2 rounded-md
      hover:bg-primary/70 transition-colors cursor-pointer"
    >
      <FiLogIn size={20} />
      <span>Login</span>
    </button>
  );
};

export default AuthButtons;