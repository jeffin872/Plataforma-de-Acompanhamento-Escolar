import { api } from "./axiosClient.js";
import { ENDPOINTS } from "./endpoints.js";

/**
 * POST /api/auth/login — corpo: { email, senha }
 * Resposta (200): { sucesso, mensagem, dados: { token, usuario } }
 * Resposta (401/400/403): { sucesso: false, mensagem }
 */
export async function login(email, senha) {
  const { data } = await api.post(ENDPOINTS.AUTH_LOGIN, { email, senha });
  return data.dados; // { token, usuario }
}

/** GET /api/auth/me — dados do usuário logado, a partir do token atual. */
export async function buscarUsuarioLogado() {
  const { data } = await api.get(ENDPOINTS.AUTH_ME);
  return data.dados; // usuario
}

/** PUT /api/auth/senha — corpo: { senha_atual, nova_senha } */
export async function trocarSenha(senhaAtual, novaSenha) {
  const { data } = await api.put(ENDPOINTS.AUTH_SENHA, {
    senha_atual: senhaAtual,
    nova_senha: novaSenha,
  });
  return data.mensagem;
}
