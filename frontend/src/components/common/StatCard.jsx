import styles from "./StatCard.module.css";

/** Card compacto de número + rótulo, usado na grade de estatísticas do dashboard. */
export default function StatCard({ rotulo, valor, tom = "neutro" }) {
  return (
    <div className={`${styles.card} ${styles[tom]}`}>
      <span className={styles.valor}>{valor}</span>
      <span className={styles.rotulo}>{rotulo}</span>
    </div>
  );
}
