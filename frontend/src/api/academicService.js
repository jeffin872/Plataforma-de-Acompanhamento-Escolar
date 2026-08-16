import { api } from "./axiosClient.js";
import { ENDPOINTS } from "./endpoints.js";

/**
 * Serviço da Área do Professor (perfil "professor").
 * Espelha app/academic/routes.py.
 */

export async function listarMinhasTurmas() {
  const { data } = await api.get(ENDPOINTS.ACADEMIC_MINHAS_TURMAS);
  return data.dados;
}

// --- Notas ---
export async function lancarNota(nota) {
  // nota: { aluno_id, turma_id, disciplina_id, valor, etapa, data_avaliacao }
  const { data } = await api.post(ENDPOINTS.ACADEMIC_NOTAS, nota);
  return data.dados;
}

export async function listarNotasDaTurma(turmaId) {
  const { data } = await api.get(ENDPOINTS.ACADEMIC_TURMA_NOTAS(turmaId));
  return data.dados;
}

// --- Faltas ---
export async function registrarFalta(aluno_id, turma_id, data_falta) {
  const { data } = await api.post(ENDPOINTS.ACADEMIC_FALTAS, {
    aluno_id,
    turma_id,
    data_falta,
  });
  return data.dados;
}

export async function justificarFalta(faltaId, motivo) {
  const { data } = await api.put(ENDPOINTS.ACADEMIC_FALTA_JUSTIFICAR(faltaId), { motivo });
  return data.dados;
}

export async function listarFaltasDaTurma(turmaId) {
  const { data } = await api.get(ENDPOINTS.ACADEMIC_TURMA_FALTAS(turmaId));
  return data.dados;
}

// --- Ocorrências ---
export async function registrarOcorrencia(ocorrencia) {
  // ocorrencia: { aluno_id, turma_id, tipo, descricao, data_ocorrencia }
  const { data } = await api.post(ENDPOINTS.ACADEMIC_OCORRENCIAS, ocorrencia);
  return data.dados;
}

export async function listarOcorrenciasDaTurma(turmaId) {
  const { data } = await api.get(ENDPOINTS.ACADEMIC_TURMA_OCORRENCIAS(turmaId));
  return data.dados;
}
