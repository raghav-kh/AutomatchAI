import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const TOKEN_KEY = "automatch_token";

export const api = axios.create({ baseURL });

// --- Token storage & auto-attachment ---
export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY);
}
export function storeToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
  api.defaults.headers.common.Authorization = `Bearer ${token}`;
}
export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
  delete api.defaults.headers.common.Authorization;
}
// Restore token on page load/refresh
const existingToken = getStoredToken();
if (existingToken) {
  api.defaults.headers.common.Authorization = `Bearer ${existingToken}`;
}

// --- Auth ---
export const login = (username, password) => {
  const form = new URLSearchParams();
  form.set("username", username);
  form.set("password", password);
  return api.post("/auth/login", form, { headers: { "Content-Type": "application/x-www-form-urlencoded" } }).then((r) => r.data);
};
export const register = (username, password, setupKey) =>
  api.post("/auth/register", { username, password, setup_key: setupKey }).then((r) => r.data);
export const getMe = () => api.get("/auth/me").then((r) => r.data);

// --- Manufacturers ---
export const listManufacturers = (params) => api.get("/manufacturers", { params }).then((r) => r.data);
export const createManufacturer = (data) => api.post("/manufacturers", data).then((r) => r.data);
export const updateManufacturer = (id, data) => api.patch(`/manufacturers/${id}`, data).then((r) => r.data);
export const deleteManufacturer = (id) => api.delete(`/manufacturers/${id}`);
export const pendingClassification = () => api.get("/manufacturers/pending-classification").then((r) => r.data);

// --- Cars ---
export const listCars = (params) => api.get("/cars", { params }).then((r) => r.data);
export const getCar = (id) => api.get(`/cars/${id}`).then((r) => r.data);
export const createCar = (data) => api.post("/cars", data).then((r) => r.data);
export const updateCar = (id, data) => api.patch(`/cars/${id}`, data).then((r) => r.data);
export const deleteCar = (id) => api.delete(`/cars/${id}`);

// --- Variants ---
export const listVariantsForCar = (carId) => api.get(`/cars/${carId}/variants`).then((r) => r.data);
export const getVariant = (id) => api.get(`/variants/${id}`).then((r) => r.data);
export const createVariant = (carId, data) => api.post(`/cars/${carId}/variants`, data).then((r) => r.data);
export const updateVariant = (id, data) => api.patch(`/variants/${id}`, data).then((r) => r.data);
export const deleteVariant = (id) => api.delete(`/variants/${id}`);
export const upsertSpecifications = (variantId, data) =>
  api.put(`/variants/${variantId}/specifications`, data).then((r) => r.data);
export const upsertAiAttributes = (variantId, data) =>
  api.put(`/variants/${variantId}/ai-attributes`, data).then((r) => r.data);

// --- Recommendations / Comparisons / Ownership cost ---
export const getRecommendations = (preferences, topN = 10) =>
  api.post("/recommendations", preferences, { params: { top_n: topN } }).then((r) => r.data);

export const compareVariants = (variantIds) =>
  api
    .get("/compare", { params: { variant_ids: variantIds }, paramsSerializer: { indexes: null } })
    .then((r) => r.data);

export const getAlternatives = (variantId, limit = 3) =>
  api.get(`/variants/${variantId}/alternatives`, { params: { limit } }).then((r) => r.data);

export const getOwnershipCost = (variantId, params) =>
  api.get(`/variants/${variantId}/ownership-cost`, { params }).then((r) => r.data);

// --- Pipeline ---
export const classifyPending = () => api.post("/pipeline/classify-pending").then((r) => r.data);
export const ingestManufacturer = (id) => api.post(`/pipeline/manufacturers/${id}/ingest`).then((r) => r.data);

// If the stored token is invalid/expired, clear it so the UI drops back to a logged-out state
// instead of silently failing every write forever.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      clearToken();
    }
    return Promise.reject(error);
  }
);
