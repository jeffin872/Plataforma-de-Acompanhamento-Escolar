import { useAuth } from "../../hooks/useAuth.js";
import { useApi } from "../../hooks/useApi.js";
import { buscarDashboardAdmin } from "../../api/adminService.js";
import Card from "../../components/common/Card.jsx";
import StatCard from "../../components/common/StatCard.jsx";
import Spinner from "../../components/common/Spinner.jsx";
import Alert from "../../components/common/Alert.jsx";
import styles from "../shared/DashboardShell.module.css";

/**
 * Primeira tela real consumindo a API: GET /api/admin/dashboard
 * (ver app/admin/routes.py -> dashboard()). Serve também como referência
 * de padrão para as próximas telas administrativas (turmas, usuários...).
 */
export default function AdminDashboardPage() {
  const { usuario } = useAuth();
  const { dados, carregando, erro, recarregar } = useApi(buscarDashboardAdmin);

  return (
    <div className={styles.shell}>
      <header className={styles.boasVindas}>
        <h2>Olá, {usuario?.nome?.split(" ")[0]}.</h2>
        <p className="text-muted">
          Visão geral da escola — turmas, corpo docente, famílias e pendências.
        </p>
      </header>

      {erro && <Alert tom="erro">{erro}</Alert>}

      {carregando && <Spinner mensagem="Carregando indicadores…" />}

      {!carregando && dados && (
        <div className={styles.grade}>
          <StatCard rotulo="Turmas ativas" valor={dados.total_turmas} />
          <StatCard rotulo="Alunos matriculados" valor={dados.total_alunos} />
          <StatCard rotulo="Professores ativos" valor={dados.total_professores} />
          <StatCard rotulo="Responsáveis cadastrados" valor={dados.total_responsaveis} />
          <StatCard
            rotulo="Documentos pendentes de análise"
            valor={dados.documentos_pendentes}
            tom={dados.documentos_pendentes > 0 ? "alerta" : "neutro"}
          />
        </div>
      )}

      <Card titulo="Próximos passos deste painel">
        <p className={styles.textoSecundario}>
          As telas de gestão de turmas, usuários, vínculos e a fila de
          documentos pendentes ainda serão construídas sobre esta mesma
          base de rotas, contexto de autenticação e componentes — veja o
          menu lateral e o "Relatório de Continuidade" no README do
          projeto.
        </p>
        <button type="button" className={styles.linkRecarregar} onClick={recarregar}>
          Recarregar indicadores
        </button>
      </Card>
    </div>
  );
}
