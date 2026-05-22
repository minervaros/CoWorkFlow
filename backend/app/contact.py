import os
import re

from flask import Blueprint, jsonify, request
from app.mailer import send_email

contact_bp = Blueprint('contact', __name__)

EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


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

    sent, error = send_email(
        to_email=email,
        to_name=nombre,
        subject=f"Hemos recibido tu solicitud: {asunto}",
        body=body,
        sender_name="CoWorkFlow Soporte"
    )

    if not sent:
        return jsonify({'message': f'No se pudo enviar el correo: {error}'}), 500

    return jsonify({'message': 'Correo enviado correctamente al usuario.'}), 200

