import styles from "./Button.module.css";

/**
 * variante: "primaria" (padrão) | "secundaria" | "perigo" | "texto"
 * carregando: mostra um estado de "enviando…" e desabilita o botão,
 * evitando duplo-clique em ações como login ou lançar nota.
 */
export default function Button({
  variante = "primaria",
  carregando = false,
  disabled,
  children,
  type = "button",
  ...props
}) {
  return (
    <button
      type={type}
      className={`${styles.botao} ${styles[variante]}`}
      disabled={disabled || carregando}
      aria-busy={carregando || undefined}
      {...props}
    >
      {carregando ? "Enviando…" : children}
    </button>
  );
}
