import { useAuth } from "../../hooks/useAuth.js";
import { useApi } from "../../hooks/useApi.js";
import { listarMinhasTurmas } from "../../api/academicService.js";
import Card from "../../components/common/Card.jsx";
import Spinner from "../../components/common/Spinner.jsx";
import Alert from "../../components/common/Alert.jsx";
import EmptyState from "../../components/common/EmptyState.jsx";
import Badge from "../../components/common/Badge.jsx";
import styles from "../shared/DashboardShell.module.css";

/**
 * Consome GET /api/academic/minhas-turmas (ver app/academic/routes.py),
 * que já devolve só os vínculos turma+disciplina do professor logado —
 * a trava "vínculo obrigatório para lançar nota/falta" é toda garantida
 * pelo backend; aqui só exibimos o que ele autoriza.
 */
export default function ProfessorDashboardPage() {
  const { usuario } = useAuth();
  const { dados: vinculos, carregando, erro } = useApi(listarMinhasTurmas);

  return (
    <div className={styles.shell}>
      <header className={styles.boasVindas}>
        <h2>Olá, {usuario?.nome?.split(" ")[0]}.</h2>
        <p className="text-muted">Suas turmas e disciplinas nesta escola.</p>
      </header>

      {erro && <Alert tom="erro">{erro}</Alert>}
      {carregando && <Spinner mensagem="Carregando suas turmas…" />}

      {!carregando && vinculos && (
        <Card titulo={`Minhas turmas (${vinculos.length})`}>
          {vinculos.length === 0 ? (
            <EmptyState
              titulo="Nenhuma turma vinculada ainda"
              descricao="Quando a administração vincular você a uma disciplina e turma, elas aparecerão aqui."
            />
          ) : (
            <div className={styles.listaCards}>
              {vinculos.map((vinculo) => (
                <div key={vinculo.id} className={styles.itemCard}>
                  <span className={styles.itemCardTitulo}>{vinculo.turma.nome}</span>
                  <Badge tom="primario">{vinculo.disciplina.nome}</Badge>
                  <span className={styles.itemCardDetalhe}>
                    {vinculo.turma.total_alunos} aluno(s) · {vinculo.turma.ano_letivo}
                  </span>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      <Card titulo="Próximos passos deste painel">
        <p className={styles.textoSecundario}>
          O lançamento de notas, faltas e ocorrências (POST
          /api/academic/notas, /faltas, /ocorrencias) será construído a
          partir de cada turma listada acima. Veja o "Relatório de
          Continuidade" no README do projeto.
        </p>
      </Card>
    </div>
  );
}
