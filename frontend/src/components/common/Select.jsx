import { forwardRef, useId } from "react";
import styles from "./Select.module.css";

/**
 * Select com rótulo e mensagem de erro embutidos — mesmo padrão de
 * acessibilidade do Input.jsx (label associado via htmlFor/id,
 * aria-invalid, aria-describedby).
 *
 * Uso:
 *   <Select rotulo="Aluno" value={alunoId} onChange={...}>
 *     <option value="">Selecione…</option>
 *     {alunos.map((a) => <option key={a.id} value={a.id}>{a.nome}</option>)}
 *   </Select>
 */
const Select = forwardRef(function Select(
  { rotulo, erro, dica, id, children, ...props },
  ref
) {
  const idGerado = useId();
  const selectId = id || idGerado;
  const idErro = erro ? `${selectId}-erro` : undefined;
  const idDica = dica ? `${selectId}-dica` : undefined;

  return (
    <div className={styles.campo}>
      {rotulo && (
        <label htmlFor={selectId} className={styles.rotulo}>
          {rotulo}
        </label>
      )}
      <select
        id={selectId}
        ref={ref}
        className={`${styles.select} ${erro ? styles.comErro : ""}`}
        aria-invalid={Boolean(erro) || undefined}
        aria-describedby={idErro || idDica}
        {...props}
      >
        {children}
      </select>
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

export default Select;
