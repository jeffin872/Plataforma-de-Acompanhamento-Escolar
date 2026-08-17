import { api } from "./axiosClient.js";
import { ENDPOINTS } from "./endpoints.js";

/**
 * Serviço do fluxo "Gestão de Faltas e Atestados" (perfil "professor").
 * Espelha app/fluxo_faltas/routes.py -> professor_faltas_bp.
 *
 * Diferente de academicService.js (que já lança faltas "de verdade" no
 * PostgreSQL via /api/academic/faltas), este serviço fala com o fluxo
 * MVP em memória usado neste entregável — ver README > Relatório de
 * Continuidade para o plano de unificação dos dois fluxos.
 */

/** Lista as faltas já registradas neste fluxo (mais recentes primeiro). */
export async function listarFaltasMvp({ alunoId, status } = {}) {
  const { data } = await api.get(ENDPOINTS.PROFESSOR_FALTAS, {
    params: {
      aluno_id: alunoId || undefined,
      status: status || undefined,
    },
  });
  return data.dados;
}

/** Registra uma falta com status inicial "Pendente". */
export async function registrarFaltaMvp({ alunoId, data: dataFalta, disciplina }) {
  const { data } = await api.post(ENDPOINTS.PROFESSOR_FALTAS, {
    aluno_id: alunoId,
    data: dataFalta,
    disciplina,
  });
  return data.dados;
}
