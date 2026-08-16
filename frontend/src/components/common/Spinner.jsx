import styles from "./Spinner.module.css";

/**
 * `telaCheia`: centraliza o spinner ocupando a viewport inteira — usado
 * enquanto o AuthContext revalida a sessão, antes de decidir pra onde
 * a rota protegida deve mandar o usuário.
 */
export default function Spinner({ telaCheia = false, mensagem = "Carregando…" }) {
  const conteudo = (
    <div className={styles.wrapper} role="status" aria-live="polite">
      <span className={styles.aro} aria-hidden="true" />
      <span className={styles.mensagem}>{mensagem}</span>
    </div>
  );

  if (!telaCheia) return conteudo;

  return <div className={styles.telaCheia}>{conteudo}</div>;
}
