// frontend/src/pages/Dashboard.jsx
import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { getSaludFinanciera } from "../api/api";
import Sidebar from "../components/Sidebar";
import {
  ArrowUpCircle,
  ArrowDownCircle,
  DollarSign,
  PiggyBank,
  CreditCard,
  Shield,
  TrendingUp,
  AlertCircle,
  Lightbulb,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

const Dashboard = () => {
  const { user } = useAuth();
  const [analisis, setAnalisis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dias, setDias] = useState(30);

  useEffect(() => {
    cargarAnalisis();
  }, [dias]);

  const cargarAnalisis = async () => {
    try {
      setLoading(true);
      const data = await getSaludFinanciera(user.usuario_id, dias);
      setAnalisis(data);
    } catch (error) {
      console.error("Error al cargar análisis:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={styles.layout}>
        <Sidebar />
        <div style={styles.mainContent}>
          <div style={styles.loadingCard}>
            <div style={styles.spinner}></div>
            <h2>Cargando análisis financiero</h2>
          </div>
        </div>
      </div>
    );
  }

  // Calcular semáforo
  const calcularSemaforo = () => {
    if (!analisis)
      return { status: "neutral", mensaje: "Sin datos", color: "#9e9e9e" };
    const porcentaje = analisis.puntuacion_general.porcentaje;

    if (porcentaje >= 75) {
      return {
        status: "Tu salud financiera es buena",
        color: "#10b981",
        icon: AlertCircle,
      };
    } else if (porcentaje >= 50) {
      return {
        status: "Tu salud financiera necesita atención",
        color: "#f59e0b",
        icon: AlertCircle,
      };
    } else {
      return {
        status: "Tu situación financiera requiere acción inmediata",
        color: "#ef4444",
        icon: AlertCircle,
      };
    }
  };

  const semaforo = calcularSemaforo();

  // Datos para gráfico de distribución (simulados por categoría)
  const datosDistribucion = [
    { name: "Vivienda", value: 1000000, color: "#667eea" },
    { name: "Alimentación", value: 600000, color: "#10b981" },
    { name: "Transporte", value: 400000, color: "#f59e0b" },
    { name: "Ocio", value: 500000, color: "#ef4444" },
    { name: "Otros", value: 300000, color: "#8b5cf6" },
  ];

  // Datos para gráfico de evolución (simulados)
  const datosEvolucion = [
    { mes: "Ene", ingresos: 3200000, gastos: 2600000 },
    { mes: "Feb", ingresos: 3400000, gastos: 2700000 },
    { mes: "Mar", ingresos: 3300000, gastos: 2800000 },
    { mes: "Abr", ingresos: 3500000, gastos: 2900000 },
    { mes: "May", ingresos: 3600000, gastos: 2750000 },
    { mes: "Jun", ingresos: 3500000, gastos: 2800000 },
  ];

  return (
    <div style={styles.layout}>
      <Sidebar />
      <div style={styles.mainContent}>
        <div style={styles.container}>
          {/* Header */}
          <div style={styles.header}>
            <div>
              <h1 style={styles.title}>Inicio</h1>
              <p style={styles.subtitle}>¡Hola {user?.nombre_completo}!</p>
            </div>
            <select
              value={dias}
              onChange={(e) => setDias(Number(e.target.value))}
              style={styles.select}
            >
              <option value={7}>Últimos 7 días</option>
              <option value={30}>Últimos 30 días</option>
              <option value={90}>Últimos 90 días</option>
              <option value={365}>Último año</option>
            </select>
          </div>

          {analisis && (
            <>
              {/* Resumen Financiero - 3 Cards */}
              <div style={styles.gridTres}>
                <CardResumen
                  titulo="Ingresos Totales"
                  valor={analisis.resumen_financiero.ingresos}
                  Icon={ArrowUpCircle}
                  color="#10b981"
                />
                <CardResumen
                  titulo="Gastos Totales"
                  valor={analisis.resumen_financiero.egresos}
                  Icon={ArrowDownCircle}
                  color="#ef4444"
                />
                <CardResumen
                  titulo="Balance"
                  valor={analisis.resumen_financiero.balance}
                  Icon={DollarSign}
                  color={
                    analisis.resumen_financiero.balance >= 0
                      ? "#10b981"
                      : "#ef4444"
                  }
                  destacado={true}
                />
              </div>

              {/* Indicadores Rápidos */}
              <div style={styles.gridTres}>
                <IndicadorCard
                  titulo="Ahorro Alcanzado"
                  Icon={PiggyBank}
                  porcentaje={8}
                  meta={10}
                  color="#667eea"
                />
                <IndicadorCard
                  titulo="Deudas sobre Ingresos"
                  Icon={CreditCard}
                  porcentaje={35}
                  meta={30}
                  color="#f59e0b"
                  warning={true}
                />
                <IndicadorCard
                  titulo="Fondo de Emergencia"
                  Icon={Shield}
                  valor={1200000}
                  meta="3 meses de gastos"
                  color="#10b981"
                />
              </div>

              {/* Gráficos */}
              <div style={styles.gridDos}>
                {/* Distribución de Gastos */}
                <div style={styles.card}>
                  <h3 style={styles.cardTitle}>Distribución de Gastos</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={datosDistribucion}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) =>
                          `${name} ${(percent * 100).toFixed(0)}%`
                        }
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {datosDistribucion.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip
                        formatter={(value) => `$${value.toLocaleString()}`}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                {/* Evolución Mensual */}
                <div style={styles.card}>
                  <h3 style={styles.cardTitle}>Evolución Mensual</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={datosEvolucion}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis
                        dataKey="mes"
                        stroke="#9ca3af"
                        style={{ fontSize: "12px" }}
                      />
                      <YAxis stroke="#9ca3af" style={{ fontSize: "12px" }} />
                      <Tooltip
                        formatter={(value) => `$${value.toLocaleString()}`}
                        contentStyle={{
                          background: "white",
                          border: "1px solid #e5e7eb",
                          borderRadius: "8px",
                        }}
                      />
                      <Legend />
                      <Bar dataKey="ingresos" fill="#10b981" name="Ingresos" />
                      <Bar dataKey="gastos" fill="#ef4444" name="Gastos" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Semáforo Financiero */}
              <div style={styles.card}>
                <h3 style={styles.cardTitle}>Semáforo Financiero</h3>
                <div style={styles.semaforoContent}>
                  <div
                    style={{
                      ...styles.semaforoIcon,
                      background: `${semaforo.color}15`,
                    }}
                  >
                    <semaforo.icon size={32} color={semaforo.color} />
                  </div>
                  <div style={styles.semaforoText}>
                    <h4
                      style={{
                        ...styles.semaforoStatus,
                        color: semaforo.color,
                      }}
                    >
                      {semaforo.status}
                    </h4>
                    <p style={styles.semaforoDesc}>
                      Puntuación: {analisis.puntuacion_general.porcentaje}% (
                      {analisis.puntuacion_general.cumplidas} de{" "}
                      {analisis.puntuacion_general.total} reglas cumplidas)
                    </p>
                  </div>
                </div>
              </div>

              {/* Recomendaciones */}
              <div style={styles.card}>
                <h3
                  style={{
                    ...styles.cardTitle,
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                  }}
                >
                  <Lightbulb size={20} color="#667eea" />
                  Recomendaciones Personalizadas del Sistema Experto
                </h3>
                <div style={styles.recomendaciones}>
                  {Object.entries(analisis.reglas)
                    .filter(([, regla]) => !regla.cumple)
                    .slice(0, 4)
                    .map(([key, regla]) => (
                      <RecomendacionCard key={key} nombre={key} regla={regla} />
                    ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

// Componentes auxiliares
const CardResumen = ({ titulo, valor, Icon, color, destacado }) => (
  <div
    style={{
      ...styles.card,
      ...(destacado ? { borderLeft: `4px solid ${color}` } : {}),
    }}
  >
    <div style={styles.cardHeader}>
      <p style={styles.cardLabel}>{titulo}</p>
      <Icon size={20} style={{ color }} />
    </div>
    <p style={{ ...styles.cardValor, color }}>
      ${Math.abs(valor).toLocaleString("es-CL")}
    </p>
    <p style={styles.cardFooter}>Este mes</p>
  </div>
);

const IndicadorCard = ({
  titulo,
  Icon,
  porcentaje,
  meta,
  valor,
  color,
  warning,
}) => (
  <div style={styles.card}>
    <div style={styles.cardHeader}>
      <p style={styles.cardLabel}>{titulo}</p>
      <Icon size={20} style={{ color }} />
    </div>
    {porcentaje !== undefined ? (
      <>
        <p style={{ ...styles.cardValor, color: warning ? "#f59e0b" : color }}>
          {porcentaje}%
        </p>
        <div style={styles.progressBar}>
          <div
            style={{
              ...styles.progressFill,
              width: `${Math.min(porcentaje, 100)}%`,
              background: color,
            }}
          ></div>
        </div>
        <p style={styles.cardFooter}>Recomendado: {meta}%</p>
      </>
    ) : (
      <>
        <p style={{ ...styles.cardValor, color }}>
          ${valor?.toLocaleString("es-CL")}
        </p>
        <p style={styles.cardFooter}>Meta: {meta}</p>
      </>
    )}
  </div>
);

const RecomendacionCard = ({ nombre, regla }) => {
  const getColor = () => {
    if (regla.severidad === "danger") return "#ef4444";
    if (regla.severidad === "warning") return "#f59e0b";
    return "#10b981";
  };

  const getIcon = () => {
    if (regla.severidad === "danger") return "🚨";
    if (regla.severidad === "warning") return "⚠️";
    return "💡";
  };

  return (
    <div
      style={{
        ...styles.recomendacionCard,
        borderLeft: `4px solid ${getColor()}`,
      }}
    >
      <div style={styles.recomendacionHeader}>
        <span style={styles.recomendacionIcon}>{getIcon()}</span>
        <h4 style={styles.recomendacionTitulo}>
          {nombre.replace(/_/g, " ").replace(/regla /gi, "")}
        </h4>
      </div>
      <p style={styles.recomendacionMensaje}>{regla.mensaje}</p>
    </div>
  );
};

const styles = {
  layout: {
    display: "flex",
    minHeight: "100vh",
    background: "#f9fafb",
  },
  mainContent: {
    flex: 1,
    marginLeft: "280px",
    padding: "32px",
  },
  container: {
    maxWidth: "1400px",
    margin: "0 auto",
  },
  loadingCard: {
    background: "white",
    padding: "60px",
    borderRadius: "12px",
    boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
    textAlign: "center",
  },
  spinner: {
    width: "50px",
    height: "50px",
    margin: "0 auto 20px",
    border: "4px solid #f3f3f3",
    borderTop: "4px solid #667eea",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "32px",
  },
  title: {
    fontSize: "28px",
    fontWeight: "700",
    color: "#111827",
    marginBottom: "4px",
  },
  subtitle: {
    fontSize: "14px",
    color: "#6b7280",
  },
  select: {
    padding: "10px 16px",
    borderRadius: "8px",
    border: "1px solid #e5e7eb",
    background: "white",
    fontSize: "14px",
    cursor: "pointer",
    color: "#374151",
  },
  gridTres: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: "20px",
    marginBottom: "24px",
  },
  gridDos: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(450px, 1fr))",
    gap: "20px",
    marginBottom: "24px",
  },
  card: {
    background: "white",
    padding: "24px",
    borderRadius: "12px",
    boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
    border: "1px solid #e5e7eb",
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "12px",
  },
  cardLabel: {
    fontSize: "13px",
    fontWeight: "500",
    color: "#6b7280",
    margin: 0,
  },
  cardTitle: {
    fontSize: "16px",
    fontWeight: "600",
    color: "#111827",
    marginBottom: "20px",
  },
  cardValor: {
    fontSize: "28px",
    fontWeight: "700",
    marginBottom: "8px",
  },
  cardFooter: {
    fontSize: "12px",
    color: "#9ca3af",
    margin: 0,
  },
  progressBar: {
    width: "100%",
    height: "8px",
    background: "#e5e7eb",
    borderRadius: "4px",
    overflow: "hidden",
    margin: "12px 0 8px",
  },
  progressFill: {
    height: "100%",
    borderRadius: "4px",
    transition: "width 0.3s",
  },
  semaforoContent: {
    display: "flex",
    alignItems: "center",
    gap: "20px",
    marginTop: "16px",
  },
  semaforoIcon: {
    width: "64px",
    height: "64px",
    borderRadius: "12px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  semaforoText: {
    flex: 1,
  },
  semaforoStatus: {
    fontSize: "18px",
    fontWeight: "600",
    marginBottom: "4px",
  },
  semaforoDesc: {
    fontSize: "13px",
    color: "#6b7280",
    margin: 0,
  },
  recomendaciones: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    marginTop: "16px",
  },
  recomendacionCard: {
    padding: "16px",
    background: "#f9fafb",
    borderRadius: "8px",
  },
  recomendacionHeader: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    marginBottom: "8px",
  },
  recomendacionIcon: {
    fontSize: "20px",
  },
  recomendacionTitulo: {
    fontSize: "14px",
    fontWeight: "600",
    color: "#111827",
    margin: 0,
    textTransform: "capitalize",
  },
  recomendacionMensaje: {
    fontSize: "13px",
    color: "#6b7280",
    lineHeight: "1.5",
    margin: 0,
    paddingLeft: "32px",
  },
};

export default Dashboard;
