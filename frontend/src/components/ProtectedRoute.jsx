import { useEffect, useRef } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext.jsx'
import Spinner from './Spinner.jsx'
import { useToast } from "../contexts/ToastContext.jsx";

const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useAuth();
  const location = useLocation();
  const { error } = useToast();
  const hasShownToast = useRef(false);

  useEffect(() => {
    if (!loading && !currentUser && !hasShownToast.current) {
      error('Please login before accessing this page');
      hasShownToast.current = true;
    }
  }, [loading, currentUser, error]);

  if (loading) return (
    <div>
      <Spinner/>
    </div>
  );

  if (!currentUser) {
    return (
      <Navigate
        to="/login"
        state={{ from: location.pathname }}
        replace
      />
    );
  }

  return children;
};

export default ProtectedRoute;