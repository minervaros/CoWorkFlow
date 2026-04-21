from flask import Blueprint, request, jsonify
from app import db
from app.models import Booking, Room
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    room_id = data.get('room_id')
    start_str = data.get('start_time')
    end_str = data.get('end_time')

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
        total_price=price
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Reserva realizada con éxito", "total_price": price}), 201

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
            "status": b.status
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
            "status": b.status
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