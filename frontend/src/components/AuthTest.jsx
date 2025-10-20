import React, { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext.jsx';

const AuthTest = () => {
  const { user, loading, login, logout } = useContext(AuthContext);

  return (
    <div style={{ padding: '2rem', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>AuthContext Test</h2>
      <div>
        <strong>User:</strong> {user ? JSON.stringify(user) : 'None'}
      </div>
      <div>
        <strong>Loading:</strong> {loading ? 'Yes' : 'No'}
      </div>
      <button onClick={() => login({ name: 'Test User', email: 'test@example.com' })} disabled={loading}>
        Login as Test User
      </button>
      <button onClick={logout} disabled={loading || !user} style={{ marginLeft: '1rem' }}>
        Logout
      </button>
    </div>
  );
};

export default AuthTest;
