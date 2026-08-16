import { useMemo, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";
import Sidebar from "../components/layout/Sidebar.jsx";
import Topbar from "../components/layout/Topbar.jsx";
import styles from "./DashboardLayout.module.css";
import { NAV_ITEMS_POR_PERFIL } from "../utils/constants.js";

/**
 * Casca comum dos três painéis protegidos (Admin, Professor, Responsável):
 * Sidebar + Topbar fixos, com a página da rota atual renderizada via
 * <Outlet/>. O perfil vem do usuário autenticado — não é passado por
 * prop — então esta mesma casca serve para qualquer um dos três perfis
 * sem duplicação de código (ver ProtectedRoute + AppRoutes).
 */
export default function DashboardLayout() {
  const { perfil } = useAuth();
  const location = useLocation();
  const [menuMobileAberto, setMenuMobileAberto] = useState(false);

  const tituloSecao = useMemo(() => {
    const itens = NAV_ITEMS_POR_PERFIL[perfil] || [];
    const atual = itens.find((item) => item.rota === location.pathname);
    return atual?.rotulo || "Painel";
  }, [perfil, location.pathname]);

  return (
    <div className={styles.layout}>
      <Sidebar
        perfil={perfil}
        aberta={menuMobileAberto}
        aoFechar={() => setMenuMobileAberto(false)}
      />
      <div className={styles.areaPrincipal}>
        <Topbar tituloSecao={tituloSecao} aoAbrirMenu={() => setMenuMobileAberto(true)} />
        <main className={styles.conteudo}>
          <div className={styles.conteudoInterno}>
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
