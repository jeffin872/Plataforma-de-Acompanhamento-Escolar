import { forwardRef, useId } from "react";
import styles from "./Input.module.css";

/**
 * Input com rótulo e mensagem de erro já embutidos — assim toda tela de
 * formulário (login, cadastro de aluno, lançamento de nota...) usa o
 * mesmo padrão de acessibilidade (label associado via htmlFor/id,
 * aria-invalid, aria-describedby) sem repetir esse cuidado toda vez.
 */
const Input = forwardRef(function Input(
  { rotulo, erro, dica, id, ...props },
  ref
) {
  const idGerado = useId();
  const inputId = id || idGerado;
  const idErro = erro ? `${inputId}-erro` : undefined;
  const idDica = dica ? `${inputId}-dica` : undefined;

  return (
    <div className={styles.campo}>
      {rotulo && (
        <label htmlFor={inputId} className={styles.rotulo}>
          {rotulo}
        </label>
      )}
      <input
        id={inputId}
        ref={ref}
        className={`${styles.input} ${erro ? styles.comErro : ""}`}
        aria-invalid={Boolean(erro) || undefined}
        aria-describedby={idErro || idDica}
        {...props}
      />
      {dica && !erro && (
        <span id={idDica} className={styles.dica}>
          {dica}
        </span>
      )}
      {erro && (
        <span id={idErro} className={styles.mensagemErro} role="alert">
          {erro}
        </span>
      )}
    </div>
  );
});

export default Input;
