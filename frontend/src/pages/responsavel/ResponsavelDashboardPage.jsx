import { useAuth } from "../../hooks/useAuth.js";
import { useApi } from "../../hooks/useApi.js";
import { listarMeusAlunos } from "../../api/responsavelService.js";
import Card from "../../components/common/Card.jsx";
import Spinner from "../../components/common/Spinner.jsx";
import Alert from "../../components/common/Alert.jsx";
import EmptyState from "../../components/common/EmptyState.jsx";
import styles from "../shared/DashboardShell.module.css";

/**
 * Consome GET /api/responsavel/meus-alunos. O backend já garante o
 * isolamento de dados (só retorna alunos formalmente vinculados a este
 * responsável, ver ResponsavelAluno em app/responsavel/routes.py) —
 * o frontend não precisa (nem deve) reimplementar esse filtro.
 */
export default function ResponsavelDashboardPage() {
  const { usuario } = useAuth();
  const { dados: alunos, carregando, erro } = useApi(listarMeusAlunos);

  return (
    <div className={styles.shell}>
      <header className={styles.boasVindas}>
        <h2>Olá, {usuario?.nome?.split(" ")[0]}.</h2>
        <p className="text-muted">Acompanhe aqui os alunos vinculados a você.</p>
      </header>

      {erro && <Alert tom="erro">{erro}</Alert>}
      {carregando && <Spinner mensagem="Carregando seus alunos…" />}

      {!carregando && alunos && (
        <Card titulo={`Meus alunos (${alunos.length})`}>
          {alunos.length === 0 ? (
            <EmptyState
              titulo="Nenhum aluno vinculado ainda"
              descricao="Assim que a escola vincular um aluno ao seu cadastro, ele aparecerá aqui com notas, faltas e ocorrências."
            />
          ) : (
            <div className={styles.listaCards}>
              {alunos.map((aluno) => (
                <div key={aluno.id} className={styles.itemCard}>
                  <span className={styles.itemCardTitulo}>{aluno.nome}</span>
                  <span className={styles.itemCardDetalhe}>
                    Matrícula {aluno.matricula}
                    {aluno.turma ? ` · ${aluno.turma.nome}` : ""}
                  </span>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      <Card titulo="Próximos passos deste painel">
        <p className={styles.textoSecundario}>
          As telas de notas, faltas, ocorrências, envio de atestados e
          notificações de cada aluno serão construídas a partir desta
          lista. Veja o "Relatório de Continuidade" no README do projeto.
        </p>
      </Card>
    </div>
  );
}
