// frontend/src/components/Sidebar.jsx
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  Home,
  TrendingUp,
  TrendingDown,
  CreditCard,
  LogOut,
  User,
  DollarSign,
  Landmark,
} from "lucide-react";

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logoutUser } = useAuth();

  const handleLogout = () => {
    logoutUser();
    navigate("/login");
  };

  const menuItems = [
    { icon: Home, label: "Inicio", path: "/dashboard" },
    { icon: TrendingUp, label: "Ingresos", path: "/ingresos" },
    { icon: TrendingDown, label: "Egresos", path: "/egresos" },
    { icon: Landmark, label: "Activos", path: "/activos" },
    { icon: CreditCard, label: "Pasivos", path: "/pasivos" },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div style={styles.sidebar}>
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.logo}>
          <div style={styles.logoIcon}>
            <DollarSign size={24} color="white" />
          </div>
          <span style={styles.logoText}>
            Sistema Experto de Educación Financiera
          </span>
        </div>
      </div>

      {/* Menu */}
      <nav style={styles.nav}>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);

          return (
            <Link
              key={item.path}
              to={item.path}
              style={{
                ...styles.menuItem,
                ...(active ? styles.menuItemActive : {}),
              }}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* User section */}
      <div style={styles.userSection}>
        <div style={styles.userInfo}>
          <div style={styles.avatar}>
            <User size={16} />
          </div>
          <div style={styles.userText}>
            <p style={styles.userName}>{user?.nombre_completo}</p>
            <p style={styles.userEmail}>{user?.email}</p>
          </div>
        </div>
        <button onClick={handleLogout} style={styles.logoutBtn}>
          <LogOut size={18} />
        </button>
      </div>
    </div>
  );
};

const styles = {
  sidebar: {
    width: "280px",
    height: "100vh",
    background: "white",
    borderRight: "1px solid #e5e7eb",
    display: "flex",
    flexDirection: "column",
    position: "fixed",
    left: 0,
    top: 0,
    zIndex: 100,
  },
  header: {
    padding: "20px",
    borderBottom: "1px solid #e5e7eb",
  },
  logo: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
  },
  logoIcon: {
    width: "40px",
    height: "40px",
    borderRadius: "8px",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  logoText: {
    fontSize: "15px",
    fontWeight: "600",
    color: "#1f2937",
    lineHeight: "1.3",
  },
  nav: {
    padding: "20px 12px",
    flex: 1,
    overflowY: "auto",
  },
  menuItem: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "12px 16px",
    borderRadius: "8px",
    color: "#6b7280",
    textDecoration: "none",
    marginBottom: "4px",
    fontSize: "15px",
    fontWeight: "500",
    transition: "all 0.2s",
    cursor: "pointer",
  },
  menuItemActive: {
    background: "#f3f4f6",
    color: "#667eea",
    fontWeight: "600",
  },
  userSection: {
    padding: "16px",
    borderTop: "1px solid #e5e7eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: "12px",
  },
  userInfo: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    flex: 1,
    minWidth: 0,
  },
  avatar: {
    width: "36px",
    height: "36px",
    borderRadius: "8px",
    background: "#667eea",
    color: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  userText: {
    flex: 1,
    minWidth: 0,
  },
  userName: {
    fontSize: "14px",
    fontWeight: "600",
    color: "#1f2937",
    margin: 0,
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  userEmail: {
    fontSize: "12px",
    color: "#9ca3af",
    margin: 0,
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  logoutBtn: {
    width: "36px",
    height: "36px",
    borderRadius: "8px",
    border: "1px solid #e5e7eb",
    background: "white",
    color: "#6b7280",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    transition: "all 0.2s",
    flexShrink: 0,
  },
};

export default Sidebar;
