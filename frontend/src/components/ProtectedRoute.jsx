import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext.jsx'
import Spinner from './Spinner.jsx'

const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useAuth();
  const location = useLocation();

  if (loading) return (
    <div>
      <Spinner/>
    </div>
  );

  if (!currentUser) {
    return (
      <Navigate
        to="/login"
        state={{ from: location, message: 'Please login before accessing this page' }}
        replace
      />
    );
  }

  return children;
};

export default ProtectedRoute;