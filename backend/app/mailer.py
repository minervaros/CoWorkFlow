import os
import smtplib
from email.message import EmailMessage

def _get_smtp_config():
    host = os.getenv('SMTP_HOST', '').strip()
    port = int(os.getenv('SMTP_PORT', '587'))
    user = os.getenv('SMTP_USER', '').strip()
    password = os.getenv('SMTP_PASSWORD', '').strip()
    from_email = os.getenv('SMTP_FROM_EMAIL', user).strip()
    use_tls = os.getenv('SMTP_USE_TLS', 'true').strip().lower() in ('1', 'true', 'yes', 'on')

    return {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'from_email': from_email,
        'use_tls': use_tls
    }

def send_email(to_email, to_name, subject, body, sender_name="CoWorkFlow"):
    brevo_key = os.getenv('BREVO_API_KEY', '').strip()
    
    if brevo_key:
        try:
            import urllib.request
            import json
            url = "https://api.brevo.com/v3/smtp/email"
            headers = {
                "accept": "application/json",
                "api-key": brevo_key,
                "content-type": "application/json"
            }
            remitente = os.getenv('SMTP_FROM_EMAIL', 'minervarosich05@gmail.com').strip()

            payload = {
                "sender": {
                    "name": sender_name,
                    "email": remitente
                },
                "to": [
                    {
                        "email": to_email,
                        "name": to_name
                    }
                ],
                "subject": subject,
                "textContent": body
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                response.read()
            return True, None
        except Exception as error:
            print(f"Error en Brevo API al enviar correo: {str(error)}")
            return False, f"Error en Brevo API: {str(error)}"

    # Fallback SMTP convencional
    smtp_cfg = _get_smtp_config()
    if not smtp_cfg['host'] or not smtp_cfg['user'] or not smtp_cfg['password'] or not smtp_cfg['from_email']:
        return False, 'El servicio de correo no está configurado.'

    correo = EmailMessage()
    correo['Subject'] = subject
    correo['From'] = smtp_cfg['from_email']
    correo['To'] = to_email
    correo.set_content(body)

    try:
        with smtplib.SMTP(smtp_cfg['host'], smtp_cfg['port'], timeout=20) as server:
            if smtp_cfg['use_tls']:
                server.starttls()
            server.login(smtp_cfg['user'], smtp_cfg['password'])
            server.send_message(correo)
        return True, None
    except Exception as error:
        return False, str(error)
