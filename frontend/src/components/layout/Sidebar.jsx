import { NavLink } from "react-router-dom";
import { NAV_ITEMS_POR_PERFIL, PERFIL_LABEL } from "../../utils/constants.js";
import RoleStamp from "./RoleStamp.jsx";
import styles from "./Sidebar.module.css";

/**
 * Navegação lateral, montada dinamicamente a partir de NAV_ITEMS_POR_PERFIL.
 * Itens ainda não implementados aparecem visíveis, porém desabilitados —
 * assim a arquitetura de informação final do produto já fica clara desde
 * este primeiro entregável de frontend.
 *
 * `aberta`/`aoFechar`: controlam a versão em gaveta (mobile). Em telas
 * largas a sidebar fica sempre visível e essas props não têm efeito visual.
 */
export default function Sidebar({ perfil, aberta, aoFechar }) {
  const itens = NAV_ITEMS_POR_PERFIL[perfil] || [];

  return (
    <>
      {aberta && (
        <button
          type="button"
          className={styles.sobreposicao}
          aria-label="Fechar menu"
          onClick={aoFechar}
        />
      )}
      <aside
        className={`${styles.sidebar} ${aberta ? styles.sidebarAberta : ""}`}
        aria-label="Navegação principal"
      >
        <div className={styles.marca}>
          <span className={styles.marcaTitulo}>Acompanhamento Escolar</span>
          <span className={styles.marcaPerfil}>
            <RoleStamp perfil={perfil} tamanho="sm" />
            {PERFIL_LABEL[perfil]}
          </span>
        </div>

        <nav>
          <ul className={styles.lista}>
            {itens.map((item) => (
              <li key={item.rota}>
                {item.implementado ? (
                  <NavLink
                    to={item.rota}
                    end={item.rota === `/${perfil}`}
                    onClick={aoFechar}
                    className={({ isActive }) =>
                      `${styles.link} ${isActive ? styles.linkAtivo : ""}`
                    }
                  >
                    {item.rotulo}
                  </NavLink>
                ) : (
                  <span className={styles.linkDesabilitado} title="Em desenvolvimento">
                    {item.rotulo}
                    <span className={styles.etiquetaEmBreve}>em breve</span>
                  </span>
                )}
              </li>
            ))}
          </ul>
        </nav>
      </aside>
    </>
  );
}
