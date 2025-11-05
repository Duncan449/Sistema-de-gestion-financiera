// frontend/src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import PrivateRoute from "./components/PrivateRoute";

// Páginas
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Ingresos from "./pages/Ingresos";
import Egresos from "./pages/Egresos";
import Activos from "./pages/Activos";
import Pasivos from "./pages/Pasivos";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Rutas públicas */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Rutas protegidas */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/ingresos"
            element={
              <PrivateRoute>
                <Ingresos />
              </PrivateRoute>
            }
          />

          <Route
            path="/egresos"
            element={
              <PrivateRoute>
                <Egresos />
              </PrivateRoute>
            }
          />

          <Route
            path="/activos"
            element={
              <PrivateRoute>
                <Activos />
              </PrivateRoute>
            }
          />

          <Route
            path="/pasivos"
            element={
              <PrivateRoute>
                <Pasivos />
              </PrivateRoute>
            }
          />

          {/* Redirigir a login si no hay ruta */}
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
