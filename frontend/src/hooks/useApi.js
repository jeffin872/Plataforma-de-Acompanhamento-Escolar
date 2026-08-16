import { useCallback, useEffect, useState } from "react";

/**
 * Evita repetir "const [dados, setDados] = useState(); const [carregando...]"
 * em toda página que busca algo na API ao montar.
 *
 * Uso:
 *   const { dados, carregando, erro, recarregar } = useApi(() => buscarDashboardAdmin());
 *
 * `dependencias` funciona como o array de um useEffect normal — passe os
 * valores que, ao mudar, devem disparar uma nova busca.
 */
export function useApi(funcaoAssincrona, dependencias = []) {
  const [dados, setDados] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  const executar = useCallback(() => {
    let cancelado = false;
    setCarregando(true);
    setErro(null);

    funcaoAssincrona()
      .then((resultado) => {
        if (!cancelado) setDados(resultado);
      })
      .catch((erroCapturado) => {
        if (!cancelado) {
          setErro(erroCapturado.mensagemAmigavel || "Não foi possível carregar os dados.");
        }
      })
      .finally(() => {
        if (!cancelado) setCarregando(false);
      });

    return () => {
      cancelado = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencias);

  useEffect(() => executar(), [executar]);

  return { dados, carregando, erro, recarregar: executar };
}
