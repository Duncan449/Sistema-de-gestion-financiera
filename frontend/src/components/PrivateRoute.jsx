// frontend/src/components/PrivateRoute.jsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();

  // Si no está autenticado, redirige al login
  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
