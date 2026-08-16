import styles from "./Card.module.css";

/** Bloco de conteúdo reutilizável — base de cards de estatística, listas, formulários. */
export default function Card({ titulo, acao, children, className = "", ...props }) {
  return (
    <section className={`${styles.card} ${className}`} {...props}>
      {(titulo || acao) && (
        <header className={styles.cabecalho}>
          {titulo && <h3 className={styles.titulo}>{titulo}</h3>}
          {acao}
        </header>
      )}
      <div className={styles.conteudo}>{children}</div>
    </section>
  );
}
