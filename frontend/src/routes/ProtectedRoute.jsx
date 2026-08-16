import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";
import { ROTA_INICIAL_POR_PERFIL } from "../utils/constants.js";
import Spinner from "../components/common/Spinner.jsx";

/**
 * Implementa a "Separação por Perfil" na camada de apresentação, espelhando
 * o decorator @perfil_requerido(...) do backend (app/auth/decorators.py):
 * o frontend nunca deve nem tentar renderizar uma tela que a API recusaria.
 *
 * Uso em AppRoutes.jsx:
 *   <Route element={<ProtectedRoute perfisPermitidos={["admin"]} />}>
 *     <Route path="/admin" element={<DashboardLayout />}>...</Route>
 *   </Route>
 *
 * Sem `perfisPermitidos`, a rota só exige estar autenticado (qualquer perfil).
 */
export default function ProtectedRoute({ perfisPermitidos }) {
  const { estaAutenticado, perfil, carregando } = useAuth();
  const location = useLocation();

  if (carregando) {
    return <Spinner telaCheia mensagem="Verificando sua sessão…" />;
  }

  if (!estaAutenticado) {
    return <Navigate to="/login" state={{ de: location }} replace />;
  }

  const perfilNaoAutorizado = perfisPermitidos && !perfisPermitidos.includes(perfil);
  if (perfilNaoAutorizado) {
    return <Navigate to="/nao-autorizado" replace />;
  }

  return <Outlet />;
}
