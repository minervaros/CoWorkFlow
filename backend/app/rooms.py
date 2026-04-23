from flask import Blueprint, request, jsonify
from app import db
from app.models import Room, Booking
from flask_jwt_extended import jwt_required, get_jwt
import json

rooms_bp = Blueprint('rooms', __name__)


def parse_equipamiento(raw_equipamiento):
    if not raw_equipamiento:
        return []

    if isinstance(raw_equipamiento, list):
        return [str(item).strip() for item in raw_equipamiento if str(item).strip()]

    if isinstance(raw_equipamiento, str):
        try:
            parsed = json.loads(raw_equipamiento)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except Exception:
            pass

        return [item.strip() for item in raw_equipamiento.split(',') if item.strip()]

    return []


def serialize_equipamiento(raw_equipamiento):
    return json.dumps(parse_equipamiento(raw_equipamiento), ensure_ascii=False)


def serialize_room(room):
    return {
        "id": room.id,
        "name": room.name,
        "location": room.location,
        "equipamiento": parse_equipamiento(room.equipamiento),
        "description": room.description,
        "capacity": room.capacity,
        "price_per_hour": room.price_per_hour,
        "is_active": room.is_active,
        "is_deleted": room.is_deleted,
        "image_url": room.image_url
    }

# --- RUTA: LISTAR TODAS LAS SALAS (Pública o Logueados) ---
@rooms_bp.route('/', methods=['GET'])
def get_rooms():

    active_only = request.args.get('active_only', 'true') == 'true'
    include_deleted = request.args.get('include_deleted', 'false') == 'true'

    if include_deleted:
        # Admin: incluye salas eliminadas
        if active_only:
            rooms = Room.query.filter_by(is_active=True).all()
        else:
            rooms = Room.query.all()
    else:
        # Usuario: excluye salas eliminadas
        if active_only:
            rooms = Room.query.filter_by(is_active=True, is_deleted=False).all()
        else:
            rooms = Room.query.filter_by(is_deleted=False).all()

    return jsonify([serialize_room(r) for r in rooms]), 200


@rooms_bp.route('/<int:id>', methods=['GET'])
def get_room(id):
    room = Room.query.filter_by(id=id, is_deleted=False).first_or_404()
    return jsonify(serialize_room(room)), 200

# --- RUTA: CREAR SALA (Solo Admins) ---
@rooms_bp.route('/', methods=['POST'])
@jwt_required()
def create_room():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "No tienes permiso"}), 403

    data = request.get_json()
    new_room = Room(
        name=data['name'],
        location=data.get('location', ''),
        equipamiento=serialize_equipamiento(data.get('equipamiento', [])),
        description=data.get('description', ''),
        capacity=data['capacity'],
        price_per_hour=data['price_per_hour'],
        image_url=data.get('image_url', ''),
        is_active=bool(data.get('is_active', True))
    )
    
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"message": "Sala creada con éxito"}), 201

# --- RUTA: ACTUALIZAR SALA (Solo Admins) ---
@rooms_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_room(id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "No tienes permiso"}), 403

    room = Room.query.get_or_404(id)
    data = request.get_json()

    if 'is_active' in data:
        room.is_active = data['is_active']

    room.name = data.get('name', room.name)
    room.location = data.get('location', room.location)
    if 'equipamiento' in data:
        room.equipamiento = serialize_equipamiento(data.get('equipamiento', []))
    room.description = data.get('description', room.description)
    room.capacity = data.get('capacity', room.capacity)
    room.price_per_hour = data.get('price_per_hour', room.price_per_hour)
    room.image_url = data.get('image_url', room.image_url)

    db.session.commit()
    return jsonify({"message": "Sala actualizada con éxito"}), 200

# --- RUTA: BORRAR SALA (Solo Admins) ---
@rooms_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_room(id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "No tienes permiso"}), 403

    room = Room.query.get_or_404(id)

    room.is_deleted = True
    db.session.commit()
    return jsonify({"message": "Sala eliminada correctamente"}), 200