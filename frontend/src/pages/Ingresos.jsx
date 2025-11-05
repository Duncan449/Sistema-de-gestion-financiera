// frontend/src/pages/Ingresos.jsx
import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import {
  getIngresos,
  createIngreso,
  updateIngreso,
  deleteIngreso,
} from "../api/api";
import { Plus, Edit2, Trash2, DollarSign, Calendar, Tag } from "lucide-react";

const Ingresos = () => {
  const [ingresos, setIngresos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    monto: "",
    categoria: "",
    fecha: new Date().toISOString().split("T")[0],
  });

  useEffect(() => {
    cargarIngresos();
  }, []);

  const cargarIngresos = async () => {
    try {
      const data = await getIngresos();
      setIngresos(data);
    } catch (error) {
      console.error("Error al cargar ingresos:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editingId) {
        await updateIngreso(editingId, formData);
      } else {
        await createIngreso(formData);
      }

      cargarIngresos();
      cerrarModal();
    } catch (error) {
      alert(error.response?.data?.detail || "Error al guardar");
    }
  };

  const handleEdit = (ingreso) => {
    setEditingId(ingreso.id);
    setFormData({
      monto: ingreso.monto,
      categoria: ingreso.categoria,
      fecha: ingreso.fecha,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm("¿Estás seguro de eliminar este ingreso?")) {
      try {
        await deleteIngreso(id);
        cargarIngresos();
      } catch (error) {
        alert("Error al eliminar");
      }
    }
  };

  const cerrarModal = () => {
    setShowModal(false);
    setEditingId(null);
    setFormData({
      monto: "",
      categoria: "",
      fecha: new Date().toISOString().split("T")[0],
    });
  };

  const calcularTotal = () => {
    return ingresos.reduce((sum, ingreso) => sum + ingreso.monto, 0);
  };

  if (loading) {
    return (
      <div style={styles.layout}>
        <Sidebar />
        <div style={styles.mainContent}>
          <div style={styles.loadingCard}>
            <div style={styles.spinner}></div>
            <h2>Cargando ingresos</h2>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.layout}>
      <Sidebar />
      <div style={styles.mainContent}>
        <div style={styles.container}>
          {/* Header */}
          <div style={styles.header}>
            <div>
              <h1 style={styles.title}>Mis Ingresos</h1>
              <p style={styles.subtitle}>
                Gestiona y visualiza todos tus ingresos
              </p>
            </div>
            <button onClick={() => setShowModal(true)} style={styles.addBtn}>
              <Plus size={18} />
              Nuevo Ingreso
            </button>
          </div>

          {/* Stats Card */}
          <div style={styles.statsCard}>
            <div style={styles.statItem}>
              <p style={styles.statLabel}>Total Ingresos</p>
              <p style={styles.statValue}>
                ${calcularTotal().toLocaleString("es-CL")}
              </p>
            </div>
            <div style={styles.statDivider}></div>
            <div style={styles.statItem}>
              <p style={styles.statLabel}>Cantidad de Registros</p>
              <p style={styles.statValue}>{ingresos.length}</p>
            </div>
            <div style={styles.statDivider}></div>
            <div style={styles.statItem}>
              <p style={styles.statLabel}>Promedio</p>
              <p style={styles.statValue}>
                $
                {ingresos.length > 0
                  ? (calcularTotal() / ingresos.length).toLocaleString(
                      "es-CL",
                      { maximumFractionDigits: 0 }
                    )
                  : "0"}
              </p>
            </div>
          </div>

          {/* Table Card */}
          <div style={styles.tableCard}>
            {ingresos.length === 0 ? (
              <div style={styles.emptyState}>
                <DollarSign size={48} color="#d1d5db" />
                <h3 style={styles.emptyTitle}>No hay ingresos registrados</h3>
                <p style={styles.emptyText}>
                  Comienza agregando tu primer ingreso
                </p>
                <button
                  onClick={() => setShowModal(true)}
                  style={styles.emptyBtn}
                >
                  <Plus size={18} />
                  Agregar Ingreso
                </button>
              </div>
            ) : (
              <div style={styles.tableWrapper}>
                <table style={styles.table}>
                  <thead>
                    <tr>
                      <th style={styles.th}>
                        <div style={styles.thContent}>
                          <Calendar size={16} />
                          Fecha
                        </div>
                      </th>
                      <th style={styles.th}>
                        <div style={styles.thContent}>
                          <Tag size={16} />
                          Categoría
                        </div>
                      </th>
                      <th style={styles.th}>
                        <div style={styles.thContent}>
                          <DollarSign size={16} />
                          Monto
                        </div>
                      </th>
                      <th style={styles.th}>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {ingresos.map((ingreso) => (
                      <tr key={ingreso.id} style={styles.tr}>
                        <td style={styles.td}>{ingreso.fecha}</td>
                        <td style={styles.td}>
                          <span style={styles.categoryBadge}>
                            {ingreso.categoria}
                          </span>
                        </td>
                        <td style={styles.td}>
                          <span style={styles.montoText}>
                            ${ingreso.monto.toLocaleString("es-CL")}
                          </span>
                        </td>
                        <td style={styles.td}>
                          <div style={styles.actionButtons}>
                            <button
                              onClick={() => handleEdit(ingreso)}
                              style={styles.editBtn}
                              title="Editar"
                            >
                              <Edit2 size={16} />
                            </button>
                            <button
                              onClick={() => handleDelete(ingreso.id)}
                              style={styles.deleteBtn}
                              title="Eliminar"
                            >
                              <Trash2 size={16} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div style={styles.modalOverlay} onClick={cerrarModal}>
          <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div style={styles.modalHeader}>
              <h2 style={styles.modalTitle}>
                {editingId ? "Editar Ingreso" : "Nuevo Ingreso"}
              </h2>
              <button onClick={cerrarModal} style={styles.closeBtn}>
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} style={styles.form}>
              <div style={styles.inputGroup}>
                <label style={styles.label}>
                  <DollarSign size={16} />
                  Monto
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.monto}
                  onChange={(e) =>
                    setFormData({ ...formData, monto: e.target.value })
                  }
                  required
                  style={styles.input}
                  placeholder="Ej: 1000000"
                />
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Categoria</label>
                <select
                  name="categoria"
                  value={formData.categoria}
                  onChange={handleEdit}
                  style={styles.select}
                >
                  <option value="">Seleccione Categoria</option>
                  <option value="deuda">Deuda</option>
                  <option value="tarjeta">Tarjeta</option>
                  <option value="préstamo">Prestamo</option>
                  <option value="hipoteca">Hipoteca</option>
                </select>
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>
                  <Calendar size={16} />
                  Fecha
                </label>
                <input
                  type="date"
                  value={formData.fecha}
                  onChange={(e) =>
                    setFormData({ ...formData, fecha: e.target.value })
                  }
                  required
                  style={styles.input}
                />
              </div>

              <div style={styles.modalFooter}>
                <button
                  type="button"
                  onClick={cerrarModal}
                  style={styles.cancelBtn}
                >
                  Cancelar
                </button>
                <button type="submit" style={styles.submitBtn}>
                  {editingId ? "Actualizar" : "Guardar"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
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
    border: "1px solid #e5e7eb",
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
    marginBottom: "24px",
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
  addBtn: {
    background: "#10b981",
    color: "white",
    border: "none",
    padding: "12px 20px",
    borderRadius: "8px",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    gap: "8px",
    transition: "all 0.2s",
  },
  statsCard: {
    background: "white",
    padding: "24px",
    borderRadius: "12px",
    boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
    border: "1px solid #e5e7eb",
    marginBottom: "24px",
    display: "flex",
    justifyContent: "space-around",
    alignItems: "center",
  },
  statItem: {
    textAlign: "center",
    flex: 1,
  },
  statLabel: {
    fontSize: "13px",
    color: "#6b7280",
    marginBottom: "8px",
  },
  statValue: {
    fontSize: "24px",
    fontWeight: "700",
    color: "#10b981",
  },
  statDivider: {
    width: "1px",
    height: "40px",
    background: "#e5e7eb",
  },
  tableCard: {
    background: "white",
    borderRadius: "12px",
    boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
    border: "1px solid #e5e7eb",
    overflow: "hidden",
  },
  emptyState: {
    padding: "80px 20px",
    textAlign: "center",
  },
  emptyTitle: {
    fontSize: "18px",
    fontWeight: "600",
    color: "#374151",
    marginTop: "16px",
    marginBottom: "8px",
  },
  emptyText: {
    fontSize: "14px",
    color: "#9ca3af",
    marginBottom: "24px",
  },
  emptyBtn: {
    background: "#10b981",
    color: "white",
    border: "none",
    padding: "10px 20px",
    borderRadius: "8px",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: "8px",
  },
  tableWrapper: {
    overflowX: "auto",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
  },
  th: {
    background: "#f9fafb",
    padding: "16px",
    textAlign: "left",
    fontSize: "13px",
    fontWeight: "600",
    color: "#6b7280",
    borderBottom: "1px solid #e5e7eb",
  },
  thContent: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
  },
  tr: {
    transition: "background 0.2s",
    cursor: "pointer",
  },
  td: {
    padding: "16px",
    fontSize: "14px",
    color: "#374151",
    borderBottom: "1px solid #f3f4f6",
  },
  categoryBadge: {
    background: "#eff6ff",
    color: "#3b82f6",
    padding: "4px 12px",
    borderRadius: "16px",
    fontSize: "12px",
    fontWeight: "500",
    textTransform: "capitalize",
  },
  montoText: {
    fontWeight: "600",
    color: "#10b981",
  },
  actionButtons: {
    display: "flex",
    gap: "8px",
  },
  editBtn: {
    background: "#f3f4f6",
    border: "none",
    padding: "8px",
    borderRadius: "6px",
    cursor: "pointer",
    color: "#3b82f6",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    transition: "all 0.2s",
  },
  deleteBtn: {
    background: "#fef2f2",
    border: "none",
    padding: "8px",
    borderRadius: "6px",
    cursor: "pointer",
    color: "#ef4444",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    transition: "all 0.2s",
  },
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: "rgba(0,0,0,0.5)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
    backdropFilter: "blur(4px)",
  },
  modal: {
    background: "white",
    borderRadius: "16px",
    width: "90%",
    maxWidth: "500px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
  },
  modalHeader: {
    padding: "24px",
    borderBottom: "1px solid #e5e7eb",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  modalTitle: {
    fontSize: "20px",
    fontWeight: "700",
    color: "#111827",
  },
  closeBtn: {
    background: "none",
    border: "none",
    fontSize: "24px",
    color: "#9ca3af",
    cursor: "pointer",
    padding: "4px 8px",
    borderRadius: "4px",
    transition: "all 0.2s",
  },
  form: {
    padding: "24px",
  },
  inputGroup: {
    marginBottom: "20px",
  },
  label: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontSize: "14px",
    fontWeight: "600",
    color: "#374151",
    marginBottom: "8px",
  },
  input: {
    width: "100%",
    padding: "12px",
    border: "1px solid #e5e7eb",
    borderRadius: "8px",
    fontSize: "14px",
    transition: "all 0.2s",
    color: "#111827",
  },
  select: {
    padding: "12px",
    border: "2px solid #e0e0e0",
    borderRadius: "8px",
    fontSize: "16px",
  },
  modalFooter: {
    display: "flex",
    gap: "12px",
    justifyContent: "flex-end",
    marginTop: "24px",
    paddingTop: "20px",
    borderTop: "1px solid #f3f4f6",
  },
  cancelBtn: {
    background: "white",
    color: "#6b7280",
    border: "1px solid #e5e7eb",
    padding: "10px 20px",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: "600",
    fontSize: "14px",
    transition: "all 0.2s",
  },
  submitBtn: {
    background: "#10b981",
    color: "white",
    border: "none",
    padding: "10px 24px",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: "600",
    fontSize: "14px",
    transition: "all 0.2s",
  },
};

export default Ingresos;
