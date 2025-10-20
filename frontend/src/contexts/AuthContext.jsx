import React, { createContext, useState } from 'react';


// Create the AuthContext
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  // Example login function
  const login = async (userData) => {
    setLoading(true);
    // Simulate authentication logic
    setTimeout(() => {
      setUser(userData);
      setLoading(false);
    }, 1000);
  };

  // Example logout function
  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
