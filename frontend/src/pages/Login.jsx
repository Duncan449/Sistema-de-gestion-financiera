// frontend/src/pages/Login.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { login } from "../api/api";
import { Mail, Lock, DollarSign, AlertCircle, ArrowRight } from "lucide-react";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login(email, password);

      loginUser(
        {
          usuario_id: data.usuario_id,
          email: data.email,
          nombre_completo: data.nombre_completo,
        },
        data.access_token
      );

      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Error al iniciar sesión");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Background decorativo */}
      <div style={styles.backgroundDecoration}></div>

      <div style={styles.card}>
        {/* Logo y Header */}
        <div style={styles.header}>
          <div style={styles.logoContainer}>
            <div style={styles.logo}>
              <DollarSign size={28} color="white" />
            </div>
          </div>
          <h1 style={styles.title}>Sistema Financiero</h1>
          <p style={styles.subtitle}>Iniciar Sesión</p>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          {/* Email Input */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <Mail size={16} />
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={styles.input}
              placeholder="tu@email.com"
            />
          </div>

          {/* Password Input */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <Lock size={16} />
              Contraseña
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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
            {loading ? (
              "Cargando..."
            ) : (
              <>
                Ingresar
                <ArrowRight size={18} />
              </>
            )}
          </button>
        </form>

        {/* Footer */}
        <div style={styles.footer}>
          <p style={styles.footerText}>
            ¿No tienes cuenta?{" "}
            <Link to="/register" style={styles.link}>
              Regístrate aquí
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
    gap: "20px",
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
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    marginTop: "8px",
  },
  footer: {
    marginTop: "32px",
    paddingTop: "24px",
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
};

export default Login;
