import { createContext, useCallback, useEffect, useMemo, useState } from "react";
import * as authService from "../api/authService.js";
import { registrarHandlerNaoAutorizado } from "../api/axiosClient.js";
import { CHAVE_TOKEN, CHAVE_USUARIO } from "../utils/constants.js";

export const AuthContext = createContext(null);

/**
 * Fonte única de verdade sobre "quem está logado e com qual perfil".
 *
 * Responsabilidades:
 *  1. Persistir o token JWT (localStorage) para sobreviver a um F5.
 *  2. Ao montar, revalidar o token contra GET /api/auth/me — se o token
 *     expirou ou foi revogado, o usuário já começa deslogado, em vez de
 *     ver telas protegidas com dados desatualizados.
 *  3. Expor login()/logout() para o resto da aplicação.
 *  4. Reagir a um 401 vindo de QUALQUER chamada da API (via
 *     registrarHandlerNaoAutorizado), garantindo que uma sessão expirada
 *     no meio do uso derruba o usuário para a tela de login.
 */
export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [carregando, setCarregando] = useState(true); // true = ainda validando sessão
  const [erroLogin, setErroLogin] = useState(null);

  const limparSessao = useCallback(() => {
    localStorage.removeItem(CHAVE_TOKEN);
    localStorage.removeItem(CHAVE_USUARIO);
    setUsuario(null);
  }, []);

  // Revalida a sessão existente uma única vez, ao montar o app.
  useEffect(() => {
    async function validarSessaoAtual() {
      const tokenSalvo = localStorage.getItem(CHAVE_TOKEN);
      if (!tokenSalvo) {
        setCarregando(false);
        return;
      }
      try {
        const usuarioAtual = await authService.buscarUsuarioLogado();
        setUsuario(usuarioAtual);
      } catch {
        // Token expirado/inválido: limpa silenciosamente e manda pro login.
        limparSessao();
      } finally {
        setCarregando(false);
      }
    }
    validarSessaoAtual();
  }, [limparSessao]);

  // Se qualquer requisição da API tomar 401 no meio da navegação
  // (sessão expirou), reagimos limpando o estado local.
  useEffect(() => {
    registrarHandlerNaoAutorizado(() => {
      limparSessao();
    });
  }, [limparSessao]);

  const login = useCallback(async (email, senha) => {
    setErroLogin(null);
    try {
      const { token, usuario: usuarioLogado } = await authService.login(email, senha);
      localStorage.setItem(CHAVE_TOKEN, token);
      localStorage.setItem(CHAVE_USUARIO, JSON.stringify(usuarioLogado));
      setUsuario(usuarioLogado);
      return usuarioLogado;
    } catch (erro) {
      const mensagem = erro.mensagemAmigavel || "Não foi possível entrar. Tente novamente.";
      setErroLogin(mensagem);
      throw erro;
    }
  }, []);

  const logout = useCallback(() => {
    limparSessao();
  }, [limparSessao]);

  const valor = useMemo(
    () => ({
      usuario,
      perfil: usuario?.perfil ?? null,
      estaAutenticado: Boolean(usuario),
      carregando,
      erroLogin,
      login,
      logout,
    }),
    [usuario, carregando, erroLogin, login, logout]
  );

  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>;
}
