import smtplib
from email.message import EmailMessage
from config import EMAIL_FROM, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SMTP

def send_email(to_email: str, subject: str, body: str) -> bool:
    if not EMAIL_FROM or not EMAIL_PASSWORD:
        raise RuntimeError("Configuração de e-mail incompleta. Defina EMAIL_FROM e EMAIL_PASSWORD nas varíaveis de ambiente.")
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL(EMAIL_SMTP, EMAIL_PORT) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"[ERRO EMAIL] {e}")
        return False
    