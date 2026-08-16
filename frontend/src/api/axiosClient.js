import axios from "axios";
import { CHAVE_TOKEN } from "../utils/constants.js";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:5000";

export const api = axios.create({
  baseURL,
  timeout: 15000,
});

/**
 * O AuthContext é quem sabe redirecionar para /login e limpar o estado
 * de usuário em memória. Como este arquivo não pode importar o contexto
 * (React) sem criar dependência circular, ele expõe este pequeno
 * "registro" de callback — o AuthContext se inscreve nele uma vez, no
 * mount. Qualquer 401 vindo do backend (token ausente/expirado/inválido,
 * ver app/__init__.py) passa por aqui.
 */
let aoReceberNaoAutorizado = null;
export function registrarHandlerNaoAutorizado(callback) {
  aoReceberNaoAutorizado = callback;
}

// --- Anexa o JWT em toda requisição, quando existir ---
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(CHAVE_TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Normaliza erros e trata 401 de forma centralizada ---
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const mensagem =
      error.response?.data?.mensagem ||
      (error.code === "ECONNABORTED"
        ? "O servidor demorou demais para responder. Tente novamente."
        : !error.response
        ? "Não foi possível conectar à API. Verifique se o backend está rodando."
        : "Ocorreu um erro inesperado.");

    if (status === 401 && aoReceberNaoAutorizado) {
      aoReceberNaoAutorizado();
    }

    // Propaga um erro já com mensagem amigável pronta para a UI usar,
    // sem que cada componente precise conhecer o formato de resposta do Flask.
    return Promise.reject({ ...error, mensagemAmigavel: mensagem, status });
  }
);

export default api;
