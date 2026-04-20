from flask import Blueprint, request, jsonify
from app import db
from app.models import Room
from flask_jwt_extended import jwt_required, get_jwt

rooms_bp = Blueprint('rooms', __name__)

# --- RUTA: LISTAR TODAS LAS SALAS (Pública o Logueados) ---
@rooms_bp.route('/', methods=['GET'])
def get_rooms():
    rooms = Room.query.filter_by(is_active=True).all()
    return jsonify([{
        "id": r.id,
        "name": r.name,
        "capacity": r.capacity,
        "price": r.price_per_hour
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
        price_per_hour=data['price_per_hour']
    )
    
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"message": "Sala creada con éxito"}), 201