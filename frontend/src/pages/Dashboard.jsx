// frontend/src/pages/Dashboard.jsx
import { useState, useEffect, useCallback } from "react";
import { useAuth } from "../context/AuthContext";
import { getSaludFinanciera, getDistribucionGastos } from "../api/api";
import Sidebar from "../components/Sidebar";
import {
  ArrowUpCircle,
  ArrowDownCircle,
  DollarSign,
  PiggyBank,
  CreditCard,
  Shield,
  TrendingUp,
  AlertTriangle,
  AlertCircle,
  AlertOctagon,
  Lightbulb,
  CheckCircle,
  XCircle,
  Info,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
} from "recharts";

const Dashboard = () => {
  const { user } = useAuth();

  // --- Estados principales ---
  const [analisis, setAnalisis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dias, setDias] = useState(30);
  const [expandedRules, setExpandedRules] = useState({});
  const [datosDistribucion, setDatosDistribucion] = useState([]);

  // --- Funciones ---
  const cargarAnalisis = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getSaludFinanciera(user.usuario_id, dias);
      setAnalisis(data);
    } catch (error) {
      console.error("Error al cargar análisis:", error);
    } finally {
      setLoading(false);
    }
  }, [user, dias]);

  // --- useEffects ---
  useEffect(() => {
    cargarAnalisis();
  }, [cargarAnalisis]);

  useEffect(() => {
    const usuarioId = user?.usuario_id || localStorage.getItem("usuarioId");
    if (!usuarioId) return;

    getDistribucionGastos(usuarioId)
      .then((data) => {
        if (!data?.distribucion) return;
        const formateado = data.distribucion.map((item) => ({
          name: item.categoria,
          value: item.monto,
          color: "#" + Math.floor(Math.random() * 16777215).toString(16),
        }));
        setDatosDistribucion(formateado);
      })
      .catch((error) =>
        console.error("Error al obtener distribución de gastos:", error)
      );
  }, [user]);

  const toggleRule = (ruleKey) => {
    setExpandedRules((prev) => ({
      ...prev,
      [ruleKey]: !prev[ruleKey],
    }));
  };

  // --- Loader ---
  if (loading) {
    return (
      <div style={styles.layout}>
        <Sidebar />
        <div style={styles.mainContent}>
          <div style={styles.loadingCard}>
            <div style={styles.spinner}></div>
            <h2>Cargando análisis financiero...</h2>
          </div>
        </div>
      </div>
    );
  }

  // --- Cálculo de semáforo ---
  const calcularSemaforo = () => {
    if (!analisis)
      return { status: "neutral", mensaje: "Sin datos", color: "#9e9e9e" };

    const porcentaje = analisis.puntuacion_general.porcentaje;

    if (porcentaje >= 75) {
      return {
        status: "Excelente",
        mensaje: "Tu salud financiera es buena",
        color: "#10b981",
        icon: CheckCircle,
      };
    } else if (porcentaje >= 50) {
      return {
        status: "Atención",
        mensaje: "Tu salud financiera necesita mejoras",
        color: "#f59e0b",
        icon: AlertCircle,
      };
    } else {
      return {
        status: "Crítico",
        mensaje: "Tu situación financiera requiere acción inmediata",
        color: "#ef4444",
        icon: XCircle,
      };
    }
  };

  const semaforo = calcularSemaforo();

  // Obtener datos de evolución mensual desde la API
  const datosEvolucion = analisis?.evolucion_mensual || [];

  // Mapeo de nombres de reglas a títulos legibles
  const nombreReglas = {
    regla_50_30_20: {
      titulo: "Regla 50/30/20",
      descripcion: "50% necesidades, 30% deseos, 20% ahorro/inversión",
      icon: PiggyBank,
    },
    limite_endeudamiento: {
      titulo: "Límite de Endeudamiento",
      descripcion: "Las deudas no deben superar el 40% de ingresos",
      icon: CreditCard,
    },
    gasta_mas_que_gana: {
      titulo: "Balance Financiero",
      descripcion: "Tus gastos no deben superar tus ingresos",
      icon: TrendingUp,
    },
    fondo_emergencia: {
      titulo: "Fondo de Emergencia",
      descripcion: "Ahorro equivalente a 3-6 meses de gastos",
      icon: Shield,
    },
    sin_inversiones: {
      titulo: "Activos e Inversiones",
      descripcion: "Poseer activos que generen valor",
      icon: DollarSign,
    },
    inversion_educacion: {
      titulo: "Inversión en Educación",
      descripcion: "Al menos 5% de ingresos en desarrollo personal",
      icon: Lightbulb,
    },
    lujos_vs_educacion: {
      titulo: "Prioridades Financieras",
      descripcion: "Priorizar educación/activos sobre lujos",
      icon: Info,
    },
    reserva_imprevistos: {
      titulo: "Reserva para Imprevistos",
      descripcion: "Al menos 1 mes de ingresos en ahorro líquido",
      icon: AlertCircle,
    },
  };

  const getColorBySeverity = (severity) => {
    switch (severity) {
      case "success":
        return "#10b981";
      case "warning":
        return "#f59e0b";
      case "danger":
        return "#ef4444";
      default:
        return "#6b7280";
    }
  };

  const getIconBySeverity = (severity) => {
    switch (severity) {
      case "success":
        return CheckCircle;
      case "warning":
        return AlertCircle;
      case "danger":
        return XCircle;
      default:
        return Info;
    }
  };

  const getRecomendacion = (ruleKey) => {
    const recomendaciones = {
      regla_50_30_20:
        "Intenta ajustar tus gastos para cumplir con la regla 50/30/20. Reduce gastos innecesarios y aumenta tu ahorro.",
      limite_endeudamiento:
        "Considera consolidar deudas o aumentar pagos mensuales para reducir el nivel de endeudamiento.",
      gasta_mas_que_gana:
        "Urgente: Revisa tus gastos y elimina lo no esencial. Busca formas de aumentar tus ingresos.",
      fondo_emergencia:
        "Destina un porcentaje fijo de tus ingresos mensualmente hasta alcanzar 3-6 meses de gastos.",
      sin_inversiones:
        "Comienza a invertir aunque sea con montos pequeños. Considera fondos mutuos o ETFs para principiantes.",
      inversion_educacion:
        "Invierte en cursos, libros o certificaciones que mejoren tus habilidades profesionales.",
      lujos_vs_educacion:
        "Revalúa tus prioridades de gasto. Los activos y la educación generan valor a largo plazo.",
      reserva_imprevistos:
        "Crea una cuenta de ahorros separada específicamente para emergencias menores.",
    };

    return (
      recomendaciones[ruleKey] ||
      "Consulta con un asesor financiero para mejorar esta área."
    );
  };

  const renderDescripcion = (texto) => {
    if (typeof texto !== "string") return texto;

    // Expresión regular que elimina cualquier emoji o símbolo no textual
    const textoLimpio = texto
      .replace(
        /([\u2700-\u27BF]|[\uE000-\uF8FF]|[\uD83C-\uDBFF][\uDC00-\uDFFF]|\uFE0F|\u200D)/g,
        ""
      )
      .trim();

    return <p style={styles.reglaDescripcion}>{textoLimpio}</p>;
  };

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
                  destacado={false}
                />
              </div>

              {/* Indicadores Rápidos */}
              {analisis && (
                <div style={styles.gridTres}>
                  {/* Ahorro Alcanzado */}
                  <IndicadorCard
                    titulo="Ahorro Alcanzado"
                    Icon={PiggyBank}
                    porcentaje={
                      analisis.reglas?.regla_50_30_20?.porcentajes?.ahorros || 0
                    }
                    meta={20}
                    color="#667eea"
                  />

                  {/* Deudas sobre Ingresos */}
                  <IndicadorCard
                    titulo="Deudas sobre Ingresos"
                    Icon={CreditCard}
                    porcentaje={
                      analisis.reglas?.limite_endeudamiento?.porcentaje_deuda ||
                      0
                    }
                    meta={40}
                    color="#f59e0b"
                    warning={
                      (analisis.reglas?.limite_endeudamiento
                        ?.porcentaje_deuda || 0) > 40
                    }
                  />

                  {/* Fondo de Emergencia */}
                  <IndicadorCard
                    titulo="Fondo de Emergencia"
                    Icon={Shield}
                    valor={analisis.reglas?.fondo_emergencia?.monto_fondo || 0}
                    meta="3 meses de gastos"
                    color={
                      analisis.reglas?.fondo_emergencia?.cumple
                        ? "#10b981"
                        : "#f59e0b"
                    }
                  />
                </div>
              )}

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
                  {datosEvolucion.length > 0 ? (
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
                        <Bar
                          dataKey="ingresos"
                          fill="#10b981"
                          name="Ingresos"
                        />
                        <Bar dataKey="gastos" fill="#ef4444" name="Gastos" />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div
                      style={{
                        padding: "40px",
                        textAlign: "center",
                        color: "#9ca3af",
                      }}
                    >
                      <p>
                        No hay datos de evolución para el período seleccionado
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Semáforo Financiero Mejorado */}
              <div style={styles.card}>
                <h3 style={styles.cardTitle}>Evaluación General</h3>
                <div style={styles.semaforoContent}>
                  <div
                    style={{
                      ...styles.semaforoIcon,
                      background: `${semaforo.color}15`,
                    }}
                  >
                    <semaforo.icon size={48} color={semaforo.color} />
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
                    <p style={styles.semaforoDesc}>{semaforo.mensaje}</p>
                    <div style={styles.scoreBar}>
                      <div style={styles.scoreBarBg}>
                        <div
                          style={{
                            ...styles.scoreBarFill,
                            width: `${analisis.puntuacion_general.porcentaje}%`,
                            background: semaforo.color,
                          }}
                        ></div>
                      </div>
                      <p style={styles.scoreText}>
                        {analisis.puntuacion_general.cumplidas} de{" "}
                        {analisis.puntuacion_general.total} reglas cumplidas (
                        {analisis.puntuacion_general.porcentaje}%)
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recomendaciones Rápidas (las que ya tenías) */}
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
                  Recomendaciones Prioritarias
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

              {/* NUEVA SECCIÓN: Evaluación Detallada por Regla */}

              <div style={styles.card}>
                <h3
                  style={{
                    ...styles.cardTitle,
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                  }}
                >
                  <AlertCircle size={20} color="#667eea" />
                  Evaluación Detallada de Salud Financiera
                </h3>
                <p style={styles.evaluacionSubtitle}>
                  Análisis completo basado en{" "}
                  {analisis.puntuacion_general.total} reglas del sistema
                  experto. Haz clic en cada regla para ver más detalles.
                </p>

                <div style={styles.reglasGrid}>
                  {Object.entries(analisis.reglas).map(([key, regla]) => {
                    const info = nombreReglas[key];
                    const Icon = info?.icon || Info;
                    const StatusIcon = getIconBySeverity(regla.severidad);
                    const color = getColorBySeverity(regla.severidad);
                    const isExpanded = expandedRules[key];

                    return (
                      <div
                        key={key}
                        style={{
                          ...styles.reglaCard,
                          borderLeft: `4px solid ${color}`,
                        }}
                      >
                        {/* Header de la regla */}
                        <div
                          style={styles.reglaHeader}
                          onClick={() => toggleRule(key)}
                        >
                          <div style={styles.reglaHeaderLeft}>
                            <div
                              style={{
                                ...styles.reglaIconContainer,
                                background: `${color}15`,
                              }}
                            >
                              <Icon size={20} color={color} />
                            </div>
                            <div>
                              <h4 style={styles.reglaTitulo}>
                                {info?.titulo || key}
                              </h4>
                              {renderDescripcion(info?.descripcion)}
                            </div>
                          </div>
                          <div style={styles.reglaHeaderRight}>
                            <StatusIcon size={24} color={color} />
                            {isExpanded ? (
                              <ChevronUp size={20} color="#9ca3af" />
                            ) : (
                              <ChevronDown size={20} color="#9ca3af" />
                            )}
                          </div>
                        </div>

                        {/* Contenido expandible */}
                        {isExpanded && (
                          <div style={styles.reglaContent}>
                            <div style={styles.reglaMensaje}>
                              <p style={styles.reglaMensajeText}>
                                {regla.mensaje}
                              </p>
                            </div>

                            {/* Detalles adicionales según la regla */}
                            {key === "regla_50_30_20" && regla.porcentajes && (
                              <div style={styles.reglaDetalles}>
                                <p style={styles.detallesTitulo}>
                                  Distribución actual:
                                </p>
                                <div style={styles.porcentajesGrid}>
                                  <div style={styles.porcentajeItem}>
                                    <span style={styles.porcentajeLabel}>
                                      Necesidades
                                    </span>
                                    <div style={styles.progressBar}>
                                      <div
                                        style={{
                                          ...styles.progressFill,
                                          width: `${regla.porcentajes.necesidades}%`,
                                          background:
                                            regla.porcentajes.necesidades > 50
                                              ? "#ef4444"
                                              : "#10b981",
                                        }}
                                      ></div>
                                    </div>
                                    <span style={styles.porcentajeValor}>
                                      {regla.porcentajes.necesidades}%
                                    </span>
                                  </div>
                                  <div style={styles.porcentajeItem}>
                                    <span style={styles.porcentajeLabel}>
                                      Deseos
                                    </span>
                                    <div style={styles.progressBar}>
                                      <div
                                        style={{
                                          ...styles.progressFill,
                                          width: `${regla.porcentajes.deseos}%`,
                                          background:
                                            regla.porcentajes.deseos > 30
                                              ? "#ef4444"
                                              : "#10b981",
                                        }}
                                      ></div>
                                    </div>
                                    <span style={styles.porcentajeValor}>
                                      {regla.porcentajes.deseos}%
                                    </span>
                                  </div>
                                  <div style={styles.porcentajeItem}>
                                    <span style={styles.porcentajeLabel}>
                                      Ahorros
                                    </span>
                                    <div style={styles.progressBar}>
                                      <div
                                        style={{
                                          ...styles.progressFill,
                                          width: `${regla.porcentajes.ahorros}%`,
                                          background:
                                            regla.porcentajes.ahorros < 20
                                              ? "#ef4444"
                                              : "#10b981",
                                        }}
                                      ></div>
                                    </div>
                                    <span style={styles.porcentajeValor}>
                                      {regla.porcentajes.ahorros}%
                                    </span>
                                  </div>
                                </div>
                              </div>
                            )}

                            {key === "limite_endeudamiento" &&
                              regla.porcentaje_deuda !== undefined && (
                                <div style={styles.reglaDetalles}>
                                  <p style={styles.detallesTitulo}>
                                    Nivel de endeudamiento:
                                  </p>
                                  <div style={styles.progressBar}>
                                    <div
                                      style={{
                                        ...styles.progressFill,
                                        width: `${regla.porcentaje_deuda}%`,
                                        background: color,
                                      }}
                                    ></div>
                                  </div>
                                  <p style={styles.detallesTexto}>
                                    {regla.porcentaje_deuda}% de tus ingresos
                                    van a deudas (máximo recomendado: 40%)
                                  </p>
                                  {regla.nivel_riesgo && (
                                    <span
                                      style={{
                                        ...styles.badge,
                                        background: `${color}15`,
                                        color: color,
                                      }}
                                    >
                                      Riesgo: {regla.nivel_riesgo}
                                    </span>
                                  )}
                                </div>
                              )}

                            {/* Recomendaciones */}
                            {!regla.cumple && (
                              <div style={styles.recomendacionBox}>
                                <Lightbulb size={16} color="#667eea" />
                                <span style={styles.recomendacionText}>
                                  {getRecomendacion(key)}
                                </span>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    );
                  })}
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
    if (regla.severidad === "danger")
      return (
        <AlertOctagon
          style={{
            width: 20,
            height: 20,
            color: "#dc2626", // rojo
          }}
        />
      );

    if (regla.severidad === "warning")
      return (
        <AlertTriangle
          style={{
            width: 20,
            height: 20,
            color: "#f59e0b", // amarillo
          }}
        />
      );

    return (
      <Lightbulb
        style={{
          width: 20,
          height: 20,
          color: "#3b82f6", // azul
        }}
        strokeWidth={2} // más marcado
      />
    );
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
    fontSize: "14px",
    fontWeight: "500",
    color: "#6b7280",
    margin: 0,
  },
  cardTitle: {
    fontSize: "17px",
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
    fontSize: "15px",
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
    gap: "24px",
    marginTop: "16px",
    flexWrap: "wrap",
  },
  semaforoIcon: {
    width: "80px",
    height: "80px",
    borderRadius: "12px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  semaforoText: {
    flex: 1,
    minWidth: "250px",
  },
  semaforoStatus: {
    fontSize: "20px",
    fontWeight: "700",
    marginBottom: "4px",
  },
  semaforoDesc: {
    fontSize: "15px",
    color: "#6b7280",
    marginBottom: "16px",
  },
  scoreBar: {
    marginTop: "12px",
  },
  scoreBarBg: {
    width: "100%",
    height: "12px",
    background: "#e5e7eb",
    borderRadius: "6px",
    overflow: "hidden",
    marginBottom: "8px",
  },
  scoreBarFill: {
    height: "100%",
    borderRadius: "6px",
    transition: "width 0.5s ease",
  },
  scoreText: {
    fontSize: "14px",
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
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    width: "20px",
    height: "20px",
  },

  recomendacionTitulo: {
    fontSize: "15px",
    fontWeight: "600",
    color: "#111827",
    margin: 0,
    textTransform: "capitalize",
  },
  recomendacionMensaje: {
    fontSize: "15px",
    color: "#6b7280",
    lineHeight: "1.5",
    margin: 0,
    paddingLeft: "32px",
  },
  evaluacionSubtitle: {
    fontSize: "15px",
    color: "#6b7280",
    marginBottom: "24px",
  },
  reglasGrid: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
  reglaCard: {
    background: "#f9fafb",
    borderRadius: "8px",
    overflow: "hidden",
    transition: "all 0.2s",
  },
  reglaHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "16px",
    cursor: "pointer",
    transition: "background 0.2s",
  },
  reglaHeaderLeft: {
    display: "flex",
    alignItems: "center",
    gap: "16px",
    flex: 1,
  },
  reglaIconContainer: {
    width: "48px",
    height: "48px",
    borderRadius: "8px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  reglaTitulo: {
    fontSize: "16px",
    fontWeight: "600",
    color: "#111827",
    margin: "0 0 4px 0",
  },
  reglaDescripcion: {
    fontSize: "14.2px",
    color: "#6b7280",
    margin: 0,
  },
  reglaHeaderRight: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
  },
  reglaContent: {
    padding: "0 16px 16px 16px",
    borderTop: "1px solid #e5e7eb",
  },
  reglaMensaje: {
    padding: "16px",
    background: "white",
    borderRadius: "8px",
    marginTop: "16px",
  },
  reglaMensajeText: {
    fontSize: "14.2px",
    color: "#374151",
    margin: 0,
    lineHeight: "1.5",
  },
  reglaDetalles: {
    marginTop: "16px",
    padding: "16px",
    background: "white",
    borderRadius: "8px",
  },
  detallesTitulo: {
    fontSize: "14.5px",
    fontWeight: "600",
    color: "#374151",
    marginBottom: "12px",
  },
  detallesTexto: {
    fontSize: "14.5px",
    color: "#6b7280",
    margin: "8px 0",
  },
  porcentajesGrid: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  porcentajeItem: {
    display: "grid",
    gridTemplateColumns: "100px 1fr 60px",
    alignItems: "center",
    gap: "12px",
  },
  porcentajeLabel: {
    fontSize: "13px",
    color: "#374151",
    fontWeight: "500",
  },
  porcentajeValor: {
    fontSize: "13px",
    fontWeight: "600",
    color: "#374151",
    textAlign: "right",
  },
  badge: {
    display: "inline-block",
    padding: "4px 12px",
    borderRadius: "12px",
    fontSize: "11px",
    fontWeight: "600",
    textTransform: "uppercase",
    marginTop: "8px",
  },
  recomendacionBox: {
    display: "flex",
    alignItems: "flex-start",
    gap: "12px",
    padding: "12px 16px",
    background: "#eff6ff",
    border: "1px solid #dbeafe",
    borderRadius: "8px",
    marginTop: "16px",
  },
  recomendacionText: {
    fontSize: "13px",
    color: "#1e40af",
    lineHeight: "1.5",
  },
};

export default Dashboard;
