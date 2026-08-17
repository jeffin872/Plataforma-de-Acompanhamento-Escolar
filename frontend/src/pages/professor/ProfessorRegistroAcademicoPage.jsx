import { useEffect, useState } from "react";
import { listarMinhasTurmas } from "../../api/academicService.js";
import { detalharTurma } from "../../api/adminService.js";
import { listarFaltasMvp, registrarFaltaMvp } from "../../api/professorService.js";
import { useApi } from "../../hooks/useApi.js";
import Card from "../../components/common/Card.jsx";
import Select from "../../components/common/Select.jsx";
import Input from "../../components/common/Input.jsx";
import Button from "../../components/common/Button.jsx";
import Alert from "../../components/common/Alert.jsx";
import Badge from "../../components/common/Badge.jsx";
import Spinner from "../../components/common/Spinner.jsx";
import EmptyState from "../../components/common/EmptyState.jsx";
import { formatarData, formatarDataHora } from "../../utils/formatters.js";
import shell from "../shared/DashboardShell.module.css";
import tabela from "../shared/DataTable.module.css";

const TOM_POR_STATUS = {
  Pendente: "alerta",
  "Em Análise": "primario",
  Justificada: "sucesso",
};

/**
 * Registro de faltas do fluxo "Gestão de Faltas e Atestados" (MVP em
 * memória — ver professorService.js). O professor escolhe um vínculo
 * (turma + disciplina) já cadastrado para ele, depois um aluno daquela
 * turma, e registra a falta — que nasce sempre com status "Pendente".
 */
export default function ProfessorRegistroAcademicoPage() {
  const { dados: vinculos, carregando: carregandoVinculos } = useApi(listarMinhasTurmas);
  const {
    dados: faltas,
    carregando: carregandoFaltas,
    erro: erroFaltas,
    recarregar: recarregarFaltas,
  } = useApi(() => listarFaltasMvp());

  const [vinculoId, setVinculoId] = useState("");
  const [alunoId, setAlunoId] = useState("");
  const [dataFalta, setDataFalta] = useState("");
  const [alunosDaTurma, setAlunosDaTurma] = useState([]);
  const [carregandoAlunos, setCarregandoAlunos] = useState(false);
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState(null);
  const [sucessoMsg, setSucessoMsg] = useState(null);

  const vinculoSelecionado = vinculos?.find((v) => String(v.id) === vinculoId);

  // Ao trocar de vínculo (turma+disciplina), busca os alunos daquela turma.
  useEffect(() => {
    setAlunoId("");
    setAlunosDaTurma([]);
    if (!vinculoSelecionado) return;

    let cancelado = false;
    setCarregandoAlunos(true);
    detalharTurma(vinculoSelecionado.turma.id)
      .then((turma) => {
        if (!cancelado) setAlunosDaTurma(turma.alunos || []);
      })
      .catch(() => {
        if (!cancelado) setErro("Não foi possível carregar os alunos desta turma.");
      })
      .finally(() => {
        if (!cancelado) setCarregandoAlunos(false);
      });

    return () => {
      cancelado = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [vinculoId]);

  async function aoSubmeter(evento) {
    evento.preventDefault();
    setErro(null);
    setSucessoMsg(null);

    if (!vinculoSelecionado || !alunoId || !dataFalta) {
      setErro("Selecione a turma/disciplina, o aluno e a data da falta.");
      return;
    }

    setEnviando(true);
    try {
      await registrarFaltaMvp({
        alunoId: Number(alunoId),
        data: dataFalta,
        disciplina: vinculoSelecionado.disciplina.nome,
      });
      setSucessoMsg("Falta registrada com sucesso — status inicial: Pendente.");
      setAlunoId("");
      setDataFalta("");
      recarregarFaltas();
    } catch (erroCapturado) {
      setErro(erroCapturado.mensagemAmigavel || "Não foi possível registrar a falta.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className={shell.shell}>
      <header className={shell.boasVindas}>
        <h2>Registro de faltas</h2>
        <p className="text-muted">
          Registre uma falta por aluno — ela entra na fila do responsável como
          "Pendente" até que um atestado seja enviado e aprovado.
        </p>
      </header>

      <Card titulo="Nova falta">
        <form className={tabela.formulario} onSubmit={aoSubmeter} noValidate>
          <div className={tabela.linhaFormulario}>
            <Select
              rotulo="Turma / disciplina"
              value={vinculoId}
              onChange={(e) => setVinculoId(e.target.value)}
              disabled={carregandoVinculos}
            >
              <option value="">
                {carregandoVinculos ? "Carregando…" : "Selecione…"}
              </option>
              {vinculos?.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.turma.nome} · {v.disciplina.nome}
                </option>
              ))}
            </Select>

            <Select
              rotulo="Aluno"
              value={alunoId}
              onChange={(e) => setAlunoId(e.target.value)}
              disabled={!vinculoSelecionado || carregandoAlunos}
            >
              <option value="">
                {!vinculoSelecionado
                  ? "Escolha a turma primeiro"
                  : carregandoAlunos
                  ? "Carregando…"
                  : alunosDaTurma.length === 0
                  ? "Nenhum aluno nesta turma"
                  : "Selecione…"}
              </option>
              {alunosDaTurma.map((aluno) => (
                <option key={aluno.id} value={aluno.id}>
                  {aluno.nome} · {aluno.matricula}
                </option>
              ))}
            </Select>

            <Input
              rotulo="Data da falta"
              type="date"
              value={dataFalta}
              onChange={(e) => setDataFalta(e.target.value)}
            />
          </div>

          <Alert tom="erro">{erro}</Alert>
          <Alert tom="sucesso">{sucessoMsg}</Alert>

          <div className={tabela.rodapeFormulario}>
            <Button type="submit" carregando={enviando}>
              Registrar falta
            </Button>
          </div>
        </form>
      </Card>

      <Card titulo="Faltas registradas neste fluxo">
        {erroFaltas && <Alert tom="erro">{erroFaltas}</Alert>}
        {carregandoFaltas && <Spinner mensagem="Carregando faltas…" />}

        {!carregandoFaltas && faltas && faltas.length === 0 && (
          <EmptyState
            titulo="Nenhuma falta registrada ainda"
            descricao="As faltas que você registrar acima vão aparecer nesta lista."
          />
        )}

        {!carregandoFaltas && faltas && faltas.length > 0 && (
          <div className={tabela.tabelaWrapper}>
            <table className={tabela.tabela}>
              <thead>
                <tr>
                  <th>Aluno</th>
                  <th>Disciplina</th>
                  <th>Data</th>
                  <th>Status</th>
                  <th>Registrada em</th>
                </tr>
              </thead>
              <tbody>
                {faltas.map((falta) => (
                  <tr key={falta.id}>
                    <td>{falta.aluno_nome}</td>
                    <td>{falta.disciplina}</td>
                    <td>{formatarData(falta.data)}</td>
                    <td>
                      <Badge tom={TOM_POR_STATUS[falta.status] || "neutro"}>
                        {falta.status}
                      </Badge>
                    </td>
                    <td className="text-muted">{formatarDataHora(falta.registrado_em)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
