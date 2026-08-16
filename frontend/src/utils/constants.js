/**
 * Constantes derivadas diretamente das regras do backend
 * (ver app/models/usuario.py -> PERFIS_VALIDOS e app/auth/decorators.py).
 * Mantendo esses valores centralizados evitamos strings soltas ("admin",
 * "professor"...) espalhadas pelos componentes.
 */

export const PERFIS = {
  ADMIN: "admin",
  PROFESSOR: "professor",
  RESPONSAVEL: "responsavel",
};

export const PERFIL_LABEL = {
  [PERFIS.ADMIN]: "Administrador",
  [PERFIS.PROFESSOR]: "Professor",
  [PERFIS.RESPONSAVEL]: "Responsável",
};

// Sigla usada no "selo" (RoleStamp) da barra lateral/topo — parte da
// identidade visual do produto (ver README.md > Decisões de Design).
export const PERFIL_SIGLA = {
  [PERFIS.ADMIN]: "ADM",
  [PERFIS.PROFESSOR]: "PROF",
  [PERFIS.RESPONSAVEL]: "RESP",
};

// Para onde cada perfil vai depois do login / ao acessar "/".
export const ROTA_INICIAL_POR_PERFIL = {
  [PERFIS.ADMIN]: "/admin",
  [PERFIS.PROFESSOR]: "/professor",
  [PERFIS.RESPONSAVEL]: "/responsavel",
};

/**
 * Itens de navegação da sidebar por perfil.
 * `implementado: false` faz o item aparecer desabilitado com a etiqueta
 * "em breve" — assim a estrutura de navegação final já fica visível
 * desde este primeiro entregável, mesmo que a tela ainda não exista.
 * Ver "Relatório de Continuidade" no README.md.
 */
export const NAV_ITEMS_POR_PERFIL = {
  [PERFIS.ADMIN]: [
    { rotulo: "Visão geral", rota: "/admin", implementado: true },
    { rotulo: "Turmas", rota: "/admin/turmas", implementado: false },
    { rotulo: "Usuários", rota: "/admin/usuarios", implementado: false },
    { rotulo: "Vínculos", rota: "/admin/vinculos", implementado: false },
    { rotulo: "Documentos pendentes", rota: "/admin/documentos", implementado: false },
    { rotulo: "Histórico escolar", rota: "/admin/historico", implementado: false },
  ],
  [PERFIS.PROFESSOR]: [
    { rotulo: "Visão geral", rota: "/professor", implementado: true },
    { rotulo: "Minhas turmas", rota: "/professor/turmas", implementado: false },
    { rotulo: "Lançar notas", rota: "/professor/notas", implementado: false },
    { rotulo: "Lançar faltas", rota: "/professor/faltas", implementado: false },
    { rotulo: "Ocorrências", rota: "/professor/ocorrencias", implementado: false },
  ],
  [PERFIS.RESPONSAVEL]: [
    { rotulo: "Visão geral", rota: "/responsavel", implementado: true },
    { rotulo: "Meus alunos", rota: "/responsavel/alunos", implementado: false },
    { rotulo: "Documentos", rota: "/responsavel/documentos", implementado: false },
    { rotulo: "Notificações", rota: "/responsavel/notificacoes", implementado: false },
  ],
};

export const CHAVE_TOKEN = "pae:token";
export const CHAVE_USUARIO = "pae:usuario";
