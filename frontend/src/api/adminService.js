import { api } from "./axiosClient.js";
import { ENDPOINTS } from "./endpoints.js";

/**
 * Serviço do módulo Administrativo (perfil "admin").
 * Espelha app/admin/routes.py. Usado pelas telas de gestão de usuários,
 * turmas, vínculos e pelo dashboard — algumas ainda a serem construídas
 * (ver "Relatório de Continuidade" no README.md).
 */

// --- Usuários ---
export async function listarUsuarios(perfil) {
  const { data } = await api.get(ENDPOINTS.ADMIN_USUARIOS, {
    params: perfil ? { perfil } : undefined,
  });
  return data.dados;
}

export async function criarUsuario(usuario) {
  const { data } = await api.post(ENDPOINTS.ADMIN_USUARIOS, usuario);
  return data.dados;
}

export async function atualizarUsuario(id, alteracoes) {
  const { data } = await api.put(ENDPOINTS.ADMIN_USUARIO(id), alteracoes);
  return data.dados;
}

export async function desativarUsuario(id) {
  const { data } = await api.delete(ENDPOINTS.ADMIN_USUARIO(id));
  return data.mensagem;
}

// --- Turmas ---
export async function listarTurmas() {
  const { data } = await api.get(ENDPOINTS.ADMIN_TURMAS);
  return data.dados;
}

export async function criarTurma(turma) {
  const { data } = await api.post(ENDPOINTS.ADMIN_TURMAS, turma);
  return data.dados;
}

export async function detalharTurma(turmaId) {
  const { data } = await api.get(ENDPOINTS.ADMIN_TURMA(turmaId));
  return data.dados;
}

export async function adicionarAlunoNaTurma(turmaId, aluno) {
  const { data } = await api.post(ENDPOINTS.ADMIN_TURMA_ALUNOS(turmaId), aluno);
  return data.dados;
}

export async function vincularProfessorDisciplina(turmaId, professorId, disciplina) {
  const { data } = await api.post(ENDPOINTS.ADMIN_TURMA_VINCULAR_PROFESSOR(turmaId), {
    professor_id: professorId,
    disciplina,
  });
  return data.dados;
}

// --- Vínculo responsável <-> aluno ---
export async function vincularResponsavelAluno(responsavelId, alunoId, parentesco) {
  const { data } = await api.post(ENDPOINTS.ADMIN_VINCULAR_RESPONSAVEL, {
    responsavel_id: responsavelId,
    aluno_id: alunoId,
    parentesco,
  });
  return data.mensagem;
}

// --- Histórico escolar ---
export async function importarHistorico(alunoId, notas, faltas) {
  const { data } = await api.post(ENDPOINTS.ADMIN_HISTORICO_IMPORTAR, {
    aluno_id: alunoId,
    notas,
    faltas,
  });
  return data.dados;
}

// --- Dashboard ---
export async function buscarDashboardAdmin() {
  const { data } = await api.get(ENDPOINTS.ADMIN_DASHBOARD);
  return data.dados;
}
