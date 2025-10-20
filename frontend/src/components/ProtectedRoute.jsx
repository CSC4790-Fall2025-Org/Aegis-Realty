import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useAuth();

  if (loading) return <div>Loading...</div>;

  if (!currentUser) {
    alert("Please login before accessing this page");
    return <Navigate to="/login"/>;
  }

  return children;
};

export default ProtectedRoute;