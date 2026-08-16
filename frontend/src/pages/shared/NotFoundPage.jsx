import { Link } from "react-router-dom";
import Button from "../../components/common/Button.jsx";
import styles from "./StatusPage.module.css";

export default function NotFoundPage() {
  return (
    <div className={styles.pagina}>
      <div className={styles.conteudo}>
        <span className={styles.codigo}>Erro 404</span>
        <h1 className={styles.titulo}>Página não encontrada</h1>
        <p className={styles.descricao}>
          O endereço acessado não existe na plataforma. Volte para o início
          e navegue pelo menu do seu painel.
        </p>
        <Link to="/">
          <Button>Voltar ao início</Button>
        </Link>
      </div>
    </div>
  );
}
