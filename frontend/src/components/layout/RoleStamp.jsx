import { PERFIL_SIGLA } from "../../utils/constants.js";
import styles from "./RoleStamp.module.css";

/**
 * Elemento de assinatura visual do produto: um "carimbo" circular com a
 * sigla do perfil (ADM / PROF / RESP), inspirado no carimbo de correção
 * de um professor. Reforça a "Separação por Perfil" também visualmente —
 * cada perfil tem sua cor — sem depender só do texto do menu.
 */
export default function RoleStamp({ perfil, tamanho = "md" }) {
  return (
    <span
      className={`${styles.selo} ${styles[perfil]} ${styles[tamanho]}`}
      aria-hidden="true"
    >
      {PERFIL_SIGLA[perfil] || "?"}
    </span>
  );
}
