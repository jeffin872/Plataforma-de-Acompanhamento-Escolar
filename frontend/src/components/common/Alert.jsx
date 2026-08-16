import styles from "./Alert.module.css";

/**
 * tom: "erro" (padrão) | "sucesso" | "info"
 * Usado para respostas da API (ex: "E-mail ou senha inválidos.") — a
 * mesma mensagem que o Flask devolve em `mensagem`, sem reinterpretação.
 */
export default function Alert({ tom = "erro", children }) {
  if (!children) return null;
  return (
    <div className={`${styles.alerta} ${styles[tom]}`} role="alert">
      {children}
    </div>
  );
}
