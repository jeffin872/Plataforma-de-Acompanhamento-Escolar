import { useEffect, useState } from "react";
import { listarAtestadosPendentesMvp, validarAtestadoMvp } from "../../api/adminService.js";
import { buscarArquivoComoBlobUrl } from "../../api/documentsService.js";
import { useApi } from "../../hooks/useApi.js";
import Card from "../../components/common/Card.jsx";
import Button from "../../components/common/Button.jsx";
import Alert from "../../components/common/Alert.jsx";
import Badge from "../../components/common/Badge.jsx";
import Spinner from "../../components/common/Spinner.jsx";
import EmptyState from "../../components/common/EmptyState.jsx";
import { formatarData, formatarDataHora } from "../../utils/formatters.js";
import shell from "../shared/DashboardShell.module.css";
import styles from "./AdminValidarAtestadosPage.module.css";

const EXTENSOES_IMAGEM = ["jpg", "jpeg", "png"];

function extensaoDoArquivo(nomeArquivo) {
  if (!nomeArquivo || !nomeArquivo.includes(".")) return "";
  return nomeArquivo.split(".").pop().toLowerCase();
}

/**
 * Fila de análise do fluxo "Gestão de Faltas e Atestados" (MVP em
 * memória). Lista os atestados "Em Análise" à esquerda e, ao selecionar
 * um deles, mostra o documento enviado e os dados vinculados à direita
 * — o Administrador pode visualizar o arquivo de verdade e então
 * Aprovar/Recusar (ao aprovar, a falta vinculada vira automaticamente
 * "Justificada" no backend, ver app/fluxo_faltas/routes.py).
 */
export default function AdminValidarAtestadosPage() {
  const {
    dados: atestados,
    carregando,
    erro: erroLista,
    recarregar,
  } = useApi(() => listarAtestadosPendentesMvp());

  // Controla qual atestado está selecionado (coluna da direita) e qual
  // está com uma ação em andamento, pra desabilitar só os botões
  // daquele card durante o request.
  const [selecionadoId, setSelecionadoId] = useState(null);
  const [idEmAcao, setIdEmAcao] = useState(null);
  const [erroAcao, setErroAcao] = useState(null);

  const [blobUrl, setBlobUrl] = useState(null);
  const [carregandoArquivo, setCarregandoArquivo] = useState(false);
  const [erroArquivo, setErroArquivo] = useState(null);

  // Seleciona automaticamente o primeiro atestado da fila — e reajusta a
  // seleção sempre que a lista muda (ex.: depois de aprovar/recusar, o
  // item selecionado some da fila de "Em Análise").
  useEffect(() => {
    if (!atestados || atestados.length === 0) {
      setSelecionadoId(null);
      return;
    }
    setSelecionadoId((atual) =>
      atual && atestados.some((a) => a.id === atual) ? atual : atestados[0].id
    );
  }, [atestados]);

  const selecionado = atestados?.find((a) => a.id === selecionadoId) || null;

  // Busca o arquivo (autenticado) sempre que a seleção muda, pra exibir
  // uma prévia real do atestado no painel de análise.
  useEffect(() => {
    setBlobUrl((urlAnterior) => {
      if (urlAnterior) URL.revokeObjectURL(urlAnterior);
      return null;
    });
    setErroArquivo(null);

    if (!selecionado?.url_arquivo) return;

    let cancelado = false;
    setCarregandoArquivo(true);
    buscarArquivoComoBlobUrl(selecionado.url_arquivo)
      .then((url) => {
        if (!cancelado) setBlobUrl(url);
      })
      .catch(() => {
        if (!cancelado) setErroArquivo("Não foi possível carregar o arquivo do atestado.");
      })
      .finally(() => {
        if (!cancelado) setCarregandoArquivo(false);
      });

    return () => {
      cancelado = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selecionado?.id, selecionado?.url_arquivo]);

  async function validar(atestadoId, acao) {
    setErroAcao(null);
    setIdEmAcao(atestadoId);
    try {
      await validarAtestadoMvp(atestadoId, acao);
      recarregar();
    } catch (erroCapturado) {
      setErroAcao(erroCapturado.mensagemAmigavel || "Não foi possível concluir a análise.");
    } finally {
      setIdEmAcao(null);
    }
  }

  const extensao = extensaoDoArquivo(selecionado?.nome_arquivo);
  const ehImagem = EXTENSOES_IMAGEM.includes(extensao);
  const ehPdf = extensao === "pdf";
  const emAcaoSelecionado = selecionado && idEmAcao === selecionado.id;

  return (
    <div className={shell.shell}>
      <header className={shell.boasVindas}>
        <h2>Validar atestados</h2>
        <p className="text-muted">
          Analise os documentos enviados pelos responsáveis antes de aprovar ou recusar.
        </p>
      </header>

      {erroAcao && <Alert tom="erro">{erroAcao}</Alert>}
      {erroLista && <Alert tom="erro">{erroLista}</Alert>}

      {carregando && <Spinner mensagem="Carregando atestados…" />}

      {!carregando && atestados && atestados.length === 0 && (
        <Card>
          <EmptyState
            titulo="Nenhum atestado pendente"
            descricao="Quando um responsável enviar um atestado, ele aparece aqui para análise."
          />
        </Card>
      )}

      {!carregando && atestados && atestados.length > 0 && (
        <div className={styles.duasColunas}>
          <Card titulo={`Pendências de validação (${atestados.length})`}>
            <div className={styles.lista}>
              {atestados.map((atestado) => {
                const selecionadoAtual = atestado.id === selecionadoId;
                return (
                  <button
                    key={atestado.id}
                    type="button"
                    className={`${styles.itemLista} ${
                      selecionadoAtual ? styles.itemListaSelecionado : ""
                    }`}
                    onClick={() => setSelecionadoId(atestado.id)}
                    aria-pressed={selecionadoAtual}
                  >
                    <div className={styles.itemListaTopo}>
                      <span className={styles.itemListaNome}>{atestado.aluno_nome}</span>
                      <Badge tom="alerta">Pendente</Badge>
                    </div>
                    <span className={styles.itemListaDetalhe}>
                      {formatarData(atestado.data_falta)} · {atestado.disciplina}
                    </span>
                  </button>
                );
              })}
            </div>
          </Card>

          {selecionado && (
            <Card titulo="Análise do documento">
              <div className={styles.painelAnalise}>
                <div className={styles.previewBox}>
                  {carregandoArquivo && <Spinner mensagem="Carregando arquivo…" />}

                  {!carregandoArquivo && blobUrl && ehImagem && (
                    <img
                      className={styles.previewImagem}
                      src={blobUrl}
                      alt={`Atestado enviado: ${selecionado.nome_arquivo}`}
                    />
                  )}

                  {!carregandoArquivo && blobUrl && ehPdf && (
                    <iframe
                      className={styles.previewIframe}
                      src={blobUrl}
                      title={`Atestado enviado: ${selecionado.nome_arquivo}`}
                    />
                  )}

                  {!carregandoArquivo && !blobUrl && (
                    <div className={styles.previewIndisponivel}>
                      <span className={styles.selo} aria-hidden="true">
                        {extensao ? extensao.toUpperCase() : "DOC"}
                      </span>
                      <span className={styles.nomeArquivo}>{selecionado.nome_arquivo}</span>
                      {erroArquivo ? (
                        <Alert tom="erro">{erroArquivo}</Alert>
                      ) : (
                        <p className="text-muted" style={{ fontSize: 13 }}>
                          Prévia não disponível para este arquivo.
                        </p>
                      )}
                    </div>
                  )}
                </div>

                {blobUrl && (
                  <div className={styles.acoesArquivo}>
                    <Button
                      variante="secundaria"
                      type="button"
                      onClick={() => window.open(blobUrl, "_blank", "noopener")}
                    >
                      Abrir em nova aba
                    </Button>
                    <Button
                      variante="texto"
                      type="button"
                      onClick={() => {
                        const link = document.createElement("a");
                        link.href = blobUrl;
                        link.download = selecionado.nome_arquivo || "atestado";
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                      }}
                    >
                      Baixar arquivo
                    </Button>
                  </div>
                )}

                <dl className={styles.dadosVinculados}>
                  <div className={styles.dadosVinculadosItem}>
                    <dt>Estudante</dt>
                    <dd>{selecionado.aluno_nome}</dd>
                  </div>
                  <div className={styles.dadosVinculadosItem}>
                    <dt>Disciplina</dt>
                    <dd>{selecionado.disciplina}</dd>
                  </div>
                  <div className={styles.dadosVinculadosItem}>
                    <dt>Falta justificada</dt>
                    <dd>{formatarData(selecionado.data_falta)}</dd>
                  </div>
                  <div className={styles.dadosVinculadosItem}>
                    <dt>Responsável</dt>
                    <dd>{selecionado.responsavel_nome}</dd>
                  </div>
                  <div className={styles.dadosVinculadosItem}>
                    <dt>Enviado em</dt>
                    <dd>{formatarDataHora(selecionado.enviado_em)}</dd>
                  </div>
                  <div className={styles.dadosVinculadosItem}>
                    <dt>Status atual</dt>
                    <dd>
                      <Badge tom="primario">{selecionado.status}</Badge>
                    </dd>
                  </div>
                </dl>

                <div className={styles.acoesDecisao}>
                  <Button
                    variante="perigo"
                    carregando={emAcaoSelecionado}
                    disabled={idEmAcao !== null && !emAcaoSelecionado}
                    onClick={() => validar(selecionado.id, "rejeitar")}
                  >
                    Recusar
                  </Button>
                  <Button
                    variante="primaria"
                    carregando={emAcaoSelecionado}
                    disabled={idEmAcao !== null && !emAcaoSelecionado}
                    onClick={() => validar(selecionado.id, "aprovar")}
                  >
                    Aprovar atestado
                  </Button>
                </div>
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
