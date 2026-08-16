import { api } from "./axiosClient.js";
import { ENDPOINTS } from "./endpoints.js";

/**
 * Serviço da Área do Responsável (perfil "responsavel").
 * Espelha app/responsavel/routes.py — todas as rotas aqui são somente
 * leitura, e o backend já garante que só retornam dados de alunos
 * formalmente vinculados ao responsável logado.
 */

export async function listarMeusAlunos() {
  const { data } = await api.get(ENDPOINTS.RESPONSAVEL_MEUS_ALUNOS);
  return data.dados;
}

export async function listarNotasDoAluno(alunoId) {
  const { data } = await api.get(ENDPOINTS.RESPONSAVEL_ALUNO_NOTAS(alunoId));
  return data.dados;
}

export async function listarFaltasDoAluno(alunoId) {
  const { data } = await api.get(ENDPOINTS.RESPONSAVEL_ALUNO_FALTAS(alunoId));
  return data.dados; // { faltas, total, nao_justificadas }
}

export async function listarOcorrenciasDoAluno(alunoId) {
  const { data } = await api.get(ENDPOINTS.RESPONSAVEL_ALUNO_OCORRENCIAS(alunoId));
  return data.dados;
}

export async function listarMinhasNotificacoes() {
  const { data } = await api.get(ENDPOINTS.RESPONSAVEL_NOTIFICACOES);
  return data.dados;
}
