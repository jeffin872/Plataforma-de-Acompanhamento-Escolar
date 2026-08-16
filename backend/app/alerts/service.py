"""
Regras automáticas de alerta. Hoje cobre o cenário citado na documentação
("alerta de excesso de faltas"); novos gatilhos (ex: nota baixa recorrente)
podem ser adicionados aqui seguindo o mesmo padrão: checar a condição,
criar uma Notificacao e chamar enviar_email().
"""
from flask import current_app

from app.extensions import db
from app.models import Aluno, Falta, ResponsavelAluno, Notificacao
from app.alerts.email_sender import enviar_email


def verificar_excesso_faltas(aluno_id: int) -> bool:
    """
    Conta as faltas não justificadas do aluno; se atingir o limite
    configurado (LIMITE_FALTAS_ALERTA, padrão 5), dispara notificação +
    e-mail para todos os responsáveis vinculados a ele.

    Retorna True se um alerta foi disparado nesta chamada.
    """
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return False

    total_nao_justificadas = Falta.query.filter_by(
        aluno_id=aluno_id, justificada=False
    ).count()
    limite = current_app.config.get("LIMITE_FALTAS_ALERTA", 5)

    if total_nao_justificadas < limite or total_nao_justificadas % limite != 0:
        # Só alerta ao cruzar o limite (e a cada novo múltiplo dele), para
        # não mandar um e-mail novo a cada falta registrada depois disso.
        return False

    responsaveis = ResponsavelAluno.query.filter_by(aluno_id=aluno_id).all()
    mensagem = (
        f"O(a) aluno(a) {aluno.nome} atingiu {total_nao_justificadas} faltas "
        f"não justificadas. Fique atento(a) à frequência escolar."
    )

    for vinculo in responsaveis:
        db.session.add(Notificacao(
            usuario_id=vinculo.responsavel_id,
            tipo="excesso_faltas",
            mensagem=mensagem,
        ))
        enviar_email(
            destinatario=vinculo.responsavel.email,
            assunto="Alerta de frequência escolar",
            mensagem=mensagem,
        )

    db.session.commit()
    return True
