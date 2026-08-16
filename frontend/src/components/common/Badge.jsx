import styles from "./Badge.module.css";

/** tom: "neutro" | "sucesso" | "alerta" | "perigo" | "primario" */
export default function Badge({ tom = "neutro", children }) {
  return <span className={`${styles.badge} ${styles[tom]}`}>{children}</span>;
}
