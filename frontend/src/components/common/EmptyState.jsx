import styles from "./EmptyState.module.css";

/**
 * Estado vazio como "convite a agir" (ver diretrizes de UX writing),
 * nunca só um "Nenhum item encontrado." solto.
 */
export default function EmptyState({ titulo, descricao, acao }) {
  return (
    <div className={styles.wrapper}>
      <h4 className={styles.titulo}>{titulo}</h4>
      {descricao && <p className={styles.descricao}>{descricao}</p>}
      {acao && <div className={styles.acao}>{acao}</div>}
    </div>
  );
}
