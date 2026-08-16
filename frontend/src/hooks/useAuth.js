import { useContext } from "react";
import { AuthContext } from "../context/AuthContext.jsx";

/**
 * Uso: const { usuario, perfil, estaAutenticado, login, logout } = useAuth();
 * Lança um erro claro se usado fora do <AuthProvider>, em vez de deixar
 * o React quebrar silenciosamente com "usuario is null".
 */
export function useAuth() {
  const contexto = useContext(AuthContext);
  if (!contexto) {
    throw new Error("useAuth() precisa ser usado dentro de um <AuthProvider>.");
  }
  return contexto;
}
