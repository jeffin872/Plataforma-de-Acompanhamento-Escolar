import { Link } from "react-router-dom";
import Button from "../../components/common/Button.jsx";
import { useAuth } from "../../hooks/useAuth.js";
import styles from "./StatusPage.module.css";

/**
 * Exibida quando um usuário autenticado tenta acessar um painel de outro
 * perfil (ex: um responsável tentando abrir /admin) — espelha o 403 que
 * o backend já devolveria (ver @perfil_requerido em app/auth/decorators.py).
 */
export default function UnauthorizedPage() {
  const { logout } = useAuth();

  return (
    <div className={styles.pagina}>
      <div className={styles.conteudo}>
        <span className={styles.codigo}>Erro 403</span>
        <h1 className={styles.titulo}>Acesso não autorizado</h1>
        <p className={styles.descricao}>
          Sua conta não tem permissão para acessar esta área da plataforma.
          Se você acredita que isso é um engano, procure a administração da
          escola.
        </p>
        <Link to="/">
          <Button>Voltar ao meu painel</Button>
        </Link>
        <Button variante="texto" onClick={logout}>
          Sair e entrar com outra conta
        </Button>
      </div>
    </div>
  );
}
