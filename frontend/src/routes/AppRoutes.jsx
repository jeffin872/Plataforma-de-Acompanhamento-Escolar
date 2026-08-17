import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "./ProtectedRoute.jsx";
import DashboardLayout from "../layouts/DashboardLayout.jsx";
import LoginPage from "../pages/auth/LoginPage.jsx";
import AdminDashboardPage from "../pages/admin/AdminDashboardPage.jsx";
import ProfessorDashboardPage from "../pages/professor/ProfessorDashboardPage.jsx";
import ResponsavelDashboardPage from "../pages/responsavel/ResponsavelDashboardPage.jsx";
import ProfessorRegistroAcademicoPage from "../pages/professor/ProfessorRegistroAcademicoPage.jsx";
import ResponsavelEnvioAtestadoPage from "../pages/responsavel/ResponsavelEnvioAtestadoPage.jsx";
import AdminValidarAtestadosPage from "../pages/admin/AdminValidarAtestadosPage.jsx";
import NotFoundPage from "../pages/shared/NotFoundPage.jsx";
import UnauthorizedPage from "../pages/shared/UnauthorizedPage.jsx";
import { useAuth } from "../hooks/useAuth.js";
import { PERFIS, ROTA_INICIAL_POR_PERFIL } from "../utils/constants.js";
import Spinner from "../components/common/Spinner.jsx";

/** Decide para onde "/" deve levar, com base na sessão atual. */
function RedirecionadorInicial() {
  const { estaAutenticado, perfil, carregando } = useAuth();

  if (carregando) return <Spinner telaCheia mensagem="Carregando…" />;
  if (!estaAutenticado) return <Navigate to="/login" replace />;
  return <Navigate to={ROTA_INICIAL_POR_PERFIL[perfil]} replace />;
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      {/* --- Painel do Administrador --- */}
      <Route element={<ProtectedRoute perfisPermitidos={[PERFIS.ADMIN]} />}>
        <Route path="/admin" element={<DashboardLayout />}>
          <Route index element={<AdminDashboardPage />} />
          <Route path="documentos" element={<AdminValidarAtestadosPage />} />
          {/* Próximas rotas (turmas, usuários, vínculos, histórico)
              entram aqui como filhas de /admin, reaproveitando o mesmo
              DashboardLayout — ver "Relatório de Continuidade". */}
        </Route>
      </Route>

      {/* --- Painel do Professor --- */}
      <Route element={<ProtectedRoute perfisPermitidos={[PERFIS.PROFESSOR]} />}>
        <Route path="/professor" element={<DashboardLayout />}>
          <Route index element={<ProfessorDashboardPage />} />
          <Route path="faltas" element={<ProfessorRegistroAcademicoPage />} />
        </Route>
      </Route>

      {/* --- Painel do Responsável --- */}
      <Route element={<ProtectedRoute perfisPermitidos={[PERFIS.RESPONSAVEL]} />}>
        <Route path="/responsavel" element={<DashboardLayout />}>
          <Route index element={<ResponsavelDashboardPage />} />
          <Route path="documentos" element={<ResponsavelEnvioAtestadoPage />} />
        </Route>
      </Route>

      <Route path="/" element={<RedirecionadorInicial />} />
      <Route path="/nao-autorizado" element={<UnauthorizedPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
