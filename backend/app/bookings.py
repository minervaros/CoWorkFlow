from flask import Blueprint, request, jsonify
from app import db
from app.models import Booking, Room, TourBooking, User
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
from sqlalchemy import or_
import os
import re
import smtplib
from email.message import EmailMessage

bookings_bp = Blueprint('bookings', __name__)

SEDE_LOCATION_HINTS = {
    'ruzafa': ['ruzafa'],
    'el-carmen': ['el carmen', 'carmen'],
    'eixample': ['eixample'],
    'el-cabanyal': ['cabanyal', 'el cabanyal']
}

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


def send_tour_confirmation_email(to_email, full_name, sede_name, fecha, hora, people_count, company_name):
    smtp_cfg = _get_smtp_config()
    if not smtp_cfg['host'] or not smtp_cfg['user'] or not smtp_cfg['password'] or not smtp_cfg['from_email']:
        return False, 'El servicio de correo no está configurado en el servidor.'

    correo = EmailMessage()
    correo['Subject'] = f"Confirmación de tour en {sede_name}"
    correo['From'] = smtp_cfg['from_email']
    correo['To'] = to_email
    correo.set_content(
        f"Hola {full_name},\n\n"
        "Tu solicitud de tour se ha registrado correctamente con estos datos:\n"
        f"- Sede: {sede_name}\n"
        f"- Fecha: {fecha}\n"
        f"- Hora: {hora}\n"
        f"- Personas: {people_count}\n"
        f"- Empresa/autónomo: {company_name}\n\n"
        "Nos pondremos en contacto contigo para confirmar los detalles.\n\n"
        "Equipo CoWorkFlow"
    )

    try:
        with smtplib.SMTP(smtp_cfg['host'], smtp_cfg['port'], timeout=20) as server:
            if smtp_cfg['use_tls']:
                server.starttls()
            server.login(smtp_cfg['user'], smtp_cfg['password'])
            server.send_message(correo)
        return True, None
    except Exception as error:
        return False, str(error)


def send_room_booking_confirmation_email(to_email, full_name, room_name, start_dt, end_dt, total_price, payment_status, payment_method):
    smtp_cfg = _get_smtp_config()
    if not smtp_cfg['host'] or not smtp_cfg['user'] or not smtp_cfg['password'] or not smtp_cfg['from_email']:
        return False, 'El servicio de correo no está configurado en el servidor.'

    fecha = start_dt.strftime('%Y-%m-%d')
    hora_inicio = start_dt.strftime('%H:%M')
    hora_fin = end_dt.strftime('%H:%M')

    correo = EmailMessage()
    correo['Subject'] = f"Confirmación de reserva - {room_name}"
    correo['From'] = smtp_cfg['from_email']
    correo['To'] = to_email

    metodo_txt = 'Plataforma online' if payment_method == 'platform' else 'Recepción'
    estado_txt = 'Pagada' if payment_status == 'paid' else 'Pendiente'

    correo.set_content(
        f"Hola {full_name},\n\n"
        "Tu reserva de sala se ha registrado correctamente:\n"
        f"- Sala: {room_name}\n"
        f"- Fecha: {fecha}\n"
        f"- Hora inicio: {hora_inicio}\n"
        f"- Hora fin: {hora_fin}\n"
        f"- Total: {total_price:.2f} €\n\n"
        f"- Método de pago: {metodo_txt}\n"
        f"- Estado de pago: {estado_txt}\n\n"
        "Gracias por confiar en CoWorkFlow.\n\n"
        "Equipo CoWorkFlow"
    )

    try:
        with smtplib.SMTP(smtp_cfg['host'], smtp_cfg['port'], timeout=20) as server:
            if smtp_cfg['use_tls']:
                server.starttls()
            server.login(smtp_cfg['user'], smtp_cfg['password'])
            server.send_message(correo)
        return True, None
    except Exception as error:
        return False, str(error)


def find_tour_conflict(sede_slug, start, end):
    location_filters = [Room.location.ilike(f"%{hint}%") for hint in SEDE_LOCATION_HINTS[sede_slug]]
    rooms = Room.query.filter(
        Room.is_active == True,
        or_(*location_filters)
    ).all()

    if not rooms:
        return None, None, "No hay salas activas para la sede seleccionada."

    room_ids = [room.id for room in rooms]

    overlapping_room_booking = Booking.query.filter(
        Booking.room_id.in_(room_ids),
        Booking.status == 'confirmed',
        Booking.start_time < end,
        Booking.end_time > start
    ).order_by(Booking.start_time.asc()).first()

    if overlapping_room_booking:
        return overlapping_room_booking, 'room', None

    overlapping_tour_booking = TourBooking.query.filter(
        TourBooking.sede_slug == sede_slug,
        or_(TourBooking.status.is_(None), TourBooking.status != 'cancelled'),
        TourBooking.start_time < end,
        TourBooking.end_time > start
    ).order_by(TourBooking.start_time.asc()).first()

    if overlapping_tour_booking:
        return overlapping_tour_booking, 'tour', None

    return None, None, None

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    room_id = data.get('room_id')
    start_str = data.get('start_time')
    end_str = data.get('end_time')
    payment_status = (data.get('payment_status') or 'pending').strip().lower()
    payment_method = (data.get('payment_method') or 'reception').strip().lower()

    valid_payment_statuses = {'paid', 'pending', 'reception'}
    valid_payment_methods = {'platform', 'reception'}

    if payment_status not in valid_payment_statuses:
        return jsonify({"message": "Estado de pago inválido."}), 400

    if payment_method not in valid_payment_methods:
        return jsonify({"message": "Método de pago inválido."}), 400

    if payment_method == 'platform' and payment_status != 'paid':
        return jsonify({"message": "El pago en plataforma debe guardarse como pagado."}), 400

    if payment_method == 'reception' and payment_status == 'paid':
        return jsonify({"message": "El pago en recepción no puede guardarse como pagado."}), 400

    # 1. Validaciones básicas y conversión de fechas (Esto ya lo tienes)
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"message": "La sala no existe"}), 404
    
    if not room.is_active:
        return jsonify({"message": "La sala no está disponible actualmente"}), 400

    try:
        start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
    except:
        return jsonify({"message": "Formato de fecha inválido"}), 400
    
    if start < datetime.now():
        return jsonify({"message": "No puedes realizar una reserva en una fecha pasada"}), 400

    if (end - start).total_seconds() <= 0:
        return jsonify({"message": "La hora de fin debe ser posterior a la de inicio"}), 400

    # --- VALIDACIÓN DE DISPONIBILIDAD (Solapamiento) ---
    # Buscamos si existe alguna reserva que choque con este horario
    overlapping_booking = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status == 'confirmed',
        Booking.start_time < end,  # La reserva existente empieza antes de que yo termine
        Booking.end_time > start   # La reserva existente termina después de que yo empiece
    ).first()

    if overlapping_booking:
        return jsonify({
            "message": "La sala ya está reservada en ese horario",
            "conflict": {
                "start": overlapping_booking.start_time.strftime('%H:%M'),
                "end": overlapping_booking.end_time.strftime('%H:%M')
            }
        }), 409 # Código 409: Conflict


    # Si pasa la validación, calculamos precio y guardamos 
    duration = (end - start).total_seconds() / 3600
    price = round(duration * room.price_per_hour, 2)

    new_booking = Booking(
        user_id=current_user_id,
        room_id=room_id,
        start_time=start,
        end_time=end,
        total_price=price,
        payment_status=payment_status,
        payment_method=payment_method
    )

    db.session.add(new_booking)
    db.session.commit()

    user = User.query.get(current_user_id)
    if user and user.email:
        sent, email_error = send_room_booking_confirmation_email(
            to_email=user.email,
            full_name=user.full_name or 'usuario',
            room_name=room.name,
            start_dt=start,
            end_dt=end,
            total_price=price,
            payment_status=payment_status,
            payment_method=payment_method
        )

        if not sent:
            return jsonify({
                "message": "Reserva realizada con éxito, pero no se pudo enviar el correo de confirmación.",
                "total_price": price,
                "payment_status": payment_status,
                "payment_method": payment_method,
                "email_error": email_error
            }), 202

    return jsonify({
        "message": "Reserva realizada con éxito",
        "total_price": price,
        "payment_status": payment_status,
        "payment_method": payment_method
    }), 201


@bookings_bp.route('/tour-availability', methods=['POST'])
@jwt_required()
def check_tour_availability():
    data = request.get_json() or {}

    sede = (data.get('sede') or '').strip().lower()
    fecha = (data.get('fecha') or '').strip()
    hora = (data.get('hora') or '').strip()

    if not sede or not fecha or not hora:
        return jsonify({
            "message": "Debes indicar sede, fecha y hora para validar disponibilidad."
        }), 400

    if sede not in SEDE_LOCATION_HINTS:
        return jsonify({"message": "La sede seleccionada no es válida."}), 400

    try:
        start = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')
    except Exception:
        return jsonify({"message": "Formato de fecha u hora inválido."}), 400

    if start < datetime.now():
        return jsonify({"message": "No puedes reservar un tour en una fecha pasada."}), 400

    end = start + timedelta(hours=1)

    conflict, conflict_type, no_rooms_message = find_tour_conflict(sede, start, end)
    if no_rooms_message:
        return jsonify({"message": no_rooms_message}), 404

    if conflict and conflict_type == 'room':
        return jsonify({
            "available": False,
            "message": "Ya existe una reserva en esa sede para esa franja horaria.",
            "conflict": {
                "room_name": conflict.room.name,
                "start": conflict.start_time.strftime('%Y-%m-%d %H:%M'),
                "end": conflict.end_time.strftime('%Y-%m-%d %H:%M')
            }
        }), 409

    if conflict and conflict_type == 'tour':
        return jsonify({
            "available": False,
            "message": "Ya hay un tour solicitado para esa sede en esa franja horaria.",
            "conflict": {
                "room_name": "Tour en sede",
                "start": conflict.start_time.strftime('%Y-%m-%d %H:%M'),
                "end": conflict.end_time.strftime('%Y-%m-%d %H:%M')
            }
        }), 409

    return jsonify({
        "available": True,
        "message": "Horario disponible para reservar el tour."
    }), 200


@bookings_bp.route('/tour-reservations', methods=['POST'])
@jwt_required()
def create_tour_reservation():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}

    sede = (data.get('sede') or '').strip().lower()
    fecha = (data.get('fecha') or '').strip()
    hora = (data.get('hora') or '').strip()
    full_name = (data.get('nombre_completo') or '').strip()
    email = (data.get('correo') or '').strip().lower()
    phone = (data.get('telefono') or '').strip()
    company_name = (data.get('empresa') or '').strip()
    people_count = data.get('personas')

    if not all([sede, fecha, hora, full_name, email, phone, company_name]):
        return jsonify({"message": "Debes completar todos los campos del formulario."}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"message": "El correo no tiene un formato válido."}), 400

    if sede not in SEDE_LOCATION_HINTS:
        return jsonify({"message": "La sede seleccionada no es válida."}), 400

    try:
        people_count = int(people_count)
    except Exception:
        return jsonify({"message": "El número de personas es inválido."}), 400

    if people_count <= 0 or people_count > 40:
        return jsonify({"message": "El número de personas debe estar entre 1 y 40."}), 400

    try:
        start = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')
    except Exception:
        return jsonify({"message": "Formato de fecha u hora inválido."}), 400

    if start < datetime.now():
        return jsonify({"message": "No puedes reservar un tour en una fecha pasada."}), 400

    end = start + timedelta(hours=1)
    conflict, conflict_type, no_rooms_message = find_tour_conflict(sede, start, end)

    if no_rooms_message:
        return jsonify({"message": no_rooms_message}), 404

    if conflict and conflict_type == 'room':
        return jsonify({
            "message": "Ese horario ya está ocupado por una reserva de sala.",
            "conflict": {
                "room_name": conflict.room.name,
                "start": conflict.start_time.strftime('%Y-%m-%d %H:%M'),
                "end": conflict.end_time.strftime('%Y-%m-%d %H:%M')
            }
        }), 409

    if conflict and conflict_type == 'tour':
        return jsonify({
            "message": "Ese horario ya tiene un tour solicitado en la sede.",
            "conflict": {
                "room_name": "Tour en sede",
                "start": conflict.start_time.strftime('%Y-%m-%d %H:%M'),
                "end": conflict.end_time.strftime('%Y-%m-%d %H:%M')
            }
        }), 409

    sede_name_map = {
        'ruzafa': 'Crea. Ruzafa',
        'el-carmen': 'Crea. El Carmen',
        'eixample': 'Crea. Eixample',
        'el-cabanyal': 'Crea. El Cabanyal'
    }

    new_tour = TourBooking(
        user_id=current_user_id,
        sede_slug=sede,
        sede_name=sede_name_map.get(sede, sede),
        start_time=start,
        end_time=end,
        full_name=full_name,
        email=email,
        phone=phone,
        people_count=people_count,
        company_name=company_name,
        status='requested'
    )

    db.session.add(new_tour)
    db.session.commit()

    sent, email_error = send_tour_confirmation_email(
        to_email=email,
        full_name=full_name,
        sede_name=new_tour.sede_name,
        fecha=fecha,
        hora=hora,
        people_count=people_count,
        company_name=company_name
    )

    if not sent:
        return jsonify({
            "message": "Tour reservado, pero no se pudo enviar el correo de confirmación.",
            "email_error": email_error
        }), 202

    return jsonify({"message": "Tour reservado correctamente."}), 201

@bookings_bp.route('/my-bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    # 1. Identificamos al usuario por su token
    current_user_id = get_jwt_identity()
    
    # 2. Buscamos todas sus reservas en la base de datos
    user_bookings = Booking.query.filter_by(user_id=current_user_id).all()
    
    # 3. Formateamos la respuesta para que sea bonita
    result = []
    for b in user_bookings:
        result.append({
            "id": b.id,
            "room_id": b.room_id,
            "room_name": b.room.name, # ¡Gracias a la relación db.relationship!
            "start_time": b.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": b.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_price": b.total_price,
            "status": b.status,
            "payment_status": b.payment_status,
            "payment_method": b.payment_method
        })
    
    return jsonify(result), 200

@bookings_bp.route('/admin/all', methods=['GET'])
@jwt_required()
def get_all_bookings():
    # 1. Verificamos que el que llama sea administrador
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Acceso denegado: Se requieren permisos de administrador"}), 403
    
    # 2. Obtenemos todas las reservas de la base de datos
    all_bookings = Booking.query.all()
    
    # 3. Formateamos la respuesta incluyendo datos del usuario y de la sala
    result = []
    for b in all_bookings:
        result.append({
            "id": b.id,
            "user_id": b.user_id,
            "user_name": b.user.full_name, # Relación con tabla Users
            "room_name": b.room.name,      # Relación con tabla Rooms
            "start_time": b.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": b.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_price": b.total_price,
            "status": b.status,
            "payment_status": b.payment_status,
            "payment_method": b.payment_method
        })
    
    return jsonify(result), 200


@bookings_bp.route('/admin/tours', methods=['GET'])
@jwt_required()
def get_all_tour_bookings():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Acceso denegado: Se requieren permisos de administrador"}), 403

    tours = TourBooking.query.order_by(TourBooking.start_time.desc()).all()

    result = []
    for t in tours:
        result.append({
            "id": t.id,
            "user_id": t.user_id,
            "user_name": t.user.full_name if t.user else None,
            "sede_slug": t.sede_slug,
            "sede_name": t.sede_name,
            "start_time": t.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": t.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "full_name": t.full_name,
            "email": t.email,
            "phone": t.phone,
            "people_count": t.people_count,
            "company_name": t.company_name,
            "status": t.status,
            "created_at": t.created_at.strftime('%Y-%m-%d %H:%M:%S') if t.created_at else None
        })

    return jsonify(result), 200

@bookings_bp.route('/<int:booking_id>/cancel', methods=['PATCH'])
@jwt_required()
def cancel_booking(booking_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    # 1. Buscar la reserva
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "La reserva no existe"}), 404

    # 2. Seguridad: ¿Es el dueño de la reserva o es admin?
    if str(booking.user_id) != str(current_user_id) and claims.get("role") != "admin":
        return jsonify({"message": "No tienes permiso para cancelar esta reserva"}), 403

    # 3. Verificar si ya estaba cancelada
    if booking.status == 'cancelled':
        return jsonify({"message": "La reserva ya está cancelada"}), 400

    # 4. Cambiar el estado (Borrado Lógico)
    booking.status = 'cancelled'
    
    try:
        db.session.commit()
        return jsonify({"message": f"Reserva {booking_id} cancelada correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al procesar la cancelación"}), 500