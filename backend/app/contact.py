import os
import re
import smtplib
from email.message import EmailMessage

from flask import Blueprint, jsonify, request

contact_bp = Blueprint('contact', __name__)

EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


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


@contact_bp.route('/send', methods=['POST'])
def send_contact_email():
    data = request.get_json() or {}

    nombre = (data.get('nombre') or '').strip()
    email = (data.get('email') or '').strip().lower()
    asunto = (data.get('asunto') or '').strip()
    mensaje = (data.get('mensaje') or '').strip()

    if not nombre or not email or not asunto or not mensaje:
        return jsonify({'message': 'Debes completar nombre, email, asunto y mensaje.'}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({'message': 'El email no tiene un formato válido.'}), 400

    if len(asunto) > 180 or len(mensaje) > 5000:
        return jsonify({'message': 'El asunto o mensaje es demasiado largo.'}), 400

    body = (
        f"Hola {nombre},\n\n"
        "Gracias por contactar con CoWorkFlow.\n"
        "Hemos recibido correctamente tu mensaje y te responderemos lo antes posible.\n\n"
        "Resumen de tu solicitud:\n"
        f"- Asunto: {asunto}\n"
        f"- Mensaje: {mensaje}\n\n"
        "Un saludo,\n"
        "Equipo CoWorkFlow"
    )

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
                    "name": "CoWorkFlow Soporte",
                    "email": remitente
                },
                "to": [
                    {
                        "email": email,
                        "name": nombre
                    }
                ],
                "subject": f"Hemos recibido tu solicitud: {asunto}",
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

            return jsonify({'message': 'Correo enviado correctamente al usuario.'}), 200
        except Exception as error:
            print(f"Error en Brevo API: {str(error)}")
            return jsonify({'message': f'No se pudo enviar el correo vía Brevo API: {str(error)}'}), 500

    # Fallback SMTP convencional
    smtp_cfg = _get_smtp_config()
    if not smtp_cfg['host'] or not smtp_cfg['user'] or not smtp_cfg['password'] or not smtp_cfg['from_email']:
        return jsonify({
            'message': 'El servicio de correo no está configurado. Define SMTP_HOST, SMTP_USER, SMTP_PASSWORD y SMTP_FROM_EMAIL.'
        }), 503

    correo = EmailMessage()
    correo['Subject'] = f"Hemos recibido tu solicitud: {asunto}"
    correo['From'] = smtp_cfg['from_email']
    correo['To'] = email
    correo.set_content(body)

    try:
        with smtplib.SMTP(smtp_cfg['host'], smtp_cfg['port'], timeout=20) as server:
            if smtp_cfg['use_tls']:
                server.starttls()
            server.login(smtp_cfg['user'], smtp_cfg['password'])
            server.send_message(correo)

        return jsonify({'message': 'Correo enviado correctamente al usuario.'}), 200
    except Exception as error:
        return jsonify({'message': f'No se pudo enviar el correo: {str(error)}'}), 500
