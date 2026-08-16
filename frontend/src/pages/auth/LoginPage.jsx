import { useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import AuthLayout from "../../layouts/AuthLayout.jsx";
import Input from "../../components/common/Input.jsx";
import Button from "../../components/common/Button.jsx";
import Alert from "../../components/common/Alert.jsx";
import { useAuth } from "../../hooks/useAuth.js";
import { ROTA_INICIAL_POR_PERFIL } from "../../utils/constants.js";
import styles from "./LoginPage.module.css";

export default function LoginPage() {
  const { login, estaAutenticado, perfil, carregando: validandoSessao } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState(null);

  // Já logado (ex: usuário digitou /login com sessão ativa) -> manda
  // direto pro painel do perfil dele, sem mostrar o formulário à toa.
  if (!validandoSessao && estaAutenticado) {
    const destino = location.state?.de?.pathname || ROTA_INICIAL_POR_PERFIL[perfil];
    return <Navigate to={destino} replace />;
  }

  async function aoSubmeter(evento) {
    evento.preventDefault();
    setErro(null);
    setEnviando(true);
    try {
      const usuarioLogado = await login(email.trim(), senha);
      navigate(ROTA_INICIAL_POR_PERFIL[usuarioLogado.perfil], { replace: true });
    } catch (erroCapturado) {
      setErro(erroCapturado.mensagemAmigavel || "Não foi possível entrar. Tente novamente.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <AuthLayout>
      <div className={styles.cartao}>
        <h2 className={styles.titulo}>Entrar</h2>
        <p className={styles.subtitulo}>
          Acesse com o e-mail e a senha cadastrados pela sua escola.
        </p>

        <form className={styles.formulario} onSubmit={aoSubmeter} noValidate>
          <Input
            rotulo="E-mail"
            type="email"
            name="email"
            autoComplete="username"
            placeholder="seunome@escola.com"
            value={email}
            onChange={(evento) => setEmail(evento.target.value)}
            required
          />
          <Input
            rotulo="Senha"
            type="password"
            name="senha"
            autoComplete="current-password"
            placeholder="••••••••"
            value={senha}
            onChange={(evento) => setSenha(evento.target.value)}
            required
          />

          <Alert tom="erro">{erro}</Alert>

          <Button type="submit" carregando={enviando}>
            Entrar
          </Button>
        </form>

        <p className={styles.rodape}>
          Administrador, professor ou responsável: use o mesmo formulário — a
          plataforma direciona você ao seu painel automaticamente.
        </p>
      </div>
    </AuthLayout>
  );
}
