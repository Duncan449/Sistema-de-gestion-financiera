// frontend/src/api/api.js
import axios from "axios";

// Configuración base de Axios
const api = axios.create({
  baseURL: "http://localhost:8000", // URL de tu backend FastAPI
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor: Añade el token JWT automáticamente a cada petición
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ============= AUTENTICACIÓN =============
export const login = async (email, password) => {
  const response = await api.post("/auth/login", { email, password });
  return response.data;
};

export const register = async (nombre_completo, email, username, password) => {
  const response = await api.post("/auth/register", {
    nombre_completo,
    email,
    username,
    password,
  });
  return response.data;
};

// ============= INGRESOS =============
export const getIngresos = async () => {
  const response = await api.get("/ingresos/");
  return response.data;
};

export const createIngreso = async (data) => {
  const response = await api.post("/ingresos/", data);
  return response.data;
};

export const updateIngreso = async (id, data) => {
  const response = await api.put(`/ingresos/${id}`, data);
  return response.data;
};

export const deleteIngreso = async (id) => {
  const response = await api.delete(`/ingresos/${id}`);
  return response.data;
};

// ============= EGRESOS =============
export const getEgresos = async () => {
  const response = await api.get("/egresos/");
  return response.data;
};

export const createEgreso = async (data) => {
  const response = await api.post("/egresos/", data);
  return response.data;
};

export const updateEgreso = async (id, data) => {
  const response = await api.put(`/egresos/${id}`, data);
  return response.data;
};

export const deleteEgreso = async (id) => {
  const response = await api.delete(`/egresos/${id}`);
  return response.data;
};

// ============= ACTIVOS =============
export const getActivos = async () => {
  const response = await api.get("/activos/");
  return response.data;
};

export const createActivo = async (data) => {
  const response = await api.post("/activos/", data);
  return response.data;
};

export const updateActivo = async (id, data) => {
  const response = await api.put(`/activos/${id}`, data);
  return response.data;
};

export const deleteActivo = async (id) => {
  const response = await api.delete(`/activos/${id}`);
  return response.data;
};

// ============= PASIVOS =============
export const getPasivos = async () => {
  const response = await api.get("/pasivos/");
  return response.data;
};

export const createPasivo = async (data) => {
  const response = await api.post("/pasivos/", data);
  return response.data;
};

export const updatePasivo = async (id, data) => {
  const response = await api.put(`/pasivos/${id}`, data);
  return response.data;
};

export const deletePasivo = async (id) => {
  const response = await api.delete(`/pasivos/${id}`);
  return response.data;
};

// ============= ANÁLISIS FINANCIERO =============
export const getSaludFinanciera = async (usuarioId, dias = 30) => {
  const response = await api.get(
    `/analisis/salud-financiera/${usuarioId}?dias=${dias}`
  );
  return response.data;
};

export default api;
