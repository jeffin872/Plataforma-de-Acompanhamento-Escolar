/**
 * Formata uma data no padrão "AAAA-MM-DD" (formato que a API sempre
 * devolve, ver *_to_dict() no backend) para o padrão brasileiro DD/MM/AAAA.
 * Retorna "—" quando a data é nula, para nunca exibir "Invalid Date" na tela.
 */
export function formatarData(dataIso) {
  if (!dataIso) return "—";
  const [ano, mes, dia] = dataIso.split("-");
  if (!ano || !mes || !dia) return dataIso;
  return `${dia}/${mes}/${ano}`;
}

/** Formata data + hora ISO (com timezone) vinda de campos *_em do backend. */
export function formatarDataHora(dataHoraIso) {
  if (!dataHoraIso) return "—";
  const data = new Date(dataHoraIso);
  if (Number.isNaN(data.getTime())) return "—";
  return data.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/** Extrai até duas iniciais de um nome completo, para avatares. */
export function iniciais(nomeCompleto = "") {
  const partes = nomeCompleto.trim().split(/\s+/).filter(Boolean);
  if (partes.length === 0) return "?";
  if (partes.length === 1) return partes[0].slice(0, 2).toUpperCase();
  return (partes[0][0] + partes[partes.length - 1][0]).toUpperCase();
}
