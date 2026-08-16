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
