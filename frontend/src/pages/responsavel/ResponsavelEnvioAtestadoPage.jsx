import { useEffect, useRef, useState } from "react";
import { listarMeusAlunos } from "../../api/responsavelService.js";
import { listarFaltasDoAlunoMvp, enviarAtestadoMvp } from "../../api/documentsService.js";
import { useApi } from "../../hooks/useApi.js";
import Card from "../../components/common/Card.jsx";
import Select from "../../components/common/Select.jsx";
import Button from "../../components/common/Button.jsx";
import Alert from "../../components/common/Alert.jsx";
import Badge from "../../components/common/Badge.jsx";
import Spinner from "../../components/common/Spinner.jsx";
import EmptyState from "../../components/common/EmptyState.jsx";
import { formatarData } from "../../utils/formatters.js";
import shell from "../shared/DashboardShell.module.css";
import tabela from "../shared/DataTable.module.css";

const TOM_POR_STATUS = {
  Pendente: "alerta",
  "Em Análise": "primario",
  Justificada: "sucesso",
};

/**
 * Envio de atestado do fluxo "Gestão de Faltas e Atestados" (MVP em
 * memória). O responsável escolhe um dos alunos vinculados a ele, vê as
 * faltas pendentes daquele aluno e anexa o atestado a uma falta
 * específica — o backend muda o status dela para "Em Análise".
 */
export default function ResponsavelEnvioAtestadoPage() {
  const { dados: alunos, carregando: carregandoAlunos } = useApi(listarMeusAlunos);

  const [alunoId, setAlunoId] = useState("");
  const [faltasDoAluno, setFaltasDoAluno] = useState(null);
  const [carregandoFaltas, setCarregandoFaltas] = useState(false);
  const [faltaId, setFaltaId] = useState("");
  const [erro, setErro] = useState(null);
  const [sucessoMsg, setSucessoMsg] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const inputArquivoRef = useRef(null);

  const faltasPendentes = faltasDoAluno?.filter((f) => f.status === "Pendente") || [];

  function carregarFaltasDoAluno(idAluno) {
    if (!idAluno) {
      setFaltasDoAluno(null);
      return;
    }
    setCarregandoFaltas(true);
    // Sem filtro de status aqui: queremos mostrar o histórico completo
    // do aluno (Pendente / Em Análise / Justificada) como contexto.
    listarFaltasDoAlunoMvp(idAluno, null)
      .then(setFaltasDoAluno)
      .catch(() => setErro("Não foi possível carregar as faltas deste aluno."))
      .finally(() => setCarregandoFaltas(false));
  }

  useEffect(() => {
    setFaltaId("");
    carregarFaltasDoAluno(alunoId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [alunoId]);

  async function aoSubmeter(evento) {
    evento.preventDefault();
    setErro(null);
    setSucessoMsg(null);

    const arquivo = inputArquivoRef.current?.files?.[0];
    if (!faltaId) {
      setErro("Selecione a falta que está justificando.");
      return;
    }
    if (!arquivo) {
      setErro("Selecione o arquivo do atestado.");
      return;
    }

    setEnviando(true);
    try {
      await enviarAtestadoMvp(faltaId, arquivo);
      setSucessoMsg("Atestado enviado! Ele já está na fila de análise da escola.");
      setFaltaId("");
      if (inputArquivoRef.current) inputArquivoRef.current.value = "";
      carregarFaltasDoAluno(alunoId);
    } catch (erroCapturado) {
      setErro(erroCapturado.mensagemAmigavel || "Não foi possível enviar o atestado.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className={shell.shell}>
      <header className={shell.boasVindas}>
        <h2>Enviar atestado</h2>
        <p className="text-muted">
          Escolha o aluno, veja as faltas pendentes e anexe o atestado que
          justifica uma delas.
        </p>
      </header>

      <Card titulo="Justificar uma falta">
        <form className={tabela.formulario} onSubmit={aoSubmeter} noValidate>
          <div className={tabela.linhaFormulario}>
            <Select
              rotulo="Aluno"
              value={alunoId}
              onChange={(e) => setAlunoId(e.target.value)}
              disabled={carregandoAlunos}
            >
              <option value="">
                {carregandoAlunos ? "Carregando…" : "Selecione…"}
              </option>
              {alunos?.map((aluno) => (
                <option key={aluno.id} value={aluno.id}>
                  {aluno.nome} · {aluno.matricula}
                </option>
              ))}
            </Select>

            <Select
              rotulo="Falta pendente"
              value={faltaId}
              onChange={(e) => setFaltaId(e.target.value)}
              disabled={!alunoId || carregandoFaltas}
            >
              <option value="">
                {!alunoId
                  ? "Escolha o aluno primeiro"
                  : carregandoFaltas
                  ? "Carregando…"
                  : faltasPendentes.length === 0
                  ? "Nenhuma falta pendente 🎉"
                  : "Selecione…"}
              </option>
              {faltasPendentes.map((falta) => (
                <option key={falta.id} value={falta.id}>
                  {formatarData(falta.data)} · {falta.disciplina}
                </option>
              ))}
            </Select>

            <div>
              <label
                htmlFor="arquivo-atestado"
                style={{
                  display: "block",
                  fontSize: 13,
                  fontWeight: 600,
                  marginBottom: 8,
                }}
              >
                Arquivo do atestado
              </label>
              <input
                id="arquivo-atestado"
                type="file"
                ref={inputArquivoRef}
                accept=".pdf,.jpg,.jpeg,.png"
                disabled={!faltaId}
              />
            </div>
          </div>

          <Alert tom="erro">{erro}</Alert>
          <Alert tom="sucesso">{sucessoMsg}</Alert>

          <div className={tabela.rodapeFormulario}>
            <Button type="submit" carregando={enviando} disabled={!faltaId}>
              Enviar atestado
            </Button>
          </div>
        </form>
      </Card>

      {alunoId && (
        <Card titulo="Faltas deste aluno">
          {carregandoFaltas && <Spinner mensagem="Carregando…" />}

          {!carregandoFaltas && faltasDoAluno && faltasDoAluno.length === 0 && (
            <EmptyState
              titulo="Nenhuma falta registrada"
              descricao="Este aluno ainda não tem faltas registradas neste fluxo."
            />
          )}

          {!carregandoFaltas && faltasDoAluno && faltasDoAluno.length > 0 && (
            <div className={tabela.tabelaWrapper}>
              <table className={tabela.tabela}>
                <thead>
                  <tr>
                    <th>Disciplina</th>
                    <th>Data</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {faltasDoAluno.map((falta) => (
                    <tr key={falta.id}>
                      <td>{falta.disciplina}</td>
                      <td>{formatarData(falta.data)}</td>
                      <td>
                        <Badge tom={TOM_POR_STATUS[falta.status] || "neutro"}>
                          {falta.status}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
