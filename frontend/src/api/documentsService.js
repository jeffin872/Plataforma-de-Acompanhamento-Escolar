import { api } from "./axiosClient.js";
import { ENDPOINTS } from "./endpoints.js";

/**
 * Serviço de Gestão de Documentos.
 * Espelha app/documents/routes.py. O envio usa multipart/form-data porque
 * a rota do backend lê o arquivo via request.files (não JSON).
 */

/** Perfil "responsavel": envia um atestado/documento para um aluno vinculado. */
export async function enviarDocumento(alunoId, arquivo, tipo = "atestado") {
  const formData = new FormData();
  formData.append("aluno_id", alunoId);
  formData.append("tipo", tipo);
  formData.append("arquivo", arquivo);

  const { data } = await api.post(ENDPOINTS.DOCUMENTOS, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data.dados;
}

/** Perfil "responsavel": lista os documentos que ele mesmo enviou. */
export async function listarMeusDocumentos() {
  const { data } = await api.get(ENDPOINTS.DOCUMENTOS_MEUS);
  return data.dados;
}

/** Perfis "admin"/"professor": fila de documentos para análise. */
export async function listarDocumentosParaAnalise(status = "pendente") {
  const { data } = await api.get(ENDPOINTS.DOCUMENTOS, { params: { status } });
  return data.dados;
}

/** Perfis "admin"/"professor": aprova ou rejeita um documento. */
export async function revisarDocumento(documentoId, status, observacao) {
  const { data } = await api.put(ENDPOINTS.DOCUMENTO(documentoId), { status, observacao });
  return data.dados;
}

/** URL para abrir/baixar o arquivo quando STORAGE_BACKEND=local no backend. */
export function urlArquivoLocal(nomeArquivo) {
  const baseURL = import.meta.env.VITE_API_URL || "http://localhost:5000";
  return `${baseURL}${ENDPOINTS.DOCUMENTO_ARQUIVO(nomeArquivo)}`;
}

/**
 * Busca o arquivo de um documento/atestado autenticado (a rota exige o
 * mesmo JWT usado pelo resto da API) e devolve uma URL de blob pronta
 * pra abrir numa nova aba ou embutir num <iframe>/<img>.
 *
 * `urlArquivo` é o caminho já devolvido pelo backend (ex.:
 * "/api/documentos/arquivo/xxxx.pdf" — ver app/documents/storage.py).
 * Um simples <a href> não funcionaria aqui porque essa rota é protegida
 * e o token vive no localStorage, não num cookie.
 */
export async function buscarArquivoComoBlobUrl(urlArquivo) {
  const resposta = await api.get(urlArquivo, { responseType: "blob" });
  return URL.createObjectURL(resposta.data);
}

// ---------------------------------------------------------------------------
// Fluxo MVP "Gestão de Faltas e Atestados" (armazenamento em memória)
// Espelha app/fluxo_faltas/routes.py -> documentos_atestados_bp.
// ---------------------------------------------------------------------------

/**
 * Lista as faltas (do fluxo MVP) de um aluno específico — usada pelo
 * Responsável para escolher, num <select>, qual falta está justificando.
 * Por padrão só traz as pendentes.
 */
export async function listarFaltasDoAlunoMvp(alunoId, status = "Pendente") {
  const { data } = await api.get(ENDPOINTS.DOCUMENTOS_FALTAS_DO_ALUNO(alunoId), {
    params: status ? { status } : undefined,
  });
  return data.dados;
}

/**
 * Envia um atestado vinculado a uma falta específica (multipart/form-data).
 * Ao ser recebido, o backend muda o status dessa falta para "Em Análise".
 */
export async function enviarAtestadoMvp(faltaId, arquivo) {
  const formData = new FormData();
  formData.append("falta_id", faltaId);
  formData.append("arquivo", arquivo);

  const { data } = await api.post(ENDPOINTS.DOCUMENTOS_UPLOAD, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data.dados;
}
