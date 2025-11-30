import { createContext, useContext, useState, useEffect } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '../services/firebase';
import { useUserByFirebaseId, useCreateUser } from '../hooks/useUserQueries.js'
import { useToast } from './ToastContext';

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
      // If user not found, auto-provision in backend
      if (error?.response?.status === 404 && firebaseUser) {
        const displayName = firebaseUser.displayName || firebaseUser.email?.split('@')[0] || '';
        createUserMutation.mutate({
          firebase_id: firebaseUser.uid,
          email: firebaseUser.email,
          display_name: displayName,
        });
      } else {
        toast.error(`Error fetching user data: ${error.message}`);
      }
    }
  });

  const createUserMutation = useCreateUser({
    onSuccess: () => {
      toast.success('Account initialized');
      // Refresh to pull favorites and other server fields
      refetchUser();
    },
    onError: (e) => {
      toast.error(e?.response?.data?.detail || 'Failed to initialize account');
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