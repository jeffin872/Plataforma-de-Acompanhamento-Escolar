/**
 * Todas as rotas da API REST Flask, em um único lugar. Espelha
 * exatamente os blueprints registrados em backend/app/__init__.py.
 * Se uma rota mudar no backend, este é o único arquivo do frontend
 * que precisa ser tocado.
 */
export const ENDPOINTS = {
  // --- app/auth/routes.py (url_prefix="/api/auth") ---
  AUTH_LOGIN: "/api/auth/login",
  AUTH_ME: "/api/auth/me",
  AUTH_SENHA: "/api/auth/senha",

  // --- app/admin/routes.py (url_prefix="/api/admin") ---
  ADMIN_USUARIOS: "/api/admin/usuarios",
  ADMIN_USUARIO: (id) => `/api/admin/usuarios/${id}`,
  ADMIN_TURMAS: "/api/admin/turmas",
  ADMIN_TURMA: (id) => `/api/admin/turmas/${id}`,
  ADMIN_TURMA_ALUNOS: (turmaId) => `/api/admin/turmas/${turmaId}/alunos`,
  ADMIN_TURMA_VINCULAR_PROFESSOR: (turmaId) => `/api/admin/turmas/${turmaId}/vincular-professor`,
  ADMIN_VINCULAR_RESPONSAVEL: "/api/admin/vincular-responsavel",
  ADMIN_HISTORICO_IMPORTAR: "/api/admin/historico/importar",
  ADMIN_DASHBOARD: "/api/admin/dashboard",

  // --- app/academic/routes.py (url_prefix="/api/academic") — perfil professor ---
  ACADEMIC_MINHAS_TURMAS: "/api/academic/minhas-turmas",
  ACADEMIC_NOTAS: "/api/academic/notas",
  ACADEMIC_TURMA_NOTAS: (turmaId) => `/api/academic/turmas/${turmaId}/notas`,
  ACADEMIC_FALTAS: "/api/academic/faltas",
  ACADEMIC_FALTA_JUSTIFICAR: (faltaId) => `/api/academic/faltas/${faltaId}/justificar`,
  ACADEMIC_TURMA_FALTAS: (turmaId) => `/api/academic/turmas/${turmaId}/faltas`,
  ACADEMIC_OCORRENCIAS: "/api/academic/ocorrencias",
  ACADEMIC_TURMA_OCORRENCIAS: (turmaId) => `/api/academic/turmas/${turmaId}/ocorrencias`,

  // --- app/responsavel/routes.py (url_prefix="/api/responsavel") ---
  RESPONSAVEL_MEUS_ALUNOS: "/api/responsavel/meus-alunos",
  RESPONSAVEL_ALUNO_NOTAS: (alunoId) => `/api/responsavel/alunos/${alunoId}/notas`,
  RESPONSAVEL_ALUNO_FALTAS: (alunoId) => `/api/responsavel/alunos/${alunoId}/faltas`,
  RESPONSAVEL_ALUNO_OCORRENCIAS: (alunoId) => `/api/responsavel/alunos/${alunoId}/ocorrencias`,
  RESPONSAVEL_NOTIFICACOES: "/api/responsavel/notificacoes",

  // --- app/documents/routes.py (url_prefix="/api/documentos") ---
  DOCUMENTOS: "/api/documentos",
  DOCUMENTOS_MEUS: "/api/documentos/meus",
  DOCUMENTO: (id) => `/api/documentos/${id}`,
  DOCUMENTO_ARQUIVO: (nomeArquivo) => `/api/documentos/arquivo/${nomeArquivo}`,

  SAUDE: "/api/saude",
};
