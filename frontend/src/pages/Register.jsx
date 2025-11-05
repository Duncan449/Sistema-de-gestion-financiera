// frontend/src/pages/Register.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../api/api";
import {
  User,
  Mail,
  Lock,
  UserPlus,
  AlertCircle,
  CheckCircle2,
  FileEdit,
} from "lucide-react";

const Register = () => {
  const [formData, setFormData] = useState({
    nombre_completo: "",
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validación de contraseñas
    if (formData.password !== formData.confirmPassword) {
      setError("Las contraseñas no coinciden");
      return;
    }

    // Validación de longitud de contraseña
    if (formData.password.length < 6) {
      setError("La contraseña debe tener al menos 6 caracteres");
      return;
    }

    setLoading(true);

    try {
      await register(
        formData.nombre_completo,
        formData.email,
        formData.username,
        formData.password
      );

      setSuccess(true);

      // Redirigir después de 2 segundos
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || "Error al registrarse");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div style={styles.container}>
        <div style={styles.backgroundDecoration}></div>
        <div style={styles.card}>
          <div style={styles.successContainer}>
            <div style={styles.successIcon}>
              <CheckCircle2 size={48} color="#10b981" />
            </div>
            <h2 style={styles.successTitle}>¡Cuenta creada exitosamente!</h2>
            <p style={styles.successText}>Redirigiendo al login...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Background decorativo */}
      <div style={styles.backgroundDecoration}></div>

      <div style={styles.card}>
        {/* Logo y Header */}
        <div style={styles.header}>
          <div style={styles.logoContainer}>
            <div style={styles.logo}>
              <FileEdit size={28} color="white" />
            </div>
          </div>
          <h1 style={styles.title}>Crear Cuenta</h1>
          <p style={styles.subtitle}>Sistema Financiero</p>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          {/* Nombre Completo */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <User size={16} />
              Nombre Completo
            </label>
            <input
              type="text"
              name="nombre_completo"
              value={formData.nombre_completo}
              onChange={handleChange}
              required
              style={styles.input}
              placeholder="Juan Pérez"
            />
          </div>

          {/* Email */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <Mail size={16} />
              Email
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              style={styles.input}
              placeholder="tu@email.com"
            />
          </div>

          {/* Username */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <UserPlus size={16} />
              Nombre de Usuario
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              style={styles.input}
              placeholder="usuario123"
            />
          </div>

          {/* Password */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <Lock size={16} />
              Contraseña
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              style={styles.input}
              placeholder="••••••••"
            />
            <p style={styles.hint}>Mínimo 6 caracteres</p>
          </div>

          {/* Confirmar Password */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <Lock size={16} />
              Confirmar Contraseña
            </label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              style={styles.input}
              placeholder="••••••••"
            />
          </div>

          {/* Error Message */}
          {error && (
            <div style={styles.errorBox}>
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.button,
              opacity: loading ? 0.7 : 1,
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Creando cuenta..." : "Registrarse"}
          </button>
        </form>

        {/* Footer */}
        <div style={styles.footer}>
          <p style={styles.footerText}>
            ¿Ya tienes cuenta?{" "}
            <Link to="/login" style={styles.link}>
              Inicia sesión aquí
            </Link>
          </p>
        </div>
      </div>

      {/* Info adicional */}
      <p style={styles.bottomText}>Sistema Experto de Educación Financiera</p>
    </div>
  );
};

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    padding: "20px",
    position: "relative",
    overflow: "hidden",
  },
  backgroundDecoration: {
    position: "absolute",
    top: "-50%",
    right: "-10%",
    width: "600px",
    height: "600px",
    background: "rgba(255, 255, 255, 0.1)",
    borderRadius: "50%",
    filter: "blur(80px)",
  },
  card: {
    background: "white",
    padding: "48px",
    borderRadius: "16px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
    width: "100%",
    maxWidth: "420px",
    position: "relative",
    zIndex: 1,
  },
  header: {
    textAlign: "center",
    marginBottom: "32px",
  },
  logoContainer: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "20px",
  },
  logo: {
    width: "60px",
    height: "60px",
    borderRadius: "14px",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 8px 20px rgba(102, 126, 234, 0.4)",
  },
  title: {
    fontSize: "26px",
    fontWeight: "700",
    color: "#111827",
    marginBottom: "8px",
  },
  subtitle: {
    fontSize: "15px",
    color: "#6b7280",
    fontWeight: "500",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
  inputGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  label: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontSize: "14px",
    fontWeight: "600",
    color: "#374151",
  },
  input: {
    width: "100%",
    padding: "12px 16px",
    border: "1px solid #e5e7eb",
    borderRadius: "8px",
    fontSize: "14px",
    transition: "all 0.2s",
    color: "#111827",
    background: "#f9fafb",
  },
  hint: {
    fontSize: "12px",
    color: "#9ca3af",
    marginTop: "-4px",
  },
  errorBox: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    background: "#fef2f2",
    border: "1px solid #fecaca",
    color: "#dc2626",
    padding: "12px 16px",
    borderRadius: "8px",
    fontSize: "13px",
    fontWeight: "500",
  },
  button: {
    width: "100%",
    padding: "14px",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "15px",
    fontWeight: "600",
    cursor: "pointer",
    transition: "all 0.2s",
    marginTop: "8px",
  },
  footer: {
    marginTop: "24px",
    paddingTop: "20px",
    borderTop: "1px solid #f3f4f6",
    textAlign: "center",
  },
  footerText: {
    fontSize: "14px",
    color: "#6b7280",
  },
  link: {
    color: "#667eea",
    textDecoration: "none",
    fontWeight: "600",
    transition: "color 0.2s",
  },
  bottomText: {
    marginTop: "24px",
    fontSize: "13px",
    color: "rgba(255, 255, 255, 0.8)",
    textAlign: "center",
    position: "relative",
    zIndex: 1,
  },
  // Estilos para pantalla de éxito
  successContainer: {
    textAlign: "center",
    padding: "20px",
  },
  successIcon: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "24px",
  },
  successTitle: {
    fontSize: "22px",
    fontWeight: "700",
    color: "#111827",
    marginBottom: "12px",
  },
  successText: {
    fontSize: "14px",
    color: "#6b7280",
  },
};

export default Register;
