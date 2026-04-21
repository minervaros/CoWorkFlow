from flask import Blueprint, request, jsonify
from app import db
from app.models import Room
from flask_jwt_extended import jwt_required, get_jwt

rooms_bp = Blueprint('rooms', __name__)

# --- RUTA: LISTAR TODAS LAS SALAS (Pública o Logueados) ---
@rooms_bp.route('/', methods=['GET'])
def get_rooms():

    active_only = request.args.get('active_only', 'true') == 'true'

    if active_only:
        rooms = Room.query.filter_by(is_active=True).all()
    else:
        rooms = Room.query.all()

    return jsonify([{
        "id": r.id,
        "name": r.name,
        "description": r.description,
        "capacity": r.capacity,
        "price_per_hour": r.price_per_hour,
        "is_active": r.is_active,
        "image_url": r.image_url
    } for r in rooms]), 200

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
        description=data.get('description', ''),
        capacity=data['capacity'],
        price_per_hour=data['price_per_hour'],
        image_url=data.get('image_url', '')
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
    room.description = data.get('description', room.description)
    room.capacity = data.get('capacity', room.capacity)
    room.price_per_hour = data.get('price_per_hour', room.price_per_hour)

    db.session.commit()
    return jsonify({"message": "Sala actualizada con éxito"}), 200

# --- RUTA: DESACTIVAR/BORRAR SALA (Solo Admins) ---
@rooms_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_room(id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "No tienes permiso"}), 403

    room = Room.query.get_or_404(id)
    
    # En lugar de borrar físicamente, cambiamos el estado
    room.is_active = False 
    
    db.session.commit()
    return jsonify({"message": "Sala desactivada correctamente"}), 200