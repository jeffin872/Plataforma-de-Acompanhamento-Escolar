"""
Abstração do canal de e-mail usado pelo Módulo de Alertas e Notificações.

Backend padrão: "console" — apenas registra o e-mail no log da aplicação.
Isso permite testar e demonstrar o fluxo completo do MVP sem precisar de
uma conta paga em nenhum serviço externo.

Para produção, defina EMAIL_BACKEND=sendgrid e SENDGRID_API_KEY no .env
(é necessário instalar `sendgrid`, que fica fora do requirements.txt
padrão para manter o setup local mais leve).
"""
from flask import current_app


def enviar_email(destinatario: str, assunto: str, mensagem: str) -> None:
    backend = current_app.config.get("EMAIL_BACKEND", "console")

    if backend == "sendgrid":
        _enviar_via_sendgrid(destinatario, assunto, mensagem)
    else:
        _enviar_via_console(destinatario, assunto, mensagem)


def _enviar_via_console(destinatario: str, assunto: str, mensagem: str) -> None:
    current_app.logger.info(
        "[E-MAIL SIMULADO] Para: %s | Assunto: %s | Mensagem: %s",
        destinatario, assunto, mensagem,
    )


def _enviar_via_sendgrid(destinatario: str, assunto: str, mensagem: str) -> None:
    from sendgrid import SendGridAPIClient  # import tardio: só necessário em produção
    from sendgrid.helpers.mail import Mail

    email = Mail(
        from_email=current_app.config["EMAIL_REMETENTE"],
        to_emails=destinatario,
        subject=assunto,
        plain_text_content=mensagem,
    )
    cliente = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
    cliente.send(email)
