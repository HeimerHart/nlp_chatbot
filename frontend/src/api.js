import axios from "axios";

function decodeToken(token) {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
}

function getAnonymousId() {
  let anonId = sessionStorage.getItem("anon_session_id");
  if (!anonId) {
    anonId =
      typeof crypto !== "undefined" && crypto.randomUUID
        ? crypto.randomUUID()
        : `guest-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    sessionStorage.setItem("anon_session_id", anonId);
  }
  return anonId;
}

export function getSessionId() {
  const token = localStorage.getItem("token");
  const payload = token ? decodeToken(token) : null;
  return payload?.email || getAnonymousId();
}

const isLocalHost = ["localhost", "127.0.0.1"].includes(window.location.hostname);

const baseURL =
  import.meta.env.VITE_API_URL ||
  (isLocalHost ? "http://localhost:8000" : "https://nlp-chatbot-backend.onrender.com");

const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401 && localStorage.getItem("token")) {
      localStorage.removeItem("token");
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

export default api;
