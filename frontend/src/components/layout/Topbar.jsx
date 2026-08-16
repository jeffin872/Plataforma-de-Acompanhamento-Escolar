import { useState, useRef, useEffect } from "react";
import { useAuth } from "../../hooks/useAuth.js";
import { iniciais } from "../../utils/formatters.js";
import RoleStamp from "./RoleStamp.jsx";
import styles from "./Topbar.module.css";

/**
 * Barra superior: botão de menu (mobile), título da seção atual e menu
 * do usuário com a ação de sair. `aoAbrirMenu` é repassado pelo
 * DashboardLayout para abrir a gaveta do Sidebar em telas estreitas.
 */
export default function Topbar({ tituloSecao, aoAbrirMenu }) {
  const { usuario, perfil, logout } = useAuth();
  const [menuAberto, setMenuAberto] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    function fecharAoClicarFora(evento) {
      if (menuRef.current && !menuRef.current.contains(evento.target)) {
        setMenuAberto(false);
      }
    }
    document.addEventListener("mousedown", fecharAoClicarFora);
    return () => document.removeEventListener("mousedown", fecharAoClicarFora);
  }, []);

  return (
    <header className={styles.topbar}>
      <div className={styles.esquerda}>
        <button
          type="button"
          className={styles.botaoMenu}
          onClick={aoAbrirMenu}
          aria-label="Abrir menu de navegação"
        >
          <span className={styles.iconeMenu} aria-hidden="true" />
        </button>
        <h1 className={styles.titulo}>{tituloSecao}</h1>
      </div>

      <div className={styles.usuarioMenu} ref={menuRef}>
        <button
          type="button"
          className={styles.botaoUsuario}
          onClick={() => setMenuAberto((aberto) => !aberto)}
          aria-haspopup="menu"
          aria-expanded={menuAberto}
        >
          <span className={styles.avatar}>{iniciais(usuario?.nome)}</span>
          <span className={styles.nomeUsuario}>{usuario?.nome}</span>
        </button>

        {menuAberto && (
          <div className={styles.dropdown} role="menu">
            <div className={styles.dropdownCabecalho}>
              <RoleStamp perfil={perfil} tamanho="sm" />
              <div>
                <p className={styles.dropdownNome}>{usuario?.nome}</p>
                <p className={styles.dropdownEmail}>{usuario?.email}</p>
              </div>
            </div>
            <button type="button" role="menuitem" className={styles.sair} onClick={logout}>
              Sair da conta
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
