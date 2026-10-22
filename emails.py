import smtplib
from email.message import EmailMessage

import config


def enviar_email(destino, assunto, texto):
    """Envia um e-mail de texto simples. Devolve True se enviou."""
    if not config.MAIL_USERNAME or not config.MAIL_PASSWORD:
        # Sem SMTP configurado: mostra o e-mail no terminal (modo de teste)
        print(f"\n--- E-MAIL (modo de teste) ---\nPara: {destino}\nAssunto: {assunto}\n\n{texto}\n---\n")
        return True

    mensagem = EmailMessage()
    mensagem["Subject"] = assunto
    mensagem["From"] = config.MAIL_FROM
    mensagem["To"] = destino
    mensagem.set_content(texto)

    try:
        with smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT, timeout=15) as servidor:
            servidor.starttls()
            servidor.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
            servidor.send_message(mensagem)
        return True
    except (smtplib.SMTPException, OSError, ValueError) as erro:
        print(f"Falha ao enviar e-mail: {erro}")
        return False