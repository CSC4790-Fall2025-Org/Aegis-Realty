import { createContext, useContext, useState, useEffect } from 'react';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { app } from '../services/firebase';
import { useUserByFirebaseId } from '../hooks/useUserQueries';
import { useToast } from './ToastContext';

const auth = getAuth(app);

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [firebaseUser, setFirebaseUser] = useState(null);
  const [initialLoading, setInitialLoading] = useState(true);
  const toast = useToast();

  const {
    data: userData,
    error: userError,
    isLoading: userLoading,
    refetch: refetchUser
  } = useUserByFirebaseId(firebaseUser?.uid, {
    enabled: !!firebaseUser?.uid,
    onError: (error) => {
      toast.error(`Error fetching user data: ${error.message}`);
    }
  });

  const currentUser = firebaseUser ? {
    ...(userData || {}),
    firebaseUser
  } : null;

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setFirebaseUser(user);
      setInitialLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const updateUserData = () => {
    if (firebaseUser) {
      refetchUser();
    }
  };

  const value = {
    currentUser,
    loading: initialLoading || (!!firebaseUser && userLoading),
    isAuthenticated: !!currentUser,
    updateUserData
  };

  return (
    <AuthContext.Provider value={value}>
      {!initialLoading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};