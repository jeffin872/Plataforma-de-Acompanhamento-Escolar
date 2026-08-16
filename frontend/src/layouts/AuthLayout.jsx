import styles from "./AuthLayout.module.css";

/**
 * Layout de tela cheia para o login: painel de marca à esquerda (tema
 * "pauta de caderno") + card de formulário à direita. Em telas estreitas,
 * o painel de marca vira um cabeçalho compacto e o formulário assume o
 * corpo da tela — ver AuthLayout.module.css.
 */
export default function AuthLayout({ children }) {
  return (
    <div className={styles.pagina}>
      <aside className={styles.painelMarca}>
        <div className={styles.painelMarcaConteudo}>
          <p className={styles.instituicao}>UFCA · Projeto Integrado III</p>
          <h1 className={styles.tituloMarca}>Plataforma de Acompanhamento Escolar</h1>
          <p className={styles.descricaoMarca}>
            Notas, faltas, ocorrências e documentos da escola — em um só lugar
            para administradores, professores e responsáveis.
          </p>
        </div>
      </aside>

      <main className={styles.painelFormulario}>{children}</main>
    </div>
  );
}
